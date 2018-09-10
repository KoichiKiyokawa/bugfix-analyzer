# 現在のコミット状態において、javaファイルのすべての行を取得する
import subprocess


# その行がコメント、もしくは特に意味のない行であったらFalseを返す
def is_code_line(code):
    SIX_WORDS_EXCEPTION_LIST = 'import static'.split()
    THREE_WORDS_EXCEPTION_LIST = 'try'.split()
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
    if len(code) >= 3:
        if code[:3] in THREE_WORDS_EXCEPTION_LIST:
            return False
    if len(code) >= 6:
        if code[:6] in SIX_WORDS_EXCEPTION_LIST:
            return False

    return True


def main():
    java_files_paths = subprocess.check_output('find . -name *.java'.split())
    # print(java_files.decode()) ok

    for java_file_path in java_files_paths.decode().split('\n'):
        # print(java_file_path) ok
        if len(java_file_path) == 0:
            break
        with open(java_file_path, 'r') as jf:
            for j_line in jf:
                code = j_line.lstrip()
                if is_code_line(code):
                    print(code, end='')


if __name__ == '__main__':
    main()
