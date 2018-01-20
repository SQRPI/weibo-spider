# weibo-spyder
社交网络挖掘期末Project 大数据相关微博用户关系爬虫


## 已实现功能
* 搜索特定标签用户
* uid和昵称转换
* 批量爬取指定用户标签
* 批量爬取用户关系列表
* 微博内容提取和分析
* 5000页面每小时的反反爬虫机制

## 使用方法

* 在cookies.txt中输入你的cookie(可输入多个)
* 在uids.txt中输入要爬取人的uid
* python content.py
* 其他功能请自行修改upload.py中的代码或等待作者有空时整理

## 参数

* --p 要爬取的页数,默认20
* --m 写入文件方式,默认a(追加),如 python content.py --m w 则为覆盖.
      大规模爬取推荐使用默认值,有断点续爬功能
* --u uid文件保存位置,默认uids.txt
* --c Cookie文件保存位置,默认cookies.txt
* --f 输出位置,默认result.txt
