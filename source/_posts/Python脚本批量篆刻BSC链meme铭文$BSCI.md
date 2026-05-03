---
title: Python脚本批量篆刻BSC链meme铭文$BSCI
permalink: bsc20-bsci/
date: 2023-12-07 09:38:02
updated: 2023-12-07 11:34:21
categories: 铭文
tags:
- 铭文mint
- $BSCI
- $BNB
---

> 作者 黑叶(black leaf)，币圈从业13年，早年活跃在微博，雪球，入场比大多数KOL都早。巅峰持仓200枚BTC，见过账户七位数归零，也见过一夜暴富。LUNA崩盘那晚没睡，312那天没跑。亏过，赚过，活下来了。现在研究怎么让你也活下来。加密/量化/合约/Web3撸毛/港美股。

### 铭文介绍
前有bnbs造富效应，BSC铭文又fomo了！也不知道谁在币安链上部署了一个$bsci 铭文，今天上午开始打的，我起来就参战了，把币安链都干崩了，现在币安交易所提币都提不出来，既然这样我也跟着一起卷一卷吧！

### 数据格式
篆刻铭文其实就是自己往自己的wallet address发送交易，交易会上链，并在交易中附上指定的data数据(格式如下）——
```
UTF-8显示：
data:,{"p":"bsc-20","op":"mint","tick":"bsci","amt":"1000"}

HEX十六进制显示：
0x646174613a2c7b2270223a226273632d3230222c226f70223a226d696e74222c227469636b223a2262736369222c22616d74223a2231303030227d
```

### 如何打铭文
常规打法是一张一张打，在[evm.ink](https://evm.ink/tokens?searchTick=bsci)官网链接钱包，点击“Mint Now", 不过这样手搓太慢了。
![](https://ac63e02.webp.li/bsc20-bsci-001.png)

### Python脚本
脚本打的方式很高效，只需要本地配置好python脚本，安装好web3依赖包就可以批量铭刻铭文。
```
pip3 install web3==5.31.1
```

执行 `vim bsciMint.py`命令新打开编辑文件，输入以下代码内容，保存退出。
```
from web3 import Web3
from dotenv import load_dotenv
import os,time
load_dotenv()

private_key = '填你wallet的private key'
address = '填你wallet的address'
rpc_url = "https://binance.llamarpc.com" # 去https://chainlist.org/chain/56这里找响应快的rpc server，替换到这里

web3 = Web3(Web3.HTTPProvider(rpc_url))
print(web3.isConnected()) 
print(Web3.fromWei(web3.eth.getBalance(address),'ether')) 
c=0

while True:
    nonce = web3.eth.get_transaction_count(address)
    tx = {
        'nonce': nonce,
        'chainId': 56,
        'to': address, 
        'from':address,
        'data':'0x646174613a2c7b2270223a226273632d3230222c226f70223a226d696e74222c227469636b223a2262736369222c22616d74223a2231303030227d', #mint 16进制数据
        'gasPrice': int(web3.eth.gas_price * 1.5),
        'value': Web3.toWei(0, 'ether') 
    }
    try:
        gas = web3.eth.estimate_gas(tx) 
        tx['gas'] = gas 
        print(tx)
        signed_tx = web3.eth.account.sign_transaction(tx,private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(web3.toHex(tx_hash))
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            c = c+1
            print("%s Mint Success!" %c)
            continue
        else:
            continue
    except Exception as e:
        print(e)
```

记得先替换程序开头的private_key和address两个为你自己的钱包。钱包申请方法使用文章末尾OKX Web3钱包。然后，打开终端，执行 `python3 bsciMint.py`命令开始打铭文：
![](https://ac63e02.webp.li/bsc20-bsci-002.png)

### 链上交易查询
查询可以在[bscscan](https://bscscan.com/txs)，输入交易哈希或者你的wallet address，就可以查询到有没有成功上链。
![](https://ac63e02.webp.li/bsc20-bsci-003.png)


### dune进度查询
通过社区[dune面板](https://dune.com/qihai613/bsci)可以查看当前铭文打的总体进度，可以输入你的wallet address，查看自己打了多少张。
![](https://ac63e02.webp.li/bsc20-bsci-004.png)


### 钱包wallet地址管理
可以使用TP钱包，不过我建议直接使用[OKX](https://www.oucnyi.net/zh-hans/join/18639032 )的Web3钱包进行跨链获取Gas，铭文铭刻比别人快一些。[OKX](https://www.oucnyi.net/zh-hans/join/18639032 )的Web3钱包支持60+主流的公链，也提供多链交易，主要是主要提币不用等，完全T+0。
注册账号后，登录APP，点击顶部Web3钱包——接收——搜索”BNB Chain"网络， 找到它的地址，返回到交易所界面购买充值BNB到这个地址，就可以开始篆刻铭文，篆刻铭文是需要消耗BNB的。
![](https://ac63e02.webp.li/bsc20-bsci-005.png)

### 解决国内无法访问欧易OKX交易所的问题
许多交易所的原始域名可能会被列入限制名单，或者由于服务器位于海外，访问速度受到影响。对于普通用户来说，这种情况往往让人感到无从下手，甚至怀疑是否是交易所本身出了问题。实际上，这更多是网络环境造成的，而非平台本身的服务中断。为了应对这种情况，欧易，币安等交易所通常会定期更新备用域名，确保用户能够通过替代地址继续访问官网。

链接点不开？试下国内其他镜像线路！👉🏻 [欧易OKX国内备用域名线路免翻墙免代理](https://vlink.cc/okxcn)

[![](https://307e939.webp.li/20250812124552161.png)](https://vlink.cc/okxcn)


- 1. 欧易OKX备用域名 [海外欧易OKX-要翻墙](https://www.okx.com/zh-hans/join/18639032) 或者 [备用网址](https://www.oucnyi.net/zh-hans/join/18639032) 
- 2. 币安 Binance 备用域名 [币安（Binance)](https://binanceuz.co/zh-CN/register?ref=36457687)
- 3. Bitget 备用域名[Bitget](https://www.glassgs.com/zh-CN/referral/register?from=referral&clacCode=VRNEYUTR)
- 4. Bybit 备用域名[Bybit/Bybitglobal](https://www.bybitglobal.com/zh-MY/invite/?ref=VMKORMM)
- 5. 火币 HTX 备用域名 [火币（Huobi/HTX）](https://www.htx.com/invite/zh-cn/1f?invite_code=whf45223)
- 6. 芝麻 Gate 备用域名 [Gate.io（芝麻开门）](https://www.gateex.cc/zh/signup?ref_type=103&ref=A1ERAQ)

### 相关阅读
[2026中国十大虚拟币交易平台最新排名出来了🔥【值得收藏】](https://heiyetouzi.xyz/top-10-exchanges/)

如果您觉得我的文章写得不错，对您有帮助，不妨点击文末给黑叶哥打赏一杯咖啡☕️，感谢！
