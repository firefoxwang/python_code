# 教程伪代码 不运行
# coding:utf-8
import pyodbc as db1  # pyodbc教程 https://mkleehammer.github.io/pyodbc/
import pymysql as db2  # pymysql教程 http://pymysql.readthedocs.io/en/latest/


# 连接数据库

# conn1 = db1.connect("99.48.66.12", "daoqing.zha", "mime@123") 用pyodbc连接，最多一个非关键字参数，这样写会报错。
conn2 = db2.connect('99.48.66.40', 'root', '1qaz@WSX')

# 使用关键字参数连接

conn1 = db1.connect(
        'DRIVER={SQL Server};SERVER=99.48.66.12;DATABASE=memedaidb;UID=daoqing.zha;PWD=mime@123;charset = utf-8')
conn2 = db2.connect(host='99.48.66.40', user='root', passwd='1qaz@WSX', db='me_notification', charset='utf8')

# 使用字典进行连接参数的管理

config1 = {
        'driver': 'SQL Server',
        'server': '99.48.66.12',
        'database': 'memedaidb',
        'uid': 'daoqing.zha',
        'pwd': 'mime@123',
        'charset': 'utf-8'
}
conn1 = db1.connect(**config1)  # pass the config1 as keyword argument with the "**" notation.


config2 = {
        'host': '99.48.66.40',
        'user': 'root',
        'passwd': '1qaz@WSX',
        'db': 'me_notification',
        'charset': 'utf8'
}
conn2 = db2.connect(**config2)

# 如果使用事务引擎，可以设置自动提交事务，或者在每次操作完成后手动提交事务 conn.commit()
conn1.autocommit(1)  # conn1.autocommit(True)
# 使用cursor()方法获取操作游标
cursor = conn1.cursor()
# 因为该模块底层其实是调用CAPI的，所以，需要先得到当前指向数据库的指针。

# 连接完成后，开始操作数据库 一定要注意数据的格式 ！！！

try:
        # 删除单条数据
        appl_no = '2012031608'
        sql = 'delete from appl.A_APPL_C_EXT where APPL_NO =%r % appl_no'
        cursor.execute(sql)

        # 删除多条数据,查找到多条数据就用循环，一个一个的删除掉找到的数据。注意格式
        memberid = '15151863768'
        cursor.execute("select appl_no from memedaidb.appl.a_appl where member_id = %r" % memberid)
        for i in cursor:
            print "appl_no is", i[0]
            appl_no = str(i[0])
            cursor.execute("delete from appl.A_APPL_C_EXT where APPL_NO =%r" % appl_no)

        # 获取表名信息
        desc = cursor.description
        print desc

        #查询一条记录 这个最常用在cursor执行后有多条记录，但是我只想看指针指着的那一条。
        print 'fetch one record:'
        result = cursor.fetchone()
        print result

        # 查询所有记录
        # 重置游标位置，偏移量:大于0向后移动;小于0向前移动，mode默认是relative
        # relative:表示从当前所在的行开始移动; absolute:表示从第一行开始移动
        cursor.scroll(0,mode='absolute')
        results = cursor.fetchall()
        for r in results:
                print r
        # 如果没有设置自动提交事务，则这里需要手动提交一次
        conn1.commit()
except:
        # 把所以的异常列为异常，这个不太好，但是现阶段可以这么做 一般错误类型有 ValueError IOError SyntaxError
        import traceback
        traceback.print_exc() # 回溯，有错误直接打印在屏幕上。
        # 发生错误时回滚
        conn1.rollback()
finally:
        # 关闭游标连接
        cursor.close()
        # 关闭数据库连接
        conn1.close()
        conn2.close()
        print 'tutorial2 ok'
