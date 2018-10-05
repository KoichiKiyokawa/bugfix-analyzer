# 「バグ修正のコミットかどうか」など判定機を格納しておく
import sys

# 定数たち
TARGET_SHA = {
    'commons-math': 'e009e73e7512a36ab6fa8933fba7de454c4fa39a',
    'closure-compiler': '739189d54feb7523a33917dbb1b0d6cf996e554c',
    'commons-lang': '6dc3a6db11d7e63c960ccc6cf48aa15d6f00e903',
    'jfreechart': '520a4be69ba932061ab9b89f328842caf152e1d9',
    'mockito': 'e51a0515ac8440572cf1af80f7aa620d51e8075e',
    'joda-time': 'add3cf9f2ba7aad62f3f96a43fdd69ee944c3eae',
}


# バグ修正のコミットだと見分ける条件
def is_bugfix_commit(item, filename):
    commit_message = item.message
    if filename == 'commons-math':
        return (commit_message.find('FixedD') is - 1
                and commit_message.find('fix') > -1
                or commit_message.find('Fix') > -1)
    elif filename == 'closure-compiler':
        return (commit_message.find('debugg') is - 1
                and commit_message.find('bug') > -1)
    elif filename == 'commons-lang':
        return (commit_message.find('bug') > -1
                and commit_message.find('fix') > -1
                or commit_message.find('Fix') > -1)
    elif filename == 'jfreechart':
        return (commit_message.find('Fix') > -1)
    elif filename == 'mockito':
        return (commit_message.find('Fix') > -1
                or commit_message.find('fix') > -1)
    elif filename == 'joda-time':
        return (commit_message.find('Fix') > -1
                or commit_message.find('fix') > -1)
    else:
        sys.stderr.write('バグ修正コミット判定が定義されていません')


# その行がコメント、もしくは特に意味のない行であったらFalseを返す
def is_code_line(code):
    TWO_WORDS_EXCEPTION_LIST = '// /*'.split()
    ONE_WORD_EXCEPTION_LIST = '{ } @ * ;'.split()

    if not code:
        return False
    if len(code) >= 1:
        if code[0] in ONE_WORD_EXCEPTION_LIST:
            return False
    if len(code) >= 2:
        if code[:2] in TWO_WORDS_EXCEPTION_LIST:
            return False

    return True


# git logによって出力された、コードとは関係のない行だったらtrueを返す
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


# 挿入行と削除行とに振り分ける
# @params also_delete: 削除行についても処理するか
def distribute_diff(diffs, also_delete=False):
    insertions = deletions = []

    for line in diffs.decode('utf-8', 'replace').split('\n'):
        # print(line) ok
        if is_git_output(line):
            continue
        code = line[1:].lstrip()  # +とか-とか最初の空白を削除
        if not is_code_line(code):
            continue
        # print(code) ok
        if line[0] is '+':
            insertions.append(code)
        elif line[0] is '-' and also_delete:
            deletions.append(code)

    return insertions, deletions
