import os
import sys
import subprocess
from git import *
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

    # git の初期化
    os.chdir(abs_dir_of_java)  # ディレクトリを移動
    subprocess.call('git pull origin master'.split())
    subprocess.call(['git', 'checkout', TARGET_SHA[filename]])

    # 変数初期化
    repo = Repo(abs_dir_of_java)
    commits = [item for item in repo.iter_commits('master')]
    cnt = 0
    bugfix_cnt = 0

    # 新しいコミットから処理
    with open(current_dir_of_analyzer + filename + '_results/bugfix_commits_messages.txt', 'w') as f:
        for i in range(len(commits)):
            cnt += 1
            if is_bugfix_commit(commits[i], filename):
                bugfix_cnt += 1
                f.write(commits[i].message)
            print(commits[i].hexsha)

    print('number of commits:', cnt)
    print('number of bugfix commits:', bugfix_cnt)

if __name__ == '__main__':
    main()
