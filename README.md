# Network-Analysis
有向グラフを用いてネットワーク分析した時のメモ  
Python 2.7.16
## network_sample.py
networkx使って隣接行列から有向グラフを構築する。
![img](https://user-images.githubusercontent.com/45719980/71140621-2108a280-2255-11ea-9bdb-fe5866efe082.png)

## 実データを使う
### データ収集
APIを叩いてall_edge_lists.jsonを用意する。
### 分析
```
$ python create_directed_graph.py
```
以下のような画像が出力される
#### dot
![directed_graph_dot](https://user-images.githubusercontent.com/45719980/72315442-292df380-36d6-11ea-95dc-3814016695a6.png)
#### fdp
![directed_graph_fdp](https://user-images.githubusercontent.com/45719980/72315443-29c68a00-36d6-11ea-80f4-0d10c8313417.png)
