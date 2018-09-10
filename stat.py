from git import *
import datetime
import time
import subprocess


def is_bugfix_commit(item):
    return item.message.find('FixedD') is -1 and item.message.find('fix') > -1


repo = Repo('./')
commits = [item for item in repo.iter_commits('master')]


def main():
    cnt = 0
    bugfix_cnt = 0
    for i in range(len(commits))[::-1]:
        item = commits[i]
        # バグ修正コミットの割合を調べる
        with open('stat.txt', 'w') as f:
            if is_bugfix_commit(item):
                f.write('-----bugfix commit-----')
                bugfix_cnt += 1
            else:
                f.write('n')

            cnt += 1
            if cnt % 1000 == 0:
                print('reached {}commits'.format(cnt))
                print(item.hexsha)
                print('{} ~ {}までのバグ'.format(cnt - 999, cnt), bugfix_cnt)
                bugfix_cnt = 0  # 初期化


if __name__ == '__main__':
    main()
