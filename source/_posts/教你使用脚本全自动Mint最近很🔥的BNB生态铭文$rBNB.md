---
title: 教你使用脚本全自动Mint最近很🔥的BNB生态铭文$rBNB
permalink: rbnb-mint/
date: 2024-01-17 15:23:23
updated: 2024-01-17 21:15:22
categories:  挖矿
tags:
- $rBNB
- $rETH
- 铭文
- 挖矿
- 零撸
---

$rBNB是[rETH](https://bnb.reth.cc/)生态系统的一部分，致力于开发与EVM 1664 兼容的多链扩展网络，该生态系统目前已经发行了三种铸造的代币：rETH、rARB 和 rBNB。根据 rETH 官网数据，BNB生态铭文$rBNB的铸造地址数量超过了20万个，总铸造量也已经超过了6000万个。$rBNB是基于 POW 机制铸造的（0 Gas 费），总供应量为 2.1 亿。

## 官网手动Mint
官网右上角连接wallet，然后点击"Mint"免费开始Mint，当前的进度大概20.3%，当前的难度是6个9，普通家用电脑大概1分钟能挖出1个$rBNB。
![](https://ac63e02.webp.li/rbnb-001.png)

## 脚本自动化Mint
#### vast.ai快速租服务器Mint
如果你自己没有Linux机器或者你想租用更强劲的服务器来挖，建议去[vast.io](https://cloud.vast.ai/?ref_id=88254)直接租，国内的服务器无法从github下载代码，所以选国外的vast，vast支持虚拟货币或者小狐狸充值，比某里某讯便宜很多，按小时收费，很方便。租用vast.io的方法我这里不重复了，直接参考[三、GPU显卡挖矿机器配置](https://heiyetouzi.xyz/minequainetwork/#toc-heading-15)，就看第三部分就可以，其他的不用看。注意模板选`ubuntu`,并且勾选`jupyter`。
![](https://ac63e02.webp.li/rbnb-002.png)
可以看到，按照价格升序排序，最低的服务器32核cpu(共享)不到$0.1/小时，服务器租用后预计5分钟就可以启动命令行终端，服务器价格是按照分钟算钱的，不用了记得销毁，不然扣你钱。
首先执行以下命令服务器初始设置，主要是安装node, vim等必须的软件
```
apt update && apt install nodejs npm vim -y
npm install -g n && n 21.0.0
hash -r && node -v
```
![](https://ac63e02.webp.li/rbnb-003.png)

下载脚本到服务器，并生成钱包、私钥和助记词到wallets.csv文件。
```
git clone https://github.com/godzillaas/RBNBAutoJS.git
cd RBNBAutoJS
npm install --registry=https://registry.npm.taobao.org
node walletGenerater.js  # 生成20个钱包到wallets.csv文件,可以自行修改
```
![](https://ac63e02.webp.li/rbnb-004.png)

执行以下node命令，开始自动Mint
```
node index.js
```
![](https://ac63e02.webp.li/rbnb-005.png)



#### 注意事项
1、如果官方修改了difficulty难度，记得同步修改下`config.js`里的difficulty，不然mint无效。
```
const config = {
  difficulty: '0x999999',
  tick: 'rBNB',
  walletTablePath: 'wallets.csv',
  rpcUrl: 'https://bsc-dataseed1.bnbchain.org',
}

module.exports = config
```

2、单单起1个窗口，CPU是跑不满的，这样租的服务器有点浪费，如果你想跑满CPU，可以点击`File--> New --> Terminal`多开几个窗口跑`node index.js`，尽量把CPU跑满，CPU跑了多少可以用`Top`命令查看
![](https://ac63e02.webp.li/rbnb-006.png)

3、官方的服务器经常出问题不稳定，会导致你的服务器好不容易Mint到一个$rBNB，却无法提交到服务器存档，建议你等待官方服务器稳定的时候再跑上述Mint脚本。或者如果你有些代码基础，可以在[Chatgpt](https://chatgpt-plus.github.io/)帮助下，自行修改上述git仓库的nodejs程序，比如，可以将Mint好的solution结果提前保存到文件中，等待官方服务器稳定之后再统一提交存档。这类的小需求是很容易通过Chatgpt来修改实现的，[Chatgpt](https://chatgpt-plus.github.io/)是一个很好的老师。
![](https://ac63e02.webp.li/rbnb-007.png)

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

