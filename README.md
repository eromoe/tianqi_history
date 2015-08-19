tianqi_history - a crawler for lishi.tianqi.com using scrapy

注册这么久一直都没有贡献什么代码。。。个人站点代码肯定是不想公开。。。
所以只能开这种东西了，希望能帮到人 ~ ^_^ ~


爬取lishi.tianqi.com的数据

#基本用法

基于python scrapy

需要安装相关包
pip install -r requirements.txt 

配置文件：
tianqi_history/settings.py

命令:
scrapy crawl weather 

想要ctrl-c 停止， 然后恢复爬虫，使用如下命令
scrapy crawl weather -s JOBDIR=data

注意 2次ctrl-c 强制停止后 无法恢复,需要删除 data目录
