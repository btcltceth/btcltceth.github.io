---
title: 一文看懂最近很火的Solana pow明星项目——ORE显卡GPU保姆级教程
permalink: solana-ore/
date: 2024-04-11 12:05:47
updated: 2024-04-16 11:15:22
categories:  挖矿
tags:
- $solana
- $ore
- 租显卡
- 租服务器
- 零撸
- jito
---

ORE是著名公链Solana下的第一个POW，Solana创始人推转发之后，将ore推向了火爆的市场。本文教程以Ubuntu 20.04为例，详细介绍ORE在显卡GPU CUDA下如何进行快速挖掘。

### 环境配置
得益于tonyke老哥以及BenjaSOL老哥的开源精神，无jito版本的ORE GPU代码已经在[https://github.com/BenjaSOL/ore-cli-gpu.git](https://github.com/BenjaSOL/ore-cli-gpu.git)开源，找一台有独立N系列显卡的机子，RTX 30, 40系列的都可以跑，10系列的有群友说也可以，我没试过。

然后逐行拷贝下面命令到linux 终端，执行完毕就配置好了相关的vim, cargo, solana, ore-cli环境，预期耗时5分钟，最后有报几个警告不要管。
```
apt update -y && apt upgrade -y 
curl https://sh.rustup.rs -sSf | sh -s -- -y
source $HOME/.cargo/env
sh -c "$(curl -sSfL https://release.solana.com/v1.18.4/install)"
export PATH="/root/.local/share/solana/install/active_release/bin:/root/.cargo/bin:$PATH"
apt install build-essential cargo jq bc vim git pkg-config libssl-dev -y
git clone https://github.com/BenjaSOL/ore-cli-gpu.git ~/ore-cli-gpu
cd ~/ore-cli-gpu 
export CUDA_VISIBLE_DEVICES=0
nvcc linux.cu -o linux
sed -i 's#PATH_TO_EXE#/root/ore-cli-gpu/linux#g' src/mine.rs
cargo build --release
```
![](https://ac63e02.webp.li/ore-0.png)


### Wallet钱包
用[MCT工具](https://mct.xyz/create-wallet?chain=sol)可以直接生成SOL钱包，如果要也可以生成批量，这里我们先生成1个，把信息保存到重要的地方，千万别泄露丢失。然后复制其中的最后一行数字格式的私钥，粘贴到上面Ubuntu系统中`~/.config/solana/id.json`文件中，保存。也可以用命令行来保存：
```
echo [17, 244, 140, 68, 96, 23, 11, 26, 38, 72, 166, 245, 226, 66, 242, 232, 104, 88, 131, 29, 140, 117, 180, 161, 187, 221, 15, 89, 181, 74, 33, 254, 129, 200, 186, 38, 159, 125, 219, 247, 92, 106, 164, 27, 255, 117, 115, 36, 216, 104, 136, 246, 122, 73, 254, 110, 16, 170, 140, 61, 177, 51, 219, 206] > ~/.config/solana/id.json
```
![](https://ac63e02.webp.li/ore-1.png)
开始挖掘ore之前，务必记得先往钱包充值一些SOL币充当gas，SOL币可以从[欧易](https://www.chouyi.kim/zh-hans/join/76527935)提到你的钱包，大概1~3分钟就可以到账，单个钱包不用放太多SOL币，大概0.01个就够了。


### ORE挖掘
#### ORE挖掘命令

```
/root/ore-cli-gpu/target/release/ore --rpc http://api.mainnet-beta.solana.com --keypair ~/.config/solana/id.json --priority-fee 600000 mine --threads $(nproc)
```
当出现如下的界面，就表示GPU已经在计算哈希，说明没问题，一切都准备就绪了。
![](https://ac63e02.webp.li/ore-2.png)

好了，你现在可以开始愉快地挖倔ORE了，下面是一些简单有用的命令——


#### 查询ORE收益——rewards
```
/root/ore-cli-gpu/target/release/ore --rpc http://api.mainnet-beta.solana.com --keypair ~/.config/solana/id.json rewards
```
![](https://ac63e02.webp.li/ore-3.png)


#### 收取挖掘出的ORE——claim
```
/root/ore-cli-gpu/target/release/ore --rpc http://api.mainnet-beta.solana.com --keypair ~/.config/solana/id.json --priority-fee 50000000 claim
```
claim需要不断尝试，如果不行，就提高fee再试。
![](https://ac63e02.webp.li/ore-4-1.png)
claim成功的话，会显示“Transaction landed!
![](https://ac63e02.webp.li/ore-4-2.png)


#### 出售ORE
您随时可以将ORE及时卖掉换成SOL，地址[https://jup.ag/](https://jup.ag/) 或者[birdeye.so](https://birdeye.so/token/oreoN2tQbHXVaZsr3pf66A48miqcBXCDJozganhEJgz?chain=solana)，连接Phantom钱包插件(导入你挖ore的wallet)，就可以直接实时兑换成SOL币
![](https://ac63e02.webp.li/ore-5.png)
![](https://ac63e02.webp.li/ore-6.png)



#### RPC节点
目前，公共的免费RPC(比如上面的http://api.mainnet-beta.solana.com), 用的人太多，已经基本挖不出来了，这时候我们需要购买付费的RPC，市面上的RPC服务商我基本都用过，还是推荐[https://www.quicknode.com](https://www.quicknode.com/?via=chen)、[https://alchemy.com](https://alchemy.com/?r=9e43bf40e8668bce) ，比如quicknode $49/月的就可以挖，有500M的API请求次数，也够你用了。

购买付费RPC的时候需要美国的信永卡，没有海外信永卡怎嘛办？可以临时注册一个[虚拟卡Dupay](https://dupay.one/web-app/register-h5?invitCode=hmXfgp&lang=zh-cn)，有几$的开卡费，需要实名，平常绑定支夫宝和某信小费。关于如何给Dupay卡充值，这里不展开，有需要的童鞋可以直接参考[《ChatGPT Plus官方推荐新手教程》](https://chatgpt-plus.github.io/)中的第二部分，耐心一步一步操作。用虚拟卡不用担心被多扣钱，我是非常不建议用自己国内常用的信永卡来绑定这些国外的网站，它们都很无下限乱扣费。

#### GPU租赁
如果你自己没有显卡，则可以去租赁，按小时付费，一般RTX 4090单卡显卡是0.4$/h，一天大概10刀左右。
因为国内云翻有下载海外的依赖包有各种问题，所以推荐直接用国外显卡[https://cloud.vast.ai](https://cloud.vast.ai/?ref_id=88254)，支持虚拟货币或者小狐狸钱包充值，很方便
如何充值，租机器看这里：[https://heiyetouzi.xyz/minequainetwork/#toc-heading-15](https://heiyetouzi.xyz/minequainetwork/#toc-heading-15)，直接看第三部分——GPU显卡挖旷机器配置，其他不用看。
租便宜的RTX 3060， RTX3070就可以了，没必要上RTX4090，一小时大概$0.15左右，服务器模板选”cuda:12.0.1-devel-ubuntu20.04”，点击Edit，勾上“Run a jupyter-python notebook”选项，机器租好后，点击左侧INSTANCES，这里的open(或者connecting)打开命令行窗口，
![](https://ac63e02.webp.li/ierc20m6-001.png)
![](https://ac63e02.webp.li/ierc20m6-002.png)


#### 关于priority-fee
priority-fee给多少合适？
> 看当前网络拥堵情况决定，跟你一起卷gas的人越多，priority-fee需要越大，不然平常给1就可以，群里有小伙伴给到1000w，看自己能承受的成本决定，gas越大越贵，具体成本花费可以复制tx id到[solscan网站](https://solscan.io/)查看，悠着点，毕竟交互失败了也是要给gas的。

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


