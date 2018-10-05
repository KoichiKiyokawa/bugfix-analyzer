import sys

# 入力：コードのある行
# 出力：その行の先頭にある空白の数(インデント)
def count_intent(code):
    cnt = 0
    for word in code:
        if word is not ' ':
            break
        cnt += 1
    
    return cnt
        
def main():
    filename = sys.argv[1]
    with open(filename) as f:
        for line in f:
            code = line[1:].rstrip()  # 「先頭の+か-」と改行を削除
            # print(code)
            print(count_intent(code))


if __name__ == '__main__':
    main()