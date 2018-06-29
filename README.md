# cluster_constraints

课题是Trec2016微博检索任务，根据推特数据和给定主题检索相关推特。

```python
#推特数据
#Tue Aug 02 00:00:45 +0000 2016*-*-*760264035140984832*-*-*Make choice.

#给定主题
#{ "topid" : "RTS1",
#  "title" : "transgender bathrooms",
#  "description" : "Find information on different sides of the debate on which bathroom can be used by a transgender individual",
#  "narrative" : "The user is interested in the politics of the transgender bathroom debate, including current and proposed bills, as well as backlash and economic implications (for example, boycotts)."}
```

利用谷歌镜像网站检索给定主题，前50条检索结果中的关键词按TF-IDF排序，前10作为主题扩展。

spider.py             爬虫  
wiki.py               获取维基百科内容  
calculate\_q\_main.py 计算每个扩展词的IDF主函数  
calculate\_q.py       计算每个扩展词的IDF  

计算每条推特与每个主题的BM25相关度，

cluster_main.py       聚类过程主函数  
cluster.py            聚类过程  
\_main.py             主函数  
tweet.py              tweet类，用于解析数据和输出结果   
nmf.py                nmf类，包括一般形式的非负矩阵分解和正则化的非负矩阵分解  
rerank_main.py        重排序主函数  
rerank.py             重排序过程  
res_formal.py         格式化输出，用于评测  
eval_main.py          评测主函数  
eval.py               结果评测过程  