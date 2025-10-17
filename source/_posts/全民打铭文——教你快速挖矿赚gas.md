---
title: 全民打铭文——教你快速挖矿赚gas
permalink: unmineable-mine-avax/
date: 2023-12-20 19:47:47
updated: 2023-12-20 20:24:26
categories: 挖矿
tags:
- 铭文mint
- $AVAV
- unmineable
- 挖矿gas
---

最近，铭文热潮不断掀起，各大公链gas费涨上天，散户都快打不起铭文了。这其中，笑得最开心的当然是狗项目方，其次就是矿工了。
不过，钱不能都让你们这些黑心商赚去，本教程我来教您如何快速在卷gas的时候快速挖矿赚取矿工费。跟其他教程不一样的是，这篇教你的挖矿，矿工费都是每隔5分钟结算发放的，非常适合打铭文fomo的时候快速介入挖赚提，下图就是在最近大热的AVAV和Dino铭文卷高gas的时候我快速设置的挖avax结算图，可以看到是每隔5分钟发放，爽歪歪。
![](https://ac63e02.webp.li/unmineable-001.png)

先说一下，CPU也可以挖，不过一般建议显卡挖，高效不少，毕竟卷gas的时间很宝贵，时间就是金钱。

### unmineable介绍
1. 访问[unmineable](https://unmineable.com/?ref=s1va-4x9y)，部分国内地区访问不了，可以挂魔法网络访问。网站免注册免登录，在搜索框中输入你想要挖的币，这里我以时下最火的AVAX为例。
![](https://ac63e02.webp.li/unmineable-002.png)
2. 点击快速向导wizard——Basic基础模式——选择GPU显卡挖矿
![](https://ac63e02.webp.li/unmineable-003.png)
![](https://ac63e02.webp.li/unmineable-004.png)
![](https://ac63e02.webp.li/unmineable-005.png)
有适配的币种就选适配的算法，不懂的话就默认选第一个Kawpow就行
![](https://ac63e02.webp.li/unmineable-006-1.png)
选择币种"AVAX"（如果是挖其他币，就选对应币)，填入你钱包地址，一路点击Next-Next
![](https://ac63e02.webp.li/unmineable-006.png)
![](https://ac63e02.webp.li/unmineable-007.png)
![](https://ac63e02.webp.li/unmineable-008.png)

这里，网站自动给你生成了windows和linux的挖矿命令，你直接就可以跑。如何安装NBMiner软件，可以直接点击链接去官网下载。
![](https://ac63e02.webp.li/unmineable-009.png)

### Linux版本挖矿
如果你自己电脑就是linux，那么直接挨个执行下面命令吧，已经包含了NBMiner下载解压的步骤
```
cd ~
wget https://dl.nbminer.com/NBMiner_42.3_Linux.tgz
tar xzvf NBMiner_42.3_Linux.tgz
cd NBMiner_Linux
./nbminer -a kawpow -o stratum+ssl://kp-asia.unmineable.com:443 -u AVAX:0x3De009c7aDeCf4D435fE0AA054c4c558032c5b4B.unmineable_worker_stkyqunx#s1va-4x9y -log
```
别忘了改成你自己的地址

### vast.ai快速租GPU显卡
如果你自己没有Linux机器或者你想租用更强劲的显卡服务器来挖，建议去[vast.io](https://cloud.vast.ai/?ref_id=88254)租显卡，支持虚拟货币或者小狐狸充值，很方便，租用vast.io的方法我这里不重复了，直接参考[三、GPU显卡挖矿机器配置](https://heiyetouzi.xyz/minequainetwork/#toc-heading-15)，就只要看文章目录最后的第三部分就可以，其他的部分不用看。
GPU服务器价格是按照分钟算钱的，不用了记得销毁，不然扣你钱。
服务器租用后预计5分钟就启动完毕，点击进去也是执行上面的命令
```
cd ~
wget https://dl.nbminer.com/NBMiner_42.3_Linux.tgz
tar xzvf NBMiner_42.3_Linux.tgz
cd NBMiner_Linux
./nbminer -a kawpow -o stratum+ssl://kp-asia.unmineable.com:443 -u AVAX:0x3De009c7aDeCf4D435fE0AA054c4c558032c5b4B.unmineable_worker_stkyqunx#s1va-4x9y -log
```
![](https://ac63e02.webp.li/unmineable-010.png)
![](https://ac63e02.webp.li/unmineable-011.png)

然后就可以开始愉快地挖矿，坐等收益了。上面说了，[unmineable](https://unmineable.com/?ref=s1va-4x9y)收益是按5分钟结算的，可以到具体的页面查看(免登录)，让其他人去卷gas去吧，他们卷得越厉害，咱们收益越高，爽歪歪。
查看收益的网址：https://unmineable.com/coins/AVAX/address/你的地址

![](https://ac63e02.webp.li/unmineable-012.png)


当然，本文的例子是AVAX，现在各大公链都在打铭文，一般群里在fomo什么铭文，我们就挖什么链，记住，只有高gas的时候，才赚得多。租GPU也不要选太贵的，毕竟要考虑性价比，一般GPU型号选RTX3070， RTX3080甚至RTX3060都可以。
![](https://ac63e02.webp.li/unmineable-013.png)


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
