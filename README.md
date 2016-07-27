tianqi_history
===========

A crawler for lishi.tianqi.com using scrapy.


## English Doc:

- install

        pip install -r requirements.txt

- settings

        tianqi_history/settings.py

- run

        scrapy crawl weather

- stop, and resume

        ctrl-c
        scrapy crawl weather -s JOBDIR=data

- note

        twice ctrl-c force stop, need delete data folder

---------

## Chinese Doc


- 需要安装相关包

        pip install -r requirements.txt

- 配置文件：

        tianqi_history/settings.py

- 运行命令:

        scrapy crawl weather

- 想要ctrl-c 停止， 然后恢复爬虫，使用如下命令

        scrapy crawl weather -s JOBDIR=data

注意 2次`ctrl-c` 强制停止后 无法恢复,需要删除 data目录
