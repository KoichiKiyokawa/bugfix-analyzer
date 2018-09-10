from git import *
import datetime
import time
import subprocess
from numba import jit


# 挿入行と削除行とに振り分ける
# @params also_delete: 削除行についても処理するか
@jit
def distribute_diff(diffs, also_delete=False):
    insertions = deletions = []

    for line in diffs.decode('utf-8', 'replace').split('\n'):
        # print(line) ok
        if is_git_output(line):
            continue
        code = line[1:].lstrip()  # +とか-とか最初の空白を削除
        if is_not_code_line(code):
            continue
        # print(code) ok
        if line[0] is '+':
            insertions.append(code)
        elif line[0] is '-' and also_delete:
            deletions.append(code)

    return insertions, deletions


# git logによって出力された、コードとは関係のない行だったらtrueを返す
@jit
def is_git_output(line):
    if len(line) >= 3:
        if line[:3] == '+++' or line[:3] == '---':  # +++とか---で始まるものはファイル名に関するもの
            return True
        elif line[0] is '+' or line[0] is '-':  # それ以外で+とか-で始まるものは「コードとは関係のないgitの出力」ではない
            return False
        else:  # それ以外はコードとは関係のないgit出力
            return True
    else:
        return False


# コメント行とか関係のない行だったらtrueを返す。最初の数文字を判定
@jit
def is_not_code_line(code):
    SIX_WORDS_EXCEPTION_LIST = 'import static'.split()
    THREE_WORDS_EXCEPTION_LIST = 'try'.split()
    TWO_WORDS_EXCEPTION_LIST = '// /*'.split()
    ONE_WORD_EXCEPTION_LIST = '@ * ;'.split()

    if not code:
        return True
    elif len(code) >= 6:
        return (code[:6] in SIX_WORDS_EXCEPTION_LIST
                or code[:3] in THREE_WORDS_EXCEPTION_LIST
                or code[:2] in TWO_WORDS_EXCEPTION_LIST
                or code[0] in ONE_WORD_EXCEPTION_LIST)
    elif len(code) >= 3:
        return (code[:3] in THREE_WORDS_EXCEPTION_LIST
                or code[:2] in TWO_WORDS_EXCEPTION_LIST
                or code[0] in ONE_WORD_EXCEPTION_LIST)
    elif len(code) >= 2:
        return code[:2] in TWO_WORDS_EXCEPTION_LIST or code[0] in ONE_WORD_EXCEPTION_LIST
    elif len(code) >= 1:
        if len(code) == 1 and code[0] in ['{', '}']:
            return True
        return code[0] in ONE_WORD_EXCEPTION_LIST


# バグ修正のコミットだと見分ける条件 for commons-math
# FixedDの単語がなく、fixの単語があるもの
@jit
def is_bugfix_commit(item):
    return item.message.find('FixedD') is -1 and item.message.find('fix') > -1


repo = Repo('./')
commits = [item for item in repo.iter_commits('master')]
# 初期化
with open('res.txt', 'w') as f:
    f.write('')


@jit
def main():
    cnt = 0
    insertions = 0
    for i in range(len(commits))[::-1]:
        if 1000 < cnt:
            if is_bugfix_commit(commits[i]):
                # print(item.message) ok
                diffs = subprocess.check_output(
                    # 配列で渡す必要あり。Javaのファイルのみを分析。逆順にfor文を回しているので一つ前のコミットはi+1
                    ['git', 'diff', commits[i].hexsha,
                        commits[i+1].hexsha, '*.java']
                )
                _insertions, _deletions = distribute_diff(diffs)  # 差分を振り分け
                insert_f = open('res.txt', 'a')
                insert_f.write('\n'.join(_insertions))
                insert_f.close()
                insertions += commits[i].stats.total['insertions']

        cnt += 1
    # print(bugfix_cnt) 53
    print(insertions)


if __name__ == '__main__':
    main()
