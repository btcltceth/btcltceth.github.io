---
title: Python脚本批量篆刻雪崩链Avalanche龙头铭文$AVAL
permalink: python-script-avalanche-mint-AVAL
date: 2023-11-26 07:28:12
updated: 2023-11-29 22:54:21
categories: 铭文
tags:
- 铭文mint
- $AVAL
- $雪崩链AVAX
- $Avalanche

---

### 铭文介绍
Avalanche雪崩网络，铭文索引初始区块高度：37932982，打一张铭文的成本在EVM铭文系里面最高的。另外，#Aval的UTXO模型即将开放，Aval，是建设在Avalanche公链上的的加密货币铭文项目，旨在调侃那些只靠华丽白皮书和空洞承诺就能轻易估值数十亿美元并收割投资者的虚假项目。作为一个嘲讽性质的加密货币，Aval标榜自己是“最真实的虚拟乌托邦”，其价值实质上取决于投资者的幽默感和对市场夸大宣传的反思。Aval目前并不具有任何实质性的技术、团队或产品，但其存在的意义在于促进对加密货币市场的警醒，让投资者更加理性地对待各种夸大其词的项目。虽然Aval只是一个幽默讽刺的象征，但其存在意味着加密货币市场中那些不切实际的估值和虚假宣传的可笑一面
![](https://ac63e02.webp.li/arc20-aval-000.png)


### 数据格式
篆刻铭文其实就是自己往自己的wallet address发送交易，交易会上链，并在交易中附上指定的data数据(格式如下）——
```
UTF-8显示：
data:,{"p":"asc-20","op":"mint","tick":"aval","amt":"100000000"}

HEX十六进制显示：
0x646174613a2c7b2270223a226173632d3230222c226f70223a226d696e74222c227469636b223a226176616c222c22616d74223a22313030303030303030227d
```

### 如何打铭文
可以通过在wallet里自己给自己转账，转账金额设置为0，目标地址为自己的目标地址，注意要在高级里面加上上面👆🏻的铭文数据。操作一次就是打一张，效率低。
![](https://ac63e02.webp.li/arc20-aval-001.png)

### Python自动打
脚本打的方式很高效，只需要本地配置好python脚本，安装好web3依赖包就可以批量铭刻铭文。
```
pip3 install web3==5.31.1
```

执行 `vim avalMint.py`命令新打开编辑文件，输入以下代码内容，保存退出。
```
from web3 import Web3
from dotenv import load_dotenv
import os,time

private_key = '填你wallet的private key'
address = '填你wallet的address'
rpc_url = "https://avax.meowrpc.com" # 去https://chainlist.org/chain/43114 找响应快的rpc server
web3 = Web3(Web3.HTTPProvider(rpc_url))
print(web3.isConnected()) 
print(Web3.fromWei(web3.eth.getBalance(address),'ether')) 
c=0
while True:
    nonce = web3.eth.get_transaction_count(address)
    gas_price = int(web3.eth.gas_price*1.1)
    tx = {
        'nonce': nonce,
        'chainId': 43114,
        'to': address, 
        'from':address,
        'data':'0x646174613a2c7b2270223a226173632d3230222c226f70223a226d696e74222c227469636b223a226176616c222c22616d74223a22313030303030303030227d', # mint 16进制数据
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
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=10)
        if receipt.status == 1:
            c = c+1
            print("%s Mint Success!" %c)
            continue
        else:
            continue
    except Exception as e:
        print(e)

```

记得先替换程序开头的private_key和address两个为你自己的钱包。钱包申请方法使用文章末尾OKX Web3钱包。然后，打开终端，执行 `python3 avalMint.py`命令开始打铭文：
![](https://ac63e02.webp.li/arc20-aval-002.png)

### 链上交易查询
查询可以在[avascan](https://avascan.info/)，输入交易哈希或者你的wallet address，就可以查询到有没有成功上链。
![](https://ac63e02.webp.li/arc20-aval-004.png)


### dune进度查询
通过社区[dune面板](https://dune.com/1999eth/aval)可以查看当前铭文打的总体进度，可以输入你的wallet address，查看自己打了多少张。
![](https://ac63e02.webp.li/arc20-aval-003.png)


### 钱包wallet地址管理
可以使用TP钱包，不过我建议直接使用[OKX](https://www.chouyi.kim/zh-hans/join/76527935 )的Web3钱包进行跨链获取Gas，铭文铭刻比别人快一些。[OKX](https://www.chouyi.kim/zh-hans/join/76527935 )的Web3钱包支持60+主流的公链，也提供多链交易，主要是主要提币不用等，完全T+0。
注册后登录APP，点击顶部Web3钱包——接收——搜索”AVAX"，点开，复制找到它的地址，从交易所充值avax到这个地址，就可以开始篆刻铭文，篆刻铭文是需要消耗Avax的。
![](https://ac63e02.webp.li/arc20-aval-005.png)

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
