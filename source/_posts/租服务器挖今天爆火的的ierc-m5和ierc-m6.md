---
title: 租服务器挖今天爆火的的ierc-m5和ierc-m6
permalink: ierc20m6mining/
date: 2023-11-23 12:12:52
categories: 挖矿
tags:
- ierc20-m5
- ierc20-m6
- vast4090显卡
---

ierc-m6，快去挖，刚出的，很早期，现在进度条才0.319%
进度查询(需要挂🪜)：[https://www.ierc20.com/tick/ierc-m6](https://www.ierc20.com/tick/ierc-m6)

命令行版本，别用网页版挖矿，网页版要导入私钥，不安全，要用也用新钱包搞，群里已经有小伙伴钱包被盗了、、

另外，家里的电脑性能不行，挖不了
阿里云，腾讯云翻不了qiang，下载不了挖矿代码，直接用国外租服务器、显卡的网站吧，支持虚拟货币或者小狐狸充值，很方便

1. 注册vast网站：[https://cloud.vast.ai](https://cloud.vast.ai/?ref_id=88254)
2. 注册好，充值，租机器看这里：[https://heiyetouzi.xyz/minequainetwork/#toc-heading-15](https://heiyetouzi.xyz/minequainetwork/#toc-heading-15)，直接看第三部分——GPU显卡挖矿机器配置，其他不用看。
租便宜的RTX 3080， RTX3090就可以了，没必要上RTX4090，一小时大概$0.15左右，
3. 机器租好后，点击左侧INSTANXES，图这里的open(或者connecting)打开命令行窗口，
![](https://ac63e02.webp.li/ierc20m6-001.png)
![](https://ac63e02.webp.li/ierc20m6-002.png)


4. 依次执行下面命令安装挖矿程序：
```
apt update && apt install nodejs npm vim -y
npm install n -g
n stable
hash -r
node -v 
git clone https://github.com/IErcOrg/ierc-miner-js
cd ierc-miner-js
npm i -g yarn
yarn install
```

5. 修改tokens.json
执行命令 `vim tokens.json `打开文件，清空原有内容，将如下内容粘贴进去，保存，退出
```
{
  "ierc-m4": {
    "workc": "0x0000",
    "amt": "1000"
  },
  "ierc-m5": {
    "workc": "0x00000",
    "amt": "1000"
  },
  "ierc-m6": {
    "workc": "0x000000",
    "amt": "1000"
  }
}
```

6. 安装完毕之后就可以执行挖矿命令了。

```
yarn cli wallet --set  你的ETH钱包私钥
yarn cli mine ierc-m6 --account  你的ETH钱包地址 
```
![](https://gcore.jsdelivr.net/gh/btcltceth/blogassets@v0.2.26/b/img/ierc20m6-003.png)


挖到了m6币到https://www.ierc20.com/tick/ierc-m6  (需要挂🪜)能看到，可以直接交易，1个能卖10u
机器不够可以多租几台，冲》》》

![](https://ac63e02.webp.li/ierc20m6-004.png)
![](https://ac63e02.webp.li/ierc20m6-005.png)

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

