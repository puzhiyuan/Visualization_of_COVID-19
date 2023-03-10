import requests
import pymysql
import time
import json
import traceback
from bs4 import BeautifulSoup
import re


def get_conn():
    """
    :return: 连接，游标
    """
    # 创建连接
    conn = pymysql.connect(host="127.0.0.1",
                           user="root",
                           password="PZY0404.",
                           db="cov",
                           charset="utf8")
    # 创建游标
    cursor = conn.cursor()# 执行完毕返回的结果集默认以元组显示
    return conn, cursor

def close_conn(conn, cursor):
    cursor.close()
    conn.close()

def get_tencent_data():
    """
    :return: 返回历史数据和当日详细数据
    """
    url_det = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=diseaseh5Shelf'
    url_his = "https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,nowConfirmStatis,provinceCompare"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    }
    r_det = requests.get(url_det, headers)
    r_his = requests.get(url_his, headers)
    res_det = json.loads(r_det.text)  # json字符串转字典
    res_his = json.loads(r_his.text)
    data_det = res_det['data']['diseaseh5Shelf']
    data_his = res_his['data']

    history = {}  # 历史数据
    for i in data_his["chinaDayList"]:
        ds = i["y"]+"."+i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")
        ds = time.strftime("%Y-%m-%d", tup)  # 改变时间格式,不然插入数据库会报错，数据库是datetime类型
        confirm = i["confirm"]
        confirm_now = i["nowConfirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        history[ds] = {"confirm": confirm,"confirm_now":confirm_now, "suspect": suspect, "heal": heal, "dead": dead}
    for i in data_his["chinaDayAddList"]:
        ds = i["y"]+"."+i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")
        ds = time.strftime("%Y-%m-%d", tup)
        confirm_add = i["confirm"]
        suspect_add = i["suspect"]
        heal_add = i["heal"]
        dead_add = i["dead"]
        history[ds].update({"confirm_add": confirm_add, "suspect_add": suspect_add, "heal_add": heal_add, "dead_add": dead_add})

    details = []  # 当日详细数据
    update_time = data_det["lastUpdateTime"]
    data_country = data_det["areaTree"]  # list 之前有25个国家,现在只有中国
    data_province = data_country[0]["children"]  # 中国各省
    for pro_infos in data_province:
        province = pro_infos["name"]  # 省名
        for city_infos in pro_infos["children"]:
            city = city_infos["name"] #城市名
            confirm = city_infos["total"]["confirm"] #l累计确诊
            confirm_add = city_infos["today"]["confirm"] #新增确诊
            confirm_now = city_infos["total"]["nowConfirm"] #现有确诊
            heal = city_infos["total"]["heal"] #累计治愈
            dead = city_infos["total"]["dead"] #累计死亡
            details.append([update_time, province, city, confirm, confirm_add,confirm_now, heal, dead])
    return history, details

def update_details():
    """
    更新 details 表
    :return:
    """
    cursor = None
    conn = None
    try:
        li = get_tencent_data()[1]  #  0 是历史数据字典,1 最新详细数据列表
        conn, cursor = get_conn()
        sql = "insert into details(update_time,province,city,confirm,confirm_add,confirm_now,heal,dead) " \
              "values(%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query = 'select %s=(select update_time from details order by id desc limit 1)' #对比当前最大时间戳
        cursor.execute(sql_query,li[0][0])
        if not cursor.fetchone()[0]:
            print(f"{time.asctime()}开始更新最新数据")
            for item in li:
                cursor.execute(sql, item)
            conn.commit()  # 提交事务 update delete insert操作
            print(f"{time.asctime()}更新最新数据完毕")
        else:
            print(f"{time.asctime()}已是最新数据！")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

def update_history():
    """
    更新历史数据
    :return:
    """
    cursor = None
    conn = None
    try:
        dic = get_tencent_data()[0]  #  0 是历史数据字典,1 最新详细数据列表
        print(f"{time.asctime()}开始更新历史数据")
        conn, cursor = get_conn()
        sql = "insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query = "select confirm from history where ds=%s"
        for k, v in dic.items():
            # item 格式 {'2020-01-13': {'confirm': 41, 'suspect': 0, 'heal': 0, 'dead': 1}
            if not cursor.execute(sql_query, k):  #如果当天数据不存在，才写入
                cursor.execute(sql, [k, v.get("confirm"), v.get("confirm_add"),v.get("confirm_now"),
                                     v.get("suspect"),v.get("suspect_add"), v.get("heal"),
                                     v.get("heal_add"),v.get("dead"), v.get("dead_add")])
        conn.commit()  # 提交事务 update delete insert操作
        print(f"{time.asctime()}历史数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

def update_risk_area():
    
    #请求参数
    nowTime = int(time.time()/60)
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Access-Control-Request-Headers': 'content-type',
        'Access-Control-Request-Method': 'GET',
        'Connection': 'keep-alive',
        'Host': 'file1.dxycdn.com',
        'Origin': 'https://ncov.dxy.cn',
        'Referer': 'https://ncov.dxy.cn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    url = "https://file1.dxycdn.com/2021/0202/196/1680100273140422643-135.json?t=" + str(nowTime)
    res = requests.get(url=url, headers=headers).text
    conn, cursor = get_conn()
    print(f"{time.asctime()}开始更新风险地区数据")
    resJson = json.loads(res)
    if resJson["code"] == "success":
        # resJson["data"][0]  #高风险地区
        # resJson["data"][1]  #中风险地区
        # print(resJson["data"][0]["dangerPros"][0])  每个省的数据

        #高风险地区
        for item in resJson["data"][0]["dangerPros"]:
            provinceName = str(item["provinceName"])
            for itemArea in item["dangerAreas"]:
                allName = provinceName + " " + str(itemArea["cityName"]) + " " + str(itemArea["areaName"] + "\r")
                sql = "insert into risk_area(end_update_time, province, city, address, type) values(\"" + time.strftime("%Y年%m月%d日 %H:%M:%S", time.localtime()) + "\"," + "\"" + provinceName + "\",\"" + itemArea["cityName"] +  "\",\"" + itemArea["areaName"] + "\"," + "\"中风险\")"
                cursor.execute(sql)
                # 提交到数据库执行
                conn.commit()

        #中风险地区
        for item in resJson["data"][1]["dangerPros"]:
            provinceName = str(item["provinceName"])
            for itemArea in item["dangerAreas"]:
                sql = "insert into risk_area(end_update_time, province, city, address, type) values(\"" + time.strftime("%Y年%m月%d日 %H:%M:%S", time.localtime()) + "\"," + "\"" + provinceName + "\",\"" + itemArea["cityName"] +  "\",\"" + itemArea["areaName"] + "\"," + "\"高风险\")"
                cursor.execute(sql)
                # 提交到数据库执行
                conn.commit()
    close_conn(conn, cursor)
    print(f"{time.asctime()}风险地区数据更新完毕")


def get_world_data():
    conn, cursor = get_conn()
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia'
    r = requests.get(url, headers=headers)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'html.parser')
    get_data1 = soup.find_all('script', attrs={'id': 'getListByCountryTypeService2true'})
    # print(get_data1)
    get_data2 = get_data1[0].string
    # print(get_data2)
    RE = re.compile('\[.*\]')
    data_clear = re.findall(RE, get_data2)
    data_clear[0]
    print(f"{time.asctime()}开始更新全球疫情数据")
    data_json = json.loads(data_clear[0])  # 将字典格式转换换为json格式
    for i in data_json:
            provinceName = str(i["provinceName"])
            confirmedCount = str(i["confirmedCount"])
            deadCount = str(i["deadCount"])
            sql = "insert into world_data(provinceName, confirmedCount, deadCount, end_update_time) values(\""+ provinceName + "\",\"" + confirmedCount +  "\",\"" + deadCount + "\",\"" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\")"
            cursor.execute(sql)
            conn.commit()
    close_conn(conn=conn, cursor=cursor)
    print(f"{time.asctime()}全球疫情数据更新完毕")



if __name__ == "__main__":
    update_history()
    update_details()
    update_risk_area()
    get_world_data()
    
