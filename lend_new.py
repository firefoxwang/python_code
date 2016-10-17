#coding:utf-8

import pyodbc
import time


def lend():
    print 'input memberid ,please'
    memberid = raw_input()
    conn = pyodbc.connect('driver={sql server};server=99.48.66.12;database=memedaidb;uid=daoqing.zha;pwd=mime@123;use_unicode=True ')
   
    cur = conn.cursor()
    cur.execute("EXEC FSS.USP_BATCH_LOAN_PUBLISH")
   
    cur.execute("SELECT  TARGET_AMT, Target_id  FROM BID.TARGET where BORROWER_ID=%r ORDER BY TARGET_ID "%memberid)

 
    for i in cur:
        target_amt = i[0]
        target_id = i[1]
    print target_amt , "target_amt"
    print target_id  , 'target_id'
    
    int_id = int(target_id)
    
    float_amt = float(target_amt)
    
    cur.execute("EXEC BID.USP_BID_SUBMIT @INVESTOR = 255 , @TARGET_ID =%d , @BID_AMT =%.2f, @IP = '' , @BID_SOURCE = '' , @CLIENT_INFO = ''"%(int_id,float_amt))
            
    cur.execute("EXEC BID.USP_BATCH_TARGET")
   
    cur.execute("EXEC FSS.USP_BID_RESULT_BATCH_PROCESS")

    cur.execute("SELECT transfer_sn,TRANSFER_AMT FROM PAY.TRANSFER WHERE  DEAL_ID IS NULL and MEMBER_ID=%r  ORDER BY TRANS_APPLY_TIME "%memberid)
    time.sleep(2)
    print " 2s later" 
    for i in cur:
        transfer_sn = i[0]
        transfer_amt = i[1]
    print transfer_sn , 'transfer_sn'
    print transfer_amt , 'transfer_amt'

    float_amt = float(transfer_amt)
    str_amt = str(transfer_amt)

    cur.execute("EXEC FSS.USP_TRANSFER_RESULT_UPDATE    @TRANSFER_SN = %r,   @PROCESS_RESULT = '10' ,@RESULT_AMT = %.2f,  @DEALER = 'MANUL' , @DEAL_ID =%r, @DEAL_TIME = '2016-09-01 17:44:19' ,@ERROR_MSG = '' "%(transfer_sn,float_amt,str_amt))
    #print "EXEC FSS.USP_TRANSFER_RESULT_UPDATE    @TRANSFER_SN = %r,   @PROCESS_RESULT = '10' ,@RESULT_AMT = %.2f,  @DEALER = 'MANUL' , @DEAL_ID =%r, @DEAL_TIME = '2016-09-01 17:44:19' ,@ERROR_MSG = '' "%(transfer_sn,float_amt,str_amt)
    # 一直找不到错误，原来错误是因为 transfer_amt从数据库中取出来的时候是decimal('1900.00')的格式。实际上即使用python插入decimal格式也不行，插入float格式就可以的。所以从数据库中拿出来数据，全部改掉，再重新插进来
    #里面的deal_time有空改成Python获取的当前时间吧 ，有空再说
    conn.commit()
    cur.close()
    conn.close()
    print 'lend ok'

         
if __name__ == "__main__":
    lend()
