# 「バグ修正のコミットかどうか」など判定機を格納しておく

# 定数たち
TARGET_SHA = {
    'commons-math': 'e009e73e7512a36ab6fa8933fba7de454c4fa39a',
}

# その行がコメント、もしくは特に意味のない行であったらFalseを返す
def is_code_line(code):
    TWO_WORDS_EXCEPTION_LIST = '// /*'.split()
    ONE_WORD_EXCEPTION_LIST = '@ * ;'.split()

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


# バグ修正のコミットだと見分ける条件 for commons-math
# FixedDの単語がなく、fixの単語があるもの
def is_bugfix_commit(item):
    return item.message.find('FixedD') is -1 and item.message.find('fix') > -1


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
