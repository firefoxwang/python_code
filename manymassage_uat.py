#coding:utf-8


import pymysql

def message():
    # print 'input number 15151863768 .'
    a = 50
    conn=pymysql.connect(host='99.48.66.40',user='root',passwd='1qaz@WSX',db='me_notification_uat',charset='utf8')
    #uat环境中的，sit环境的ip我不知道。
    cur=conn.cursor()
    cur.execute("SELECT content,createtime from SMS_HISTORY where phoneNo ='15151863768' ORDER BY createTime desc ")
    #修改一下phoneno
    for i in cur:
        a -= 1
        if a >= 0 :
            print a ,i[0],i[1]
         
          
   
    cur.close()
    conn.close()               
if __name__ == "__main__":
    message()
