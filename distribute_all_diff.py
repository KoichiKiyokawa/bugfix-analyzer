from git import *
import datetime
import time
import subprocess
from numba import jit


# 挿入行と削除行とに振り分ける
# @params also_delete: 削除行についても処理するか
@jit
def distribute_diff(diffs, also_delete=False):
    EXCEPTION_LIST = 'try static import'.split()  # 特に意味のない行を含めないように
    insertions = []
    deletions = []

    for line in diffs.decode('utf-8', 'replace').split('\n'):
        # print(line) ok
        if is_git_output(line):
            continue
        code = line[1:].lstrip()  # +とか-とか最初の空白を削除
        if is_not_code_line(code):
            continue
        if code in EXCEPTION_LIST:
            continue
        # print(code) ok
        if line[0] is '+':
            insertions.append(code)
        elif also_delete:
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


# コメント行とか関係のない行だったらtrueを返す
@jit
def is_not_code_line(code):
    TWO_WORDS_EXCEPTION_LIST = '// /*'.split()
    ONE_WORD_EXCEPTION_LIST = '{ } @ * ;'.split()

    if not code:
        return True
    elif len(code) >= 2:
        return code[:2] in TWO_WORDS_EXCEPTION_LIST or code[0] in ONE_WORD_EXCEPTION_LIST
    elif len(code) >= 1:
        return code[0] in ONE_WORD_EXCEPTION_LIST


# バグ修正のコミットだと見分ける条件 for commons-math
# http~のリンクがなく、fixedの単語がなく、fixの単語があるもの
@jit
def is_bugfix_commit(item):
    return (item.message.find('http') is -1
            and item.message.find('fixed') is -1
            and item.message.find('fix') > -1)


@jit
def main():
    # すべての変更を挿入行と削除行に振り分ける
    diffs = subprocess.check_output(
        # 配列で渡す必要あり。古い順に1000コミットまで。Javaのファイルのみを分析
        ['git', 'log', '-p', '--before="2007-09-10 17:23:21"', '--reverse', '*.java']
    )
    _insertions, _deletions = distribute_diff(diffs)  # 差分を振り分け
    insert_f = open('res.txt', 'a')
    insert_f.write('\n'.join(_insertions))
    insert_f.close()


if __name__ == '__main__':
    main()
