---
title: Python脚本批量篆刻XT交易所XT Smart chain链上的首个铭文$xsci
permalink: xtmint/
date: 2023-12-23 22:08:00
updated: 2023-12-23 22:19:21
categories: 铭文
tags:
- 铭文mint
- $XSCI
- XT交易所
- $Python铭文
---

> 作者 黑叶(black leaf)，币圈从业13年，早年活跃在微博，雪球，入场比大多数KOL都早。巅峰持仓200枚BTC，见过账户七位数归零，也见过一夜暴富。LUNA崩盘那晚没睡，312那天没跑。亏过，赚过，活下来了。现在研究怎么让你也活下来。加密/量化/合约/Web3撸毛/港美股。


### 背景

[XT交易所](https://www.xtcore.plus/zh-CN/accounts/register?ref=3KXTQR)背靠XT交易所750万老外用户，信仰足、流量足、资金足！上线直接流动性加满！XTLauncpad升级，疯狂赋能XT，XT涨+铭文涨，正向飞轮一直涨！XT很关注铭文板块，想从铭文赛道超车进一线，拉盘XSCI是板上钉钉，倾斜的资源你无法想象！

### 手动mint
手动Mint直接在官网，当前进度是0.31%，索引没有滞后，还很早期，gas几乎忽略不计，近似免费mint，建议打了防身。官网地址：https://xscscriptions.com/tokens
![](https://ac63e02.webp.li/mint-xt-001.png)

### 购买$XT
打$XT铭文需要消耗少量XT代币，去[XT交易所](https://www.xtcore.plus/zh-CN/accounts/register?ref=3KXTQR)充值USDT购买，USDT可以从[欧易](https://chouyi.pro/cn/join/18639032)或者[币安](https://binanceuz.co/zh-CN/register?ref=36457687)提，大概10分钟到账，购买完XT，提到你自己的XT钱包，XT钱包建议用小狐狸直接添加网络，参数如下，也可以从[https://chainlist.org/chain/520](https://chainlist.org/chain/520)一键点击添加到小狐狸。
```
Network name：XT Smart Chain Mainnet
Network URL：https://datarpc4.xsc.pub
Chain ID：520
Currency symbol：XT

```


### 数据格式
篆刻铭文其实就是自己往自己的wallet address发送交易，交易会上链，并在交易中附上指定的data数据(格式如下）——
```
UTF-8显示：
data:,{"p":"xsc-20","op":"mint","tick":"xsci","amt":"10000"}

HEX十六进制显示：
0x646174613a2c7b2270223a227873632d3230222c226f70223a226d696e74222c227469636b223a2278736369222c22616d74223a223130303030227d
```


### Python脚本
脚本打的方式很高效，只需要本地配置好python脚本，安装好web3依赖包就可以批量铭刻铭文。如果你电脑上没有安装pip3，按照错误提示先安装pip3。
```
pip3 install web3==5.31.1
```

执行 `vim xsciMint.py`命令新打开编辑文件，输入以下代码内容，保存退出。

```
from web3 import Web3
from dotenv import load_dotenv
import os,time
load_dotenv()


private_key = '填你wallet的private key'
address = '填你wallet的address'
rpc_url = "https://datarpc1.xsc.pub" # 去https://chainlist.org/chain/520 找响应快的rpc server

web3 = Web3(Web3.HTTPProvider(rpc_url))
print(web3.isConnected()) 
print(Web3.fromWei(web3.eth.getBalance(address),'ether')) 
c=0
while True:
    nonce = web3.eth.get_transaction_count(address)
    gas_price = int(web3.eth.gas_price * 1.5)
    tx = {
        'nonce': nonce,
        'chainId': 520,
        'to': address, 
        'from':address,
        'data':'0x646174613a2c7b2270223a227873632d3230222c226f70223a226d696e74222c227469636b223a2278736369222c22616d74223a223130303030227d', #mint 16进制数据
        'gasPrice': gas_price,
        'value': Web3.toWei(0, 'ether') 
    }
    try:
        gas = web3.eth.estimateGas(tx) 
        tx['gas'] = gas 
        print(tx)
        signed_tx = web3.eth.account.sign_transaction(tx,private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(web3.toHex(tx_hash))
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        if receipt.status == 1:
            c = c+1
            print("%s Mint Success!" %c)
            continue
        else:
            continue
    except Exception as e:
        print(e)

```
记得先替换程序开头的private_key和address两个为你自己的钱包。钱包申请方法使用文章末尾OKX Web3钱包。
python程序编辑好后，打开电脑的终端(windows下是cmd)，执行 `python3 xsciMint.py`命令开始即可开始打铭文：
![](https://ac63e02.webp.li/mint-xt-002.png)


### 链上交易查询
查询可以在[https://xscscan.pub/](https://xscscan.pub/txs)，输入交易哈希或者你的wallet address，就可以查询到有没有成功上链。
![](https://ac63e02.webp.li/mint-xt-003.png)


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


