# 現在のコミット状態において、javaファイルのすべての行を取得する
import subprocess
import os
import sys
from clf import *
from git import *


def main():
    # ディレクトリ取得
    abs_dir_of_java = sys.argv[1]
    if abs_dir_of_java[-1] is not '/':
        abs_dir_of_java += '/'
    current_dir_of_analyzer = os.getcwd() + '/'

    # 結果出力ファイルの初期化
    filename = abs_dir_of_java.split('/')[-2]
    print(filename)
    with open(current_dir_of_analyzer + filename + '_results/all_commits_lines.txt', 'w') as f:
        f.write('')

    # git の初期化
    os.chdir(abs_dir_of_java)  # ディレクトリを移動
    subprocess.call('git pull origin master'.split())
    subprocess.call(['git', 'checkout', TARGET_SHA[filename]])

    # 変数初期化
    repo = Repo(abs_dir_of_java)
    commits = [item for item in repo.iter_commits('master')]
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
        with open(current_dir_of_analyzer + filename + '_results/all_bugfix_commits_lines.txt', 'a') as f:
            f.write('\n'.join(_insertions))

    print(cnt)
if __name__ == '__main__':
    main()
