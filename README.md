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

## distribute_bugfix_diff

```
python distribute_bugfix_diff.py ../<分析対象のディレクトリ名>
```

　バグ修正のために挿入された行のうち、バグ修正コミットの一つ前のコミットの状態でソースコードに含まれていたものを出力。出力先は`<分析対象のディレクトリ名>_results/bugfix_lines.txt`
 
 ## gather
 
 ```
 python gather.py ../<分析対象のディレクトリ名>
 ```
 
 バグ修正のために挿入された行をすべて取得して出力。  
 出力先は、`<分析対象のディレクトリ名>_results/all_bugfix_commits_lines.txt`

## check_message
```
python check_message.py ../<分析対象のディレクトリ名>
```

バグ修正コミットのメッセージのみを取得して出力。  
出力先は、`<分析対象のディレクトリ名>_results/bugfix_commits_messages.txt`  
バグ修正コミットの判定が正しいかチェックするときに使うと良い。
