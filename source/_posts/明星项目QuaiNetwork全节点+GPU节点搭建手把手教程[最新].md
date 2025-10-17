---
title: 明星项目QuaiNetwork全节点+GPU节点搭建手把手教程[最新]
permalink: minequainetwork/
date: 2023-10-13 17:23:28
updated: 2023-10-13 22:25:18
categories: 挖矿
tags:
- Quai节点
- QuaiNetwork
- vast4090显卡
- stratum
---

融资千万的明星项目QuaiNetwork可能大家都知道，这项目融资了两轮，加起来上千万美金，算是这两年为数不多的明牌空投的好项目。这两天旷工群里非常热闹就是因为QuaiNetwork测试网铁器时代开挖了，本次一共发放1200万个代币，其中全节点矿工分配了800万个，不过因为搭建全节点稍微复杂了些，坑很多，导致把一部分矿工挡在了门槛之外。本人经过2天的摸索、试错，埋伏官方开发者discord群4天，终于开挖成功，赶紧总结了篇教程，分享给大家。目前QuaiNetwork还处在很早期的阶段，妥妥的头矿，而且已经明牌会空投给矿工，想早期介入的，抓紧了，趁着现在有门槛竞争小，先动手已经跑赢大部分人了。这几天官方discord非常活跃，开发者都在拼命跟矿工交流——
![](https://ac63e02.webp.li/quai-discord-001.png)

## 一、全节点搭建
### 1、注册阿里云
要挖头矿，必须先搭建全节点，全节点对配置要求很高，官方推荐的是CPU至少32core, 内存mem至少64GB，SSD固态硬盘至少3T。一般家庭机器没有这么豪华配置，跑不起来，到时候浪费了时间前功尽弃不划算。所以，我们直接租[阿里云](https://www.aliyun.com/daily-act/ecs/ecs_trial_benefits?userCode=jgvx7nlo)来搭建，先注册账号，新注册有较大补贴优惠。账号注册成功后，点击左上角——产品——云服务器ECS——立即购买——
![](https://ac63e02.webp.li/quai-aliyun-setup-000.png)

### 2、购买ECS服务器
选择按量付费，地区选印度、香港、新加坡之类的，价格差不了多少。机器规格选的16共享核，32G内存。
![](https://ac63e02.webp.li/quai-aliyun-setup-001.png)
[**小技巧**] 这里选“抢占式实例”能省90%左右的成本，不过有被别人强制抢占释放的风险，你自己衡量。

- 系统镜像选Ubuntu20.04，磁盘前期先选300G，后面随时可以扩容的。
![](https://ac63e02.webp.li/quai-aliyun-setup-002.png)

- 公网ip勾选上，做全节点一定需要一个公网ip。带宽设置大于10Mbps。
![](https://ac63e02.webp.li/quai-aliyun-setup-003.png)

- 设置root管理员登录密码，后面远程ssh登录需要用到。
![](https://ac63e02.webp.li/quai-aliyun-setup-004.png)
点击“确认下单”后，Ubuntu系统实例会很快给你准备好，同时会给你分配一个可用的公网ip。

- 本机通过ssh远程连接到服务器
我本机是mac，直接打开终端Terminal，执行命令`ssh root@公网ip`，输入你刚设置的密码即可连上服务器。
![](https://ac63e02.webp.li/quai-aliyun-setup-005.png)

### 3、设置端口开放
全节点服务器需要设置端口开放的2个原因：
- 原因1：全节点同步数据过程中，需要跟网络上的其他节点(peer)通信，一般通过端口30303-30315。
- 原因2：全节点后面需要开放给远端的显卡矿机通信，一般通过端口3333。

所以，这里需要对上面创建的ECS实例开放至少3333以及30303-30315端口，不过，为了方便，我们暂且给它通通都开放。
- 在刚创建的服务器实例页面点击实例。
![](https://ac63e02.webp.li/quai-aliyun-sg-001.png)

- 点击安全组->配置规则->点手动添加，如果没有安全组就先创建一个默认的再配置。
![](https://ac63e02.webp.li/quai-aliyun-sg-002.png)

- 新增一条规则：协议类型选“全部”，源/目的端口范围都填-1/-1，授权对象源填0.0.0.0/0，保存。
![](https://ac63e02.webp.li/quai-aliyun-sg-003.png)

再回到实例页面，把实例加入(绑定)刚创建好的安全组。

### 4、Quai钱包创建
关于官方钱包的说明文档：[Wallets](https://docs.quai.network/use-quai/wallets)。 
当前，矿工们一般都用开源的[pelagus](https://pelaguswallet.io/)钱包。安装好钱包浏览器扩展插件之后，创建助记词，拿小本本记下里，然后进入钱包，建议每个zone都创建一个地址，下面挖矿配置文件需要用到。Quainetwork一共有9个zone, cyprus1, cyprus2, cyprus3, paxos1, paxos2, paxos3, hydra1,hydra2, hydra3。每个zone所在地理区域不一样，都可以挖矿，难度不一。
![](https://ac63e02.webp.li/quai-wallet-001.png)

### 5、go-quai节点程序配置
#### 5.1、安装依赖
登录上面申请的ECS服务器，依次执行
```
apt update &&  apt upgrade -y
apt install vim snapd -y
snap install go --classic
apt install git make -y
```
#### 5.2、配置go-quai工程
```
cd ~
git clone https://github.com/dominant-strategies/go-quai.git
cd go-quai && git checkout v0.19.4  # 如tags有版本更新，请以https://github.com/dominant-strategies/go-quai/tags为准
cp network.env.dist network.env
```
执行命令`vim network.env` 打开网络配置文件，做如下修改后保存——
1. 将ZONE_0_0到ZONE_2_2一共9个zone的钱包地址都替换成你自己上面创建的地址。
2. 最后两行改成：ENABLE_NAT=true，EXT_IP=你上面申请的服务器公网IP地址
![](https://ac63e02.webp.li/quai-download-000.png) 

#### 5.3、打开端口
依次执行命令如下：
```
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT
iptables -F
iptables-save
apt-get install iptables-persistent
netfilter-persistent save
netfilter-persistent reload
```

### 6、下载官网区块数据(很大)
区块链的分布式节点数据，如果每次都从0区块高度开始同步，则非常耗时，好在官方每个几天都会提供最新的区块数据打包供我们下载，导入区块数据可以加快同步速度。
```
cd ~
wget https://archive.quai.network/quai_colosseum_backup.tar.gz # 下载
tar -xzvf quai_colosseum_backup.tar.gz  # 解压，耐心等待
cp -r quai_colosseum_backup ~/.quai # 拷贝到~/.quai，耐心等待
```
![](https://ac63e02.webp.li/quai-download-001.png) 

### 7、运行全节点程序
拷贝完成后，依次执行下列命令，先编译，后执行：
```
cd go-quai  
make go-quai # 编译
make run # 运行
```
- 问题1：如何判断节点有没有在后台运行？
执行命令`ps aux | grep quai`
![](https://ac63e02.webp.li/quai-running-001.png) 

- 问题2：如何判断节点有没有在同步区块？
执行监控命令`cd ~/go-quai; watch  'cat  nodelogs/* | grep Appended | tail -n 10'`, 出现如图所示的页面一直在刷“Appended new block”,就说明节点已经在在同步了。
![](https://ac63e02.webp.li/quai-running-002.png)

- 问题3. 如何判断节点区块数据同步已经完成？
答案是：跟官方仪表盘里的区块数据比较。
上面截图中，我们本地的区块高度是：number=[1741 13145 129747]，三个数字分别代表prime, region, zone，
官方仪表盘：https://stats.quai.network  ，实时更新的。
![](https://ac63e02.webp.li/quai-running-003.png)
只要咱们本地的区块高度大等于官方仪表盘上的区块高度就证明数据同步已经完成。

【重要！】
 在进入下面配置gpu矿机执行挖矿之前，一定要确保节点已经完全同步，不然挖到的币都是无效的。并且，根据经验，同步很慢，取决于你的服务器配置(CPU/内存/磁盘/网络)，我身边的几个矿工基本都是同步了1天左右，快的4~5个小时。

## 二、stratum代理搭建
### 1、stratum代理编译
建议stratum代理直接安装在👆🏻上面的节点服务器上，这样修改的配置最少。
```
cd ~
git clone https://github.com/dominant-strategies/go-quai-stratum
cd go-quai-stratum
git checkout v0.8.0-rc.2 # checkout 最新版本，以https://github.com/dominant-strategies/go-quai-stratum/tags页面为准
cp config/config.example.json config/config.json # 拷贝配置文件
make quai-stratum # 编译
```

### 2、stratum代理运行
以下命令执行哪一个，取决于你想在哪一个zone挖矿，一共9个zone，建议选难度低的、离你全节点近的zone挖，上面的仪表盘可以查看实时难度，上面我们全节点是用的印度的，所以，这里我们选hydra1~hydra3亚洲的zone。
```
cd ~/go-quai-stratum
./build/bin/quai-stratum --region=8579 --zone=8611 # cyprus1 
./build/bin/quai-stratum --region=8579 --zone=8643 # cyprus2
./build/bin/quai-stratum --region=8579 --zone=8675 # cyprus3
./build/bin/quai-stratum --region=8581 --zone=8613 # paxos1
./build/bin/quai-stratum --region=8581 --zone=8645 # paxos2
./build/bin/quai-stratum --region=8581 --zone=8677 # paxos3
./build/bin/quai-stratum --region=8583 --zone=8615 # hydra1
./build/bin/quai-stratum --region=8583 --zone=8647 # hydra2
./build/bin/quai-stratum --region=8583 --zone=8679 # hydra3
```
stratum代理执行成功的话，会往连接上来的矿机不停发送job任务，截图如下：
![](https://ac63e02.webp.li/quai-running-004.png)
以上就是Quai全节点+stratum代理搭建的全部教程，下面👇🏻讲一讲如何设置GPU显卡——

## 三、GPU显卡挖矿机器配置
### 1、购买vast显卡机器
阿里云上没有找到合适又便宜的GPU机器，这里我在[vast.ai](https://cloud.vast.ai/?ref_id=88254)上租显卡，一般租RTX 4090，价格在0.4$/h-0.5$/h，还算实惠，高峰时期会更贵。点击 [vast.ai](https://cloud.vast.ai/?ref_id=88254) 注册成功后验证完邮箱，再去billing页面充值，至少充值个10$-20$，支持绑定visa信用卡充值，也可以直接metamask小狐狸支付，甚至还可以选coinbase用加密货币支付。
![](https://ac63e02.webp.li/quai-gpu-vast-001.png)

从模板创建GPU挖矿机器，模板选`Cuda:12.0.1-Devel-Ubuntu20.04`，点击`Edit`，勾上`Run a jupyter-python notebook`。
![](https://ac63e02.webp.li/quai-gpu-vast-002.png)
![](https://ac63e02.webp.li/quai-gpu-vast-003.png)

过滤选项，一般我们租4090机器，地理位置尽量选亚洲的(如果有的话)。
![](https://ac63e02.webp.li/quai-gpu-vast-004.png)

机器初始化后，按钮会变成open或connecting，点击open jupyter页面，右上角选new->terminals，浏览器弹出终端页面。
![](https://ac63e02.webp.li/quai-gpu-vast-005.png)

看到直接以root打开命令终端
![](https://ac63e02.webp.li/quai-gpu-vast-006.png)

### 2、安装运行gpu-miner程序
在上面👆🏻打开的命令行窗口，依次执行下列命令：
```
apt update &&  apt upgrade -y 
apt install -y git cmake build-essential mesa-common-dev screen vim 
apt-get install nvidia-cuda-toolkit -y 
cd ~
git clone https://github.com/dominant-strategies/quai-gpu-miner && cd quai-gpu-miner 
git submodule update --init --recursive
cd libethash-cuda
```
执行`vim ~/quai-gpu-miner/libethash-cuda/CMakeLists.txt`，找到指定行，按图修改，保存:
![](https://ac63e02.webp.li/quai-gpu-vast-007.png)

执行`vim ~/quai-gpu-miner/ethcoreminer/main.cpp`，找到指定行，按图修改，保存:
![](https://ac63e02.webp.li/quai-gpu-vast-008.png)

接着依次执行下面命令，编译quai-gpu-miner，
```
cd ~/quai-gpu-miner
mkdir build && cd build
cmake .. && cmake --build .
```

执行下面的命令开始gpu挖矿，记得xxx.xxx.xxx.xxx修改为你上面配置的阿里云ECS服务器公网IP。注意这个程序容易自己跑挂，跑挂了重新启动下就行，最好自己写个死循环或者守护进程让它一直跑。
```
 cd quai-gpu-miner/build/
./ethcoreminer/ethcoreminer -G -P stratum://xxx.xxx.xxx.xxx:3333 
```
![](https://ac63e02.webp.li/quai-gpu-vast-009.png)

注意这个程序容易自己跑挂，跑挂了重新启动下就行，最好自己写个死循环或者守护进程让它一直跑。参考X上大V dapaopao711的shell脚本如下,保存成test.sh跑在后台就行。
```
#!/bin/bash
while [ 1 ];
do
sleep 2
./ethcoreminer/ethcoreminer -G -P stratum://xxx.xxx.xxx.xxx:3333 -L 1 && break
done
```

下图中的61.89Mh是4090显卡算力，当看到显示的"Accepted"，则表示挖到区块(币)了。
![](https://ac63e02.webp.li/quai-gpu-vast-010.png)

区块浏览器： https://hydra2.colosseum.quaiscan.io/， 可以查到挖到的币信息。
也可以查看自己的钱包。
![](https://ac63e02.webp.li/quai-gpu-vast-011.png)

最后，特别感谢推大神[dapaopao](https://twitter.com/dapaopao711)最开始无私的分享，让我们每个人都可以挖上quai头矿，蹲一个暴富可能。

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

