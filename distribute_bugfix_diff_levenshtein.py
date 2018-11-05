from git import *
import sys
import os
import datetime
import time
import subprocess
from clf import *
import Levenshtein


def is_similar(string_a, string_b, threshold):
    # 再起結果保存するためのテーブル
    # 横幅はstring_a+1, 縦幅はstring_b+1
    # string_aはa, colと、string_bはb, rowと対応している
    # 端まで→からの端まで↓をワンセットとして順に埋めていく
    # ![参考画像](images_for_comment/lev.jpg) 丸数字がpivot
    recursive_table = [
        [None for a in range(len(string_a)+1)] for b in range(len(string_b)+1)
    ]
    recursive_table[0][0] = 0

    # 関数内関数
    # (_row, _col)のマスを埋める
    def fill_square(_row, _col):
        if _row == 0 and _col == 0:
            return
        # 各マスには1 ~ 3のうち最も小さいものを入れる
        # 1 自分のマスの上のマスの数字 + 1
        # 2 自分のマスの左のマスの数字 + 1
        # 3 自分のマスの左上のマスの数字 + c
        # （ただし自分の縦と横の文字が等しい場合は c = 0、異なる場合は c = 1）
        candidate_up = 9999  # 1
        candidate_left = 9999  # 2
        candidate_left_up = 9999  # 3
        if _row - 1 >= 0:
            # 上の数字 + 1
            candidate_up = recursive_table[_row - 1][_col] + 1
        if _col - 1 >= 0:
            # 左の数字 + 1
            candidate_left = recursive_table[_row][_col - 1] + 1
        if _row - 1 >= 0 and _col - 1 >= 0:
            # 左上の数字 (+ 1)
            # ex)2行3列目だったら、string_bの1文字目とstring_aの2文字目を比較
            # 1行目は□, 1列目は□であることに注意
            if string_a[_col-1] == string_b[_row-1]:
                # 行と列の文字が同じ場合はそのまま
                candidate_left_up = recursive_table[_row - 1][_col - 1]
            else:
                # 違う場合は+1する
                candidate_left_up = recursive_table[_row - 1][_col - 1] + 1
        recursive_table[_row][_col] = min(
            candidate_up, candidate_left, candidate_left_up)

    # pivotは(n, n)の座標。→と↓の交点にあたる。
    # nの範囲は表の縦と横のうち小さい方
    # 表の横はstring_aの文字数+1
    # 表の縦はstring_bの文字数+1であることに注意
    for pivot in range(min(len(string_a) + 1, len(string_b) + 1)):
        # まずはpivotを埋める
        fill_square(pivot, pivot)
        # ワンセットの中で最小値は必ずpivotである TODO:証明
        # よってpivotがしきい値を超えていたらすぐにFalseを返す
        if recursive_table[pivot][pivot] > threshold:
            return False
        # 次に端まで→の向きに埋めていく
        row = pivot
        for col in range(pivot+1, len(string_a)+1):
            fill_square(row, col)

        # 次に↓の向きに端まで埋めていく
        col = pivot
        for row in range(pivot + 1, len(string_b) + 1):
            fill_square(row, col)

    return recursive_table[-1][-1] <= threshold


def main():
    # ディレクトリ取得
    abs_dir_of_java = sys.argv[1]
    if abs_dir_of_java[-1] is not '/':
        abs_dir_of_java += '/'
    current_dir_of_analyzer = os.getcwd() + '/'

    # レーベンシュタイン距離のしきい値を取得
    threshold_for_Levenshtein = int(sys.argv[2])

    # 結果出力ファイルの初期化
    filename = abs_dir_of_java.split('/')[-2]
    print(filename)
    with open(current_dir_of_analyzer + filename + '_results/bugfix_lines.txt', 'w') as f:
        f.write('')

    # git の初期化
    os.chdir(abs_dir_of_java)  # ディレクトリを移動
    subprocess.call('git pull origin master'.split())
    subprocess.call(['git', 'checkout', TARGET_SHA[filename]])

    # 変数初期化
    repo = Repo(abs_dir_of_java)
    commits = [item for item in repo.iter_commits('master')]
    insertions = 0
    cnt = 0

    # 新しいコミットから処理
    for i in range(len(commits)):
        cnt += 1
        if not is_bugfix_commit(commits[i], filename):
            continue
        diffs = subprocess.check_output(
            # 配列で渡す必要あり。Javaのファイルのみを分析。
            ['git', 'diff', commits[i+1].hexsha,
                commits[i].hexsha, '*.java']
        )
        _insertions, _deletions = distribute_diff(diffs)  # 差分を振り分け
        # ひとつ古いコミットにチェックアウト
        subprocess.call(['git', 'checkout', '--force', commits[i + 1].hexsha])
        # ソースコードを取得
        java_files_paths = subprocess.check_output(
            'find . -name *.java'.split())
        srcs = []
        for java_file_path in java_files_paths.decode().split('\n'):
            if len(java_file_path) == 0:
                break
            with open(java_file_path, mode='r', errors='ignore') as jf:
                for j_line in jf:
                    code = j_line.strip()
                    if is_code_line(code):
                        srcs.append(code)

        # TODO: git logで挿入された行を取得できないと、無理
        # コードの見通しのために入っている改行を取り除く
        # for i in range(len(_insertions)):
        #     # has_linefeed_for_look = False
        #     open_bracket_count = _insertions[i].count('(')
        #     close_bracket_count = _insertions[i].count(')')
        #     index_tmp = i + 1
        #     while open_bracket_count != close_bracket_count:  # 開きカッコと閉じカッコの数が一緒になるまで
        #         open_bracket_count += _insertions[index_tmp].count('(')
        #         close_bracket_count = _insertions[index_tmp].count(')')
        #         _insertions[i] += _init_externals[index_tmp]
        #         del _insertions[index_tmp]
        #         index_tmp += 1

        # 結果を出力
        with open(current_dir_of_analyzer + filename + '_results/Levenshtein{}.txt'.format(threshold_for_Levenshtein), 'a') as f:
            for insert in _insertions:
                # if insert in srcs:
                #     f.write(insert + '\n')
                for src in srcs:
                    # if Levenshtein.distance(insert, src) <= threshold_for_Levenshtein:最後まで計算してしまうので遅い
                    if is_similar(insert, src, threshold_for_Levenshtein):
                        f.write(insert + '\n')
                        break

        insertions += commits[i].stats.total['insertions']

    print('sum of insert lines:', insertions)
    print('number of commits:', cnt)


if __name__ == '__main__':
    main()
