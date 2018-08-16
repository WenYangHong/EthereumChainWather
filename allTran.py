from web3 import Web3, HTTPProvider
import pymysql
# web3 = Web3(HTTPProvider('http://192.168.0.194:8545'))
web3 = Web3(HTTPProvider('http://localhost:8545'))

from all import Web3Tranaction

Web3Tranaction = Web3Tranaction()

print(Web3Tranaction.con_db(5769111))

# data = Web3Tranaction.getBlock(5728426)
# print(data)

# transaction = self.web3.eth.getBlock(i, full_transactions=True)
# 符合要求的账号
# address = self.getAllAddress()
# 获取每一个区块中的交易数据


