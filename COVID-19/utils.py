from cgitb import text
from pickletools import string1
import pymysql

#建立连接
def getConn():
    conn = pymysql.connect(host="127.0.0.1",
                           user="root",
                           password="PZY0404.",
                           db="cov",
                           charset="utf8")
    cursor = conn.cursor()
    return conn, cursor

#断开连接
def closeConn(conn, cursor):
    cursor.close
    conn.close

#封装查询
def query(sql, *args):
    conn, cursor = getConn()
    cursor.execute(sql,args)
    res = cursor.fetchall()
    closeConn(conn, cursor)
    return res

#左上折线统计
def get_l1_data():
    sql = "select ds,confirm_add,suspect_add from history"
    res = query(sql)
    return res

#左下数据
def get_l2_data():
	sql = "select end_update_time,province,city,address,type" \
          " from risk_area " \
          "where end_update_time=(select end_update_time " \
          "from risk_area " \
          "order by end_update_time desc limit 1) "
	res = query(sql)
	return res

#中间大屏数据
def get_m1_data():
    sql = """
    SELECT total,total-heal-dead,heal,dead from (
    select sum(confirm) total, 
    (SELECT heal from history ORDER BY ds desc LIMIT 1) heal ,
      sum(dead) dead 
    from details where update_time=(
      select update_time from details order by update_time desc limit 1)
    ) d;
    """
    res = query(sql)
    return res[0]

#现有确诊
def get_m2_data():
    sql = "select province,sum(confirm_now) from details " \
        "where update_time=(select update_time from details " \
        "order by update_time desc limit 1) " \
        "group by province"
    res = query(sql)
    return res



def get_r1_data():
    sql = 'SELECT province,confirm FROM ' \
        '(select province ,sum(confirm_now) as confirm from details  ' \
        'where update_time=(select update_time from details ' \
        'order by update_time desc limit 1) ' \
        'group by province) as a ' \
        'ORDER BY confirm DESC LIMIT 5'
    res = query(sql)
    return res
    
def get_r2_data():
    sql = 'SELECT provinceName,confirmedCount, deadCount FROM world_data ORDER BY confirmedCount DESC LIMIT 10'
    res = query(sql)
    return res


if __name__ == "__main__":
    pass
    # print(get_r2_data())

