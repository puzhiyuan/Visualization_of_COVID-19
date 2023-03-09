from flask import Flask,jsonify
from flask import render_template
import utils
from jieba.analyse import extract_tags


app = Flask(__name__)

@app.route("/getl1")
def getL1():
    day, confirm_add, suspect_add = [], [], []
    for a, b, c in utils.get_l1_data():
        day.append(a.strftime("%m-%d"))  # a是datatime类型
        confirm_add.append(b)
        suspect_add.append(c)
    return jsonify({"day": day, "confirm_add": confirm_add, "suspect_add": suspect_add})
    

@app.route("/getm1")
def getM1():
    res = []
    tup = utils.get_m1_data()
    return jsonify({"confirm": int(tup[0]),"confirm_now": int(tup[1]),"heal": int(tup[2]),"dead": int(tup[3]),})

@app.route("/getm2")
def getM2():
    res = []
    for tup in utils.get_m2_data():
        res.append({"name": tup[0], "value": int(tup[1])})
    return jsonify({"data":res})



@app.route("/getr1")
def getR1():
    data = utils.get_r1_data()
    city = []
    confirm = []
    for k,v in data:
        city.append(k)
        confirm.append(int(v))
    return jsonify({"city": city, "confirm": confirm})


@app.route("/getl2")
def getL2():
    data = utils.get_l2_data()
    # end_update_time, province, city, address, type
    details = []
    risk = []
    end_update_time = data[0][0]
    for a,b,c,d,e in data:
        risk.append(e)
        details.append(f"{b}\t{c}\t{d}")
    return jsonify({"update_time": end_update_time, "details": details, "risk": risk})

@app.route("/getr2")
def getR2():
    data = utils.get_r2_data()
    provinceName = []
    confirmedCount = []
    deadCount = []
    for a,b,c in data:
        provinceName.append(a)
        confirmedCount.append(int(b))
        deadCount.append(int(c))
    return jsonify({"provinceName": provinceName, "confirmedCount": confirmedCount, "deadCount": deadCount})




@app.route('/')
def index():
    return render_template("main.html")

if __name__ == '__main__':
    app.run()
    