1.功能说明：爬取豆瓣电影（movie.douban.com）信息。
 
2.爬取页面：

2.1 按热度排序电影  

链接：https://movie.douban.com/explore#!type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0

2.2 按时间排序电影

链接：https://movie.douban.com/explore#!type=movie&tag=%E7%83%AD%E9%97%A8&sort=time&page_limit=20&page_start=0

2.3 所有城市正在上映的电影信息 

链接：https://movie.douban.com/cinema/nowplaying/chengdu/

2.4 全部即将上映的电影信息

链接：https://movie.douban.com/coming

3.缺陷说明：

3.1 未行进URL过滤，仅在进行数据库写入时检查是否重复。

3.2 未做断点续传，重新运行后会在进行数据库写入时检查是否重复。

--------------------------------------------------------------------------------

4.运行说明：

4.1 初始化数据库，输入帐号密码后进入mysql，

输入以下命令

source <init.sql 所在路径>

source <doubanmovie.sql 所在路径>


4.2 直接运行start.py 即可

--------------------------------------------------------------------------------
5.程序说明：

5.1 start.py

整合四个爬虫程序，并无限循环运行，记录轮次，持续运行程序

5.2 settings.py

设置避免服务器封爬虫的手段:

DOWNLOAD_DELAY = 3            #延迟3s下载

COOKIES_ENABLED = False      #禁用cookies

5.3 pipelines.py

导入pymysql.cursors库，使用pymysql.connect链接数据库。

用execute将字符串转换成命令，将数据插入数据库
最后以commit()提交


5.4 其他spider文件，
已经代码中充分注释，
再此不在进行过多描述。
