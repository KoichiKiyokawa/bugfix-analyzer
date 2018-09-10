# バグ修正コミットの挿入行とある時点でのjavaファイルの行を比較。
# 「バグ修正で追加される行の多くはその時点でのソースコードに存在している」という仮説を検証

# バグ修正コミットの挿入行が集まったファイル bugfix_lines.txt
# ある時点でのjavaファイルのすべての行が集まったファイル gather.txt or unique.txt

from numba import jit
import sys

# init
with open('compare_result.txt', 'w') as f:
    f.write('')

@jit
def main():
    gather_f = open('gather.txt', 'r')
    sources = list(set(gather_f.readlines()))
    gather_f.close()
    # print(sources) ok
    f = open('bugfix_lines.txt', 'r')
    fout = open('compare_result.txt', 'w')
    cnt = 0
    for line in f:
        if line in sources:
            fout.write(line)
        if cnt % 1000 == 0:
            sys.stdout.write('\r{}'.format(cnt))
            sys.stdout.flush()
        cnt += 1
    f.close
    fout.close()

if __name__ == '__main__':
    main()
