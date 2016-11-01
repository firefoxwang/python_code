# coding:utf-8
import pyodbc
def delete():
    print 'input your mobile,please'
    mobile = raw_input()
    conn = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=99.48.66.12;DATABASE=memedaidb;UID=daoqing.zha;PWD=mime@123;charset = utf-8')
    cur = conn.cursor()
    try:
        cur.execute("select member_id,wc_nickname from memedaidb.appl.a_appl where mobile = %r" % mobile)

        result = cur.fetchone()
        print 'memberid is ', result[0]
        print 'nickname is', result[1].decode('gb2312').encode('utf-8')
        memberid_int = result[0]
        memberid = str(result[0])
        nickname = result[1]
        # 这下面是我自己加的数据，应该跟c征啥的有关系
        cur.execute("select appl_no from memedaidb.appl.a_appl where member_id = %r" % memberid)
        results = cur.fetchall()
        for i in results:
            print "appl_no is", i[0]
            appl_no = str(i[0])
            cur.execute("delete from appl.A_APPL_C_EXT where APPL_NO =%r" % appl_no)  # 因为这里面有cur指针，所以for循环里面要注意


        cur.execute(
            "delete from appl.a_token where appl_no in (select appl_no from appl.a_appl where mobile=%r)" % mobile)
        cur.execute("declare @member_id int set @member_id = %d;\
                    DELETE APPL.A_APPL WHERE MEMBER_ID = @member_id \
                    DELETE APPL.A_PRECREDIT WHERE MEMBER_ID = @member_id \
                    DELETE APPL.B_A_SCORE WHERE MEMBER_ID = @member_id \
                    DELETE APPL.A_BIZ_CARD WHERE MEMBER_ID = @member_id \
                    DELETE APPL.A_CAMPUS_CARD WHERE MEMBER_ID = @member_id \
                    DELETE CRM.ACCT_MNG_MEMBER WHERE MEMBER_ID =  @member_id \
                    DELETE CRM.BANK_CARD WHERE MEMBER_ID = @member_id \
                    DELETE CRM.ID_CARD WHERE MEMBER_ID = @member_id \
                    DELETE CRM.BUREAU_FLAG WHERE MEMBER_ID = @member_id \
                    DELETE CRM.MEMBER_CLUSTER WHERE MEMBER_ID = @member_id " % memberid_int)
        cur.execute("declare @member_id int set @member_id = %d;\
                    DELETE CRM.MEMBER_IMAGE WHERE MEMBER_ID = @member_id  \
                    DELETE CRM.MEMBER_WECHAT WHERE MEMBER_ID = @member_id \
                    DELETE SECU.SECURITY_INFO WHERE MEMBER_ID = @member_id \
                    DELETE SECU.UNION_USER WHERE MEMBER_ID = @member_id \
                    DELETE LIU.USER_STEPS WHERE MEMBER_ID = @member_id \
                    DELETE LIU.USER_DAILY_INCOME WHERE MEMBER_ID = @member_id \
                    DELETE LIU.TRANSACTION_JNL WHERE MEMBER_ID = @member_id \
                    DELETE LIU.WITHDRAW WHERE MEMBER_ID = @member_id \
                    DELETE LIU.RECHARGE WHERE MEMBER_ID = @member_id \
                    DELETE LIU.USER_ACTIVITY WHERE MEMBER_ID = @member_id" % memberid_int)
        cur.execute("declare @member_id int set @member_id = %d;\
                    DELETE LIU.PRIZE WHERE MEMBER_ID = @member_id \
                    DELETE CRM.MEMBER WHERE MEMBER_ID = @member_id \
                    DELETE CRM.FRIEND_WECHAT WHERE MEMBER_ID = @member_id \
                    DELETE LIU.LC_ORDER WHERE MEMBER_ID=@member_id \
                    DELETE MKT.TICKET_ where  MEMBER_ID=@member_id \
                    DELETE LIU.LC_MEMBER_REQ_CODE  where  MEMBER_ID=@member_id \
                    DELETE LIU.LC_MEMBER_REQ_RECODE  where MEMBER_ACTIVE_ID=@member_id or MEMBER_PASSIVE_ID=@member_id \
                    DELETE LIU.LC_FEED_BACK WHERE MEMBER_ID=@member_id DELETE LIU.LC_RECHARGE \
                    where MEMBER_ID=@member_id \
                    DELETE MKT.ACTIVITY_PARTAKE_RECORD where MEMBER_ID_ACTIVE=@member_id \
                    DELETE  CRM.CONTRACT WHERE BORROWER_ID=@member_id \
                    DELETE  FSS.LOAN_REPAY_PLAN where BORROWER_ID=@member_id  \
                    DELETE  FSS.LOANS where BORROWER_ID=@member_id  \
                    DELETE  FSS.LOAN_SETTLE_APPL where BORROWER_ID=@member_id " % memberid_int)
        # 脏数据清理
        cur.execute("delete from MER.MERCHANT_APP_USER where MEMBER_ID=%r;\
                     delete from MER.MERCHANT_WECHAT_USER where MEMBER_ID=%r;\
                     delete from MSG.BATCH_MESSAGE where MEMBERID=%r;\
                     delete from PAY.PAYMENT_ORDER where MEMBER_ID=%r;\
                     delete from CRM.MEMBER where MEMBER_ID=%r;\
                     delete from CRM.ID_CARD where MEMBER_ID=%r;" % (memberid, memberid,memberid, memberid, memberid, memberid))
        cur.execute("delete from CRM.MEMBER_WECHAT where NICKNAME= %r" % nickname)
        cur.execute("delete from APPL.A_MERCHANT_ORDER where MOBILE= %r" % mobile)
        # 删除本人注册的身份证信息

        cur.execute("DELETE FROM watson.crm.INQUIRY where mobile= %r" % mobile)
        cur.execute("DELETE FROM [memedaidb].crm.MEMBER_WECHAT where NICKNAME= %r" % nickname)

        conn.commit()
        cur.close()
        conn.close()
        print 'delete  ok'
    except:
        print 'something errer happened!!!'
        conn.rollback()
        cur.close()
        conn.close()
if __name__ == "__main__":
    delete()


