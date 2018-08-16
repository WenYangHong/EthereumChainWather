from flask import Flask,render_template,request
from web3 import Web3, HTTPProvider
import pymysql
import json
import demjson
import flask_restful
app = Flask(__name__)
api = flask_restful.Api(app)
class ERC20():

    @app.route('/')
    # 查询单个数据的余额
    def getBalance():
        # 获取查询的地址
        address = request.args.get('address')
        query = "SELECT * FROM transactions WHERE address = %s"
        # db = pymysql.connect("localhost", "root", "root", "test")
        db = pymysql.connect("localhost", "root", "Coins123", "test")
        cursor = db.cursor()
        cursor.execute(query, address)
        balance = cursor.fetchone()
        if balance:
            return json.dumps({"code":200,"data":float(balance[2]),"msg":"获取数据成功"})
        else:
            return json.dumps({"code":200,"data":"","msg":"数据为空"})




if __name__ == '__main__':
    app.run()
