---
title: 贡献python科学家脚本--煞笔opbn项目方
permalink: opbn-python/
date: 2023-12-28 14:18:02
updated: 2023-12-28 14:24:21
categories: 铭文
tags:
- 铭文mint
- $OPBN
- $OPBNB
---

### 规则
煞笔opbn项目方，煞笔规则，一个地址只能打100次。

### 批量生成钱包地址
```
from eth_account import Account, messages
from eth_account.hdaccount import Mnemonic

def generate_opbnb_wallets(num_wallets=10):
    wallets = []
    for _ in range(num_wallets):
        account = Account.create()
        address = account.address
        private_key = account.privateKey.hex()
        
        # Generate mnemonic
        mnemonic = Mnemonic().to_mnemonic(account.key)

        wallet_info = {
            'address': address,
            'private_key': private_key,
            'mnemonic': mnemonic
        }
        wallets.append(wallet_info)

    return wallets

if __name__ == "__main__":
    num_wallets = 10
    opbnb_wallets = generate_opbnb_wallets(num_wallets)
    target_addresses = []
    for i, wallet in enumerate(opbnb_wallets, start=1):
        target_addresses.append(wallet['address'])
        print(f"{wallet['address']}")
        print(f"{wallet['private_key']}")
        print(f"{wallet['mnemonic']}")
   
    print(f"{target_addresses}")
```

### 批量转账
下面程序中，sender_address和private_key是你的发送BNB的地址。上一步生成的地址，拷贝，放到target_addresses数组里，每个地址转0.01BNB，可以自行修改，
```
from web3 import Web3
from web3.middleware import geth_poa_middleware

rpc_url = ""
web3 = Web3(Web3.HTTPProvider(rpc_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

sender_address = ""
private_key = ""

target_addresses = ['']

amount_to_send = Web3.toWei(0.01, 'ether')

def build_transaction(to_address):
    transaction = {
        'to': web3.toChecksumAddress(to_address),
        'value': amount_to_send,
        'gas': 21000,
        'gasPrice': int(web3.eth.gas_price*1.0),  
        'nonce': web3.eth.getTransactionCount(sender_address),
        'chainId': 204,  
    }
    return transaction

def send_transaction(transaction, private_key):
    signed_transaction = web3.eth.account.signTransaction(transaction, private_key)
    transaction_hash = web3.eth.sendRawTransaction(signed_transaction.rawTransaction)
    return transaction_hash

for target_address in target_addresses:
    transaction = build_transaction(target_address)
    transaction_hash = send_transaction(transaction, private_key)
    receipt = web3.eth.wait_for_transaction_receipt(transaction_hash, timeout=120)
    print(f"Transaction sent to {target_address}. Transaction Hash: {web3.toHex(transaction_hash)}")
    if receipt.status == 1:
        print(f"successfully sent to {target_address}")
```

### 打铭文

按照项目方的煞笔规则，每个地址可以打100次铭文，打超的部分作废，你有10个地址的话，就起10个程序跑。
```
from web3 import Web3
from dotenv import load_dotenv
import os,time
load_dotenv()

private_key = '填你wallet的private key'
address = '填你wallet的address'
rpc_url = "https://1rpc.io/opbnb"
web3 = Web3(Web3.HTTPProvider(rpc_url))
address = Web3.toChecksumAddress(address)
print(web3.isConnected()) 
print(Web3.fromWei(web3.eth.get_balance(address),'ether')) 
c=0
while True:
    nonce = web3.eth.get_transaction_count(address)
    gas_price = int(web3.eth.gas_price*1.5)
    tx = {
        'nonce': nonce,
        'chainId': 204,
        'to': Web3.toChecksumAddress("0x83b978cf73ee1d571b1a2550c5570861285af337"), 
        'from':address,
        'data':'0x646174613a6170706c69636174696f6e2f6a736f6e2c7b2270223a226f70627263222c226f70223a226d696e74222c227469636b223a226f70626e227d', #mint 16进制数据
        'gasPrice': gas_price,
        'value': Web3.toWei(0, 'ether') 
    }
    try:
        gas = web3.eth.estimate_gas(tx) 
        tx['gas'] = gas 
        print(tx)
        signed_tx = web3.eth.account.sign_transaction(tx,private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(web3.toHex(tx_hash))
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        if receipt.status == 1:
            if c > 100:
                sys.exit()
            c = c+1
            time.sleep(20) # 可以自行修改
            print("%s Mint Success!" %c)
            continue
        else:
            continue
    except Exception as e:
        print(e)
```

### 私人RPC节点
不用花钱买，免费注册, 有http请求额度，不过够用了。  注册地址：[https://nodereal.io](https://nodereal.io/invite/43259864-4e86-498a-9843-712931dcae9a)，注册后，选opbnb链，会生成您专属的opbnb链RPC链接，替换到上面👆🏻程序中的rpc_url即可

### 批量归集
等opbn出转账功能了，再补上。

### 解决国内无法访问欧易OKX交易所的问题
许多交易所的原始域名可能会被列入限制名单，或者由于服务器位于海外，访问速度受到影响。对于普通用户来说，这种情况往往让人感到无从下手，甚至怀疑是否是交易所本身出了问题。实际上，这更多是网络环境造成的，而非平台本身的服务中断。为了应对这种情况，欧易，币安等交易所通常会定期更新备用域名，确保用户能够通过替代地址继续访问官网。

链接点不开？试下国内其他镜像线路！👉🏻 [欧易OKX国内备用域名线路免翻墙免代理](https://vlink.cc/okxcn)

[![](https://307e939.webp.li/20250812124552161.png)](https://vlink.cc/okxcn)


- 1. 欧易OKX备用域名 [海外欧易OKX-要翻墙](https://www.okx.com/zh-hans/join/76527935) 或者 [备用网址](https://www.chouyi.kim/zh-hans/join/76527935) 
- 2. 币安 Binance 备用域名 [币安（Binance)](https://binanceuz.co/zh-CN/register?ref=36457687)
- 3. Bitget 备用域名[Bitget](https://www.glassgs.com/zh-CN/referral/register?from=referral&clacCode=VRNEYUTR)
- 4. Bybit 备用域名[Bybit/Bybitglobal](https://www.bybitglobal.com/zh-MY/invite/?ref=VMKORMM)
- 5. 火币 HTX 备用域名 [火币（Huobi/HTX）](https://www.htx.com/invite/zh-cn/1f?invite_code=whf45223)
- 6. 芝麻 Gate 备用域名 [Gate.io（芝麻开门）](https://www.gateex.cc/zh/signup?ref_type=103&ref=A1ERAQ)

### 相关阅读
[2025中国十大虚拟币交易平台最新排名出来了🔥【值得收藏】](https://btc8848.com/top-10-exchanges/)


###  大家都在搜
国内购买比特币，depin小草挂机, taker挖矿, taker钻石, 小草grass空投怎么领, 炒币交易所，okx下载注册，国内okx充值，币安App注册，币安App下载, 币安平台买币教程，币安注册，bianace撸空投注册，币安苹果手机下载，总统币怎么买，狗狗币怎么买，人民币购买比特币，欧易 怎么下载，web3撸毛, web3零撸，bitget大陆下载注册，欧易护照注册，欧易下载,币安下载,炒币副业,欧易合约, 欧易OKX如何充值人民币, 欧易怎么充值, NFT钱包怎么弄, 火币如何充值人民币, 币圈新手入门教程, btc8848.com, 炒合约Tony心法，合约杠杆bit浪浪，Defi挖矿，币圈撸毛，币圈空投还能玩吗，做合约爆仓怎么办，欧易币安货币怎么买总统币，欧易币安以太坊怎么买， Defi质押挖矿怎么玩, NFT还能玩吗, we3空投撸毛, 币圈web3零撸怎么玩, 铭文怎么打, 符文怎么打, 币圈小白入门, 如何炒币, 炒币挣钱吗, 币圈新手教程btc8848.com, 炒币赚钱吗, 什么是合约杠杆, Defi挖矿, 币圈撸毛怎么玩, 欧易okx空投, 节点质押, 爆仓, 财富自由, 黑夜投资heiyetouzi.xyz

如果您觉得我的文章写得不错，对您有帮助，不妨点击文末给黑叶哥打赏一杯咖啡☕️，感谢！
