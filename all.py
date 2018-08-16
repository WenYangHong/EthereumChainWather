from web3 import Web3, HTTPProvider
import pymysql
import json
import demjson

class Web3Tranaction:
    def __init__(self):
        # self.db = pymysql.connect("localhost", "root", "root", "test")
        self.db = pymysql.connect("127.0.0.1", "root", "Coins123", "test")
        self.cursor = self.db.cursor()
        # self.web3 = Web3(HTTPProvider('http://192.168.0.194:8545'))
        self.web3 = Web3(HTTPProvider('http://localhost:8545'))

    def getTranaction(self):
        # 最新的区块号
        blockNumber = self.web3.eth.blockNumber

        # 先判断是不是最新的
        flag = self.con_db(blockNumber)
        if flag != False:
            for i in range(flag, blockNumber+1):
                transaction = self.web3.eth.getBlock(i, full_transactions=True)
                # 符合要求的账号
                address = self.getAllAddress()
                # 获取每一个区块中的交易数据
                transactionArray = transaction.transactions
                for index in range(len(transactionArray)):
                    if transactionArray[index].to in address.values():
                        Receipt = self.web3.eth.getTransactionReceipt(transactionArray[index].hash)
                        if abs(Receipt.status - 1) < 1e-8:
                            transactionValue = self.web3.fromWei(transactionArray[index].value, "ether")
                            # 查询余额
                            self.update_value(transactionArray[index].to, transactionValue)
                            # 添加流水
                            self.insertList(transactionArray[index].to, transactionArray[index]['from'],
                                            transactionValue)

    # 查询当给区块号结果
    def con_db(self,blockNumber):
        sql = "SELECT * from block WHERE id = 1"
        self.cursor.execute(sql)
        results = self.cursor.fetchone()
        if results :
            if blockNumber > results[1]:
                # 进行修改操作
                update = "UPDATE block SET blockNumber = %s  WHERE id = 1"
                try:
                    self.cursor.execute(update,blockNumber)
                    self.db.commit()
                except:
                    self.db.rollback()

                #   返回已经扫描过的最后一个区块号，从这个区块号开始扫描
                return results[1] + 1
            else:
                return False
        else:
            return False

    # 更新账号下的余额数据
    def update_value(self,address, incrementValue):
        sql = 'INSERT INTO transactions (address,total,balance) VALUES (''"' + str(address) + '"'',1,' + str(incrementValue) + ') ON DUPLICATE KEY UPDATE total = total+1 ,balance=balance+'+str(incrementValue)

        try:
            self.cursor.execute(sql)
            self.db.commit()
            # return True
        except:
            self.db.rollback()
            return False

    # 添加交易的流水
    def insertList(self,_to,_from,_value):
        sql = 'INSERT INTO transactionList (`to`,`from`,`value`) VALUES (''"' + str(_to) + '"'',''"' + str(_from) + '"'',' + str(_value) + ') '

        try:
            self.cursor.execute(sql)
            self.db.commit()
            # return True
        except:
            self.db.rollback()
            return False

    # 查询地址的余额
    def AddressBalance(self,address):
        query = "SELECT * FROM transactions WHERE address = %s"
        self.cursor.execute(query,address)
        balance = self.cursor.fetchone()
        if balance:
            return  balance[2]
        return "Search Nothing"

    # 测试用
    def getOne(self,query,param):
        self.cursor.execute(query,param)
        return self.cursor.fetchone()

    # 测试用
    def getTranactionByBlockNumber(self,blockNumber):
        # 最新的区块号
        transaction = self.web3.eth.getBlock(blockNumber, full_transactions=True)

        return transaction.transactions

    # 测试用
    def getTransactionReceipt(self,Hash):
        transaction = self.web3.eth.getTransactionReceipt(Hash)

        return transaction


    def getTranactionByHash(self):

        tranaction = self.web3.eth.getTransaction("0x04a32e617d857e55352d8204393a36d33c888b16214ee955ee2a4db29d0674ae")

        return tranaction

    # 获取所有的地址
    def getAllAddress(self):
        query = "SELECT address FROM worldaccount"
        self.cursor.execute(query)
        all = self.cursor.fetchall()
        address = {}
        for i in range(len(all)):
            address[i] = all[i][0]
        return address

    def getBlock(self,blockNumber):
        for i in range(5728420, blockNumber + 1):
            transaction = self.web3.eth.getBlock(i, full_transactions=True)
            # 符合要求的账号
            address = self.getAllAddress()
            # 获取每一个区块中的交易数据
            transactionArray = transaction.transactions
            for index in range(len(transactionArray)):
                if transactionArray[index].to in address.values():
                    transactionStatus = self.web3.toInt(hexstr=str(transactionArray[index].standardV))
                    if abs(transactionStatus - 1) < 1e-19:
                        Receipt = self.web3.eth.getTransactionReceipt(transactionArray[index].hash)
                        if abs(Receipt.status - 1) < 1e-19:
                            print(1)