# bugfix-analyzer  

## 注意
- ディレクトリ構造は以下の通りにすること
```
.┐
 ├ bugfix-analyzer
 ├ <分析対象のディレクトリ>
 └ <分析対象のディレクトリ>
 
```
- Pythonのバージョン　`3.6.5`  
- `<分析対象のディレクトリ名>_results`というディレクトリを`bugfix-analyzer/`下に作ってから実行すること

## clf.py
研究対象となるコミットのハッシュ(どこまでのコミットを解析するか指定)や、バグ修正コミットと判別する条件などを記述

## distribute_bugfix_diff.py

```
python distribute_bugfix_diff.py ../<分析対象のディレクトリ名>
```

　バグ修正のために挿入された行のうち、バグ修正コミットの一つ前のコミットの状態でソースコードに含まれていたものを出力。出力先は`<分析対象のディレクトリ名>_results/bugfix_lines.txt`

## distribute_bugfix_diff_levenshtein.py

```
python distribute_bugfix_diff_levenshtein.py ../<分析対象のディレクトリ名> <しきい値>
```
　完全一致ではなく、レーベンシュタイン距離がしきい値*以下*であればカウントする。  
出力先は`<分析対象のディレクトリ名>_results/Levenshtein<しきい値>.txt.txt`
 
## gather.py
 
 ```
 python gather.py ../<分析対象のディレクトリ名>
 ```
 
 バグ修正のために挿入された行をすべて取得して出力。  
 出力先は、`<分析対象のディレクトリ名>_results/all_bugfix_commits_lines.txt`

## check_message.py
```
python check_message.py ../<分析対象のディレクトリ名>
```

バグ修正コミットのメッセージのみを取得して出力。  
出力先は、`<分析対象のディレクトリ名>_results/bugfix_commits_messages.txt`  
バグ修正コミットの判定が正しいかチェックするときに使うと良い。
