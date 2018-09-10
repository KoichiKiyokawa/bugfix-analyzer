from git import *
import sys
import os
import datetime
import time
import subprocess
from clf import *


def main():
    # ディレクトリ取得
    abs_dir_of_java = sys.argv[1]
    if abs_dir_of_java[-1] is not '/':
        abs_dir_of_java += '/'
    current_dir_of_analyzer = os.getcwd() + '/'

    # 結果出力ファイルの初期化
    filename = abs_dir_of_java.split('/')[-2]
    print(filename)
    with open(current_dir_of_analyzer + filename + '_results/bugfix_lines.txt', 'w') as f:
        f.write('')

    # git の初期化
    os.chdir(abs_dir_of_java)  # ディレクトリを移動
    subprocess.call('git pull origin master'.split())
    subprocess.call(['git', 'checkout', TARGET_SHA[filename]])

    # 変数初期化
    repo = Repo(abs_dir_of_java)
    commits = [item for item in repo.iter_commits('master')]
    insertions = 0
    cnt = 0

    # 新しいコミットから処理
    for i in range(len(commits)):
        cnt += 1
        if not is_bugfix_commit(commits[i], filename):
            continue
        diffs = subprocess.check_output(
            # 配列で渡す必要あり。Javaのファイルのみを分析。
            ['git', 'diff', commits[i].hexsha,
                commits[i+1].hexsha, '*.java']
        )
        _insertions, _deletions = distribute_diff(diffs)  # 差分を振り分け

        # ひとつ古いコミットにチェックアウト
        subprocess.call(['git', 'checkout', commits[i + 1].hexsha])
        # ソースコードを取得
        java_files_paths = subprocess.check_output(
            'find . -name *.java'.split())
        srcs = []
        for java_file_path in java_files_paths.decode().split('\n'):
            if len(java_file_path) == 0:
                break
            with open(java_file_path, mode='r', errors='ignore') as jf:
                for j_line in jf:
                    code = j_line.strip()
                    if is_code_line(code):
                        srcs.append(code)

        # 結果を出力
        with open(current_dir_of_analyzer + filename + '_results/bugfix_lines.txt', 'a') as f:
            for insert in _insertions:
                if insert in srcs:
                    f.write(insert + '\n')

        insertions += commits[i].stats.total['insertions']

    print('sum of insert lines:', insertions)
    print('number of commits:', cnt)

if __name__ == '__main__':
    main()
