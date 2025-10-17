---
title: 【保姆教程】手把手教你在Linux系统搭建早期alpha项目cysic的验证者&证明者
permalink: cysic-verifier-prover-setup-guide/
date: 2024-12-11 11:16:04
updated: 2024-12-25 10:12:23
categories: 撸空投
tags: 
- cysic空投
- 撸空投
- web3节点
- cysic撸毛
- cysic验证者搭建
---

## 什么是Cysic

Cysic是ZK硬件加速平台，致力于设计先进的 ASIC 芯片，帮助缩短 ZK 证明生成时间，成为首个 ZK Prover Network。Cysic是一个实时的 ZK 证明生成和验证层，旨在以最快、最便宜、最简单、最去中心化的方式提供 ZK 证明。
Cysic 最近完成了 1200 万美元的 pre - A 轮融资，OKX Ventures 和 HashKey Capital 联合领投。加上去年 2 月种子轮融资600万美元，Polychain Capital 领投。目前共融资1800万美元。
![](https://ac63e02.webp.li/cysic-001.png)

第一阶段测试网将引入验证者奖励，以验证者身份加入的用户将仅根据验证贡献获得奖励，计算资源提供者预计将在第二阶段获得奖励，参与者获得的积分将通过一定比例等奖励兑换为主网代币。Cysic Network的主网预计将于2025年Q1上线。
![](https://ac63e02.webp.li/cysic-002.png)

## Cysic账号登记

如果你是新人，不知道Chrome浏览器如何安装Metamask小狐狸钱包或者Keplr钱包，建议你上网搜索一下，先把这两个钱包插件安装好，然后每个钱包新建一个地址，记得保存好私钥和助记词。做完这一步之后再往下看，这篇教程假设你已经事先安装好了metamask和Keplr两款钱包。
![](https://ac63e02.webp.li/cysic-006.png)

### 双钱包同步账号
在连接cysic官网之前，还需要保证2个钱包的地址相同，否则会报地址不匹配的错误。那如何保证呢？我们可以将metamask钱包地址导入到keplr钱包。

**问**：如何将metamask小狐狸钱包的地址导入到Keplr钱包？
>**答**：点击metamask小狐狸钱包地址-->点击'导出私钥'-->点击keplr钱包右上角-->添加钱包-->导入已有钱包-->使用助记词或私钥-->粘贴小狐狸钱包的私钥-->导入

### 连接官网
用Chrome浏览器打开[官网](https://testnet.cysic.xyz/)，首先连接Metamask小狐狸钱包，接着连接Keplr开普勒钱包。
连上之后，钱包左边会出现一个水龙头图标，每天可以点击领0.1个cys，后续可以兑换成主网代币。
![](https://ac63e02.webp.li/cysic-004.png)
【注意】当前阶段注册还需要填入邀q码才可以登记账号，自己去[资料吧](https://ziliaoba.github.io/)找。


![](https://ac63e02.webp.li/cysic-003.png)



## Cysic验证者(verifier)

跑Cysic验证者对硬件的要求不算太高，官方建议配置如下：
 >CPU: Single Core
	Memory: 8 GB
	Disk: 512 MB
	Bandwidth: 100 KB/s upload/download
	Supported Operating Systems: Windows, Linux, Mac

以Ubuntu系统为例，打开Terminal终端，Windows系统可以打开WSL终端，执行官网如下命令：

```
wget -O ~/setup_linux.sh https://github.com/cysic-labs/phase2_libs/releases/download/v1.0.0/setup_linux.sh  
chmod +x setup_linux.sh 
./setup_linux.sh 钱包EVM地址
cd ~/cysic-verifier
./start.sh
```
windows或mac平台的教程，请自行移步[官方参考](https://testnet.cysic.xyz/m/dashboard/verifier)

当输出日志如下，就说明验证者verifier在正常跑了。
```
2024/12/05 12:23:14 sync to block: 301227
2024/12/05 12:23:38 sync to block: 301230
2024/12/05 12:24:10 sync to block: 301233
2024/12/05 12:24:38 sync to block: 301235
2024/12/05 12:25:08 sync to block: 301238
2024/12/05 12:25:38 sync to block: 301241
2024/12/05 12:26:08 sync to block: 301244
2024/12/05 12:26:38 sync to block: 301246
2024/12/05 12:27:08 sync to block: 301250
2024/12/05 12:27:38 sync to block: 301253
2024/12/05 12:28:08 sync to block: 301255
2024/12/05 12:28:39 sync to block: 301259
2024/12/05 12:29:08 sync to block: 301262
2024/12/05 12:29:38 sync to block: 301265
2024/12/05 12:30:11 sync to block: 301268
2024/12/05 12:30:39 sync to block: 301270
2024/12/05 12:31:08 sync to block: 301271
2024/12/05 12:31:38 sync to block: 301276
2024/12/05 12:32:08 sync to block: 301279
2024/12/05 12:32:38 sync to block: 301282
2024/12/05 12:33:08 sync to block: 301285
2024/12/05 12:33:38 sync to block: 301288
```

当然，可以用下面nohup命令将验证者挂到后台执行。
```
nohup ./start.sh &
```
查看日志用命令:
```
tail -f -n 10 nohup.out
```

## Cysic证明者(prover)
官方提供了Scroll Prover和Aleo Prover两种，目前推荐的是跑Scroll Prover。需要提醒的是，跑Cysic证明者对硬件的要求**非常非常**高，不过证明者同时每天产生的代币也相对可观，官方建议配置如下：
>CPU: 64-thread CPU
GPU: 2 × 3070/2080 GPUs
Memory: 280 GB
Disk: 100 GB SSD
Bandwidth: 100 KB/s upload/download
Supported Operating Systems: Linux

没看错，内存确实是需要280GB，普通家庭电脑甚至VPS积分都不能满足要求，一般考虑租赁(见教程结尾），租赁需要成本，成本不低，自行决定。经本人测试，显卡不一定需要双卡，单卡也能跑。

以Ubuntu系统为例，打开Terminal终端，Windows系统可以打开WSL终端，执行官网如下命令：

```
curl -L https://github.com/cysic-labs/phase2_libs/releases/download/v1.0.0/setup_prover.sh > ~/setup_prover.sh && bash ~/setup_prover.sh 钱包EVM地址 
cd ~/cysic-prover/ && bash start.sh
```
证明者大部分时间日志也是同上面的验证者一样，在同步区块。只是当接到计算任务的时候，就会开始消耗大量的内存和显卡资源，日志类似这样：
```
Context "Range" used 1 advice columns and 7710522 total advice cells in phase 0
Special lookup advice cells: optimal columns: 0, total 0 cells used in phase 0.
Fixed columns: 1, Total fixed cells: 276286
2024-12-05T16:09:46.925712007+08:00 INFO halo2_proofs::poly::domain - using lagrange_to_coeff_many: vec_num[1], gpu_num [1]
2024-12-05T16:09:47.443251978+08:00 INFO halo2_proofs::poly::domain - using lagrange_to_coeff_many: vec_num[0], gpu_num [1]
2024-12-05T16:09:47.574210680+08:00 INFO halo2_proofs::plonk::prover - phase1 [1] GPUs free mem = | 22.30 | GiB
in bytes = | 23945281536 | 
2024-12-05T16:09:52.910266957+08:00 INFO halo2_proofs::plonk::prover - phase2 [1] GPUs free mem = | 22.30 | GiB
in bytes = | 23945281536 | 
2024-12-05T16:09:52.910512650+08:00 INFO halo2_proofs::plonk::permutation::prover - domain.k() = 25
2024-12-05T16:09:52.910526156+08:00 INFO halo2_proofs::plonk::permutation::prover - domain.extended_k() = 27
2024-12-05T16:09:52.910543398+08:00 INFO halo2_proofs::plonk::permutation::prover - columns.len() = 3
2024-12-05T16:09:52.910563156+08:00 INFO halo2_proofs::plonk::permutation::prover - pkey.permutations.len() = 3
2024-12-05T16:09:52.910581901+08:00 INFO halo2_proofs::plonk::permutation::prover - chunk_len = 3
2024-12-05T16:09:57.789105447+08:00 INFO halo2_proofs::poly::domain - using lagrange_to_coeff_many: vec_num[1], gpu_num [1]
2024-12-05T16:10:03.293103074+08:00 INFO halo2_proofs::plonk::prover - phase3 [1] GPUs free mem = | 22.30 | GiB
in bytes = | 23945281536 | 
2024-12-05T16:10:04.905982885+08:00 INFO halo2_proofs::plonk::prover - num_advice: 1
2024-12-05T16:10:04.906019885+08:00 INFO halo2_proofs::plonk::prover - instance: 1
2024-12-05T16:10:04.906029473+08:00 INFO halo2_proofs::plonk::prover - fixed: 4
2024-12-05T16:10:04.906039632+08:00 INFO halo2_proofs::plonk::prover - lookup: 1
2024-12-05T16:10:04.906048980+08:00 INFO halo2_proofs::plonk::prover - permutation: 1
2024-12-05T16:10:04.906064689+08:00 INFO halo2_proofs::plonk::prover - cals: 10
2024-12-05T16:10:04.906073987+08:00 INFO halo2_proofs::plonk::prover - num_of_gates: 1
2024-12-05T16:10:04.906083775+08:00 INFO halo2_proofs::plonk::prover - rotations: 4
2024-12-05T16:10:04.906101839+08:00 INFO halo2_proofs::poly::domain - using coeff_to_extended_part_many: vec_num[9], gpu_num [1]
2024-12-05T16:10:08.522460461+08:00 INFO halo2_proofs::poly::domain - using coeff_to_extended_part_many: vec_num[1], gpu_num [1]
2024-12-05T16:10:09.151370384+08:00 INFO halo2_proofs::poly::domain - using coeff_to_extended_part_many: vec_num[3], gpu_num [1]
2024/12/05 16:10:09 sync to block: 302546
2024/12/05 16:10:09 start process needSubmitProofHashTask: YHxBR86R0X2fE97j1NMM6dCTYCX2+HLSftct6IHzym8=, taskType: scroll, taskVersion: v1.0
2024/12/05 16:10:09 process needSubmitProofHashTaskList finish
```
如果你的机器内存不足256GB，就会被OOM kill(内存不足，杀死进程)。

windows或mac平台的教程，请自行移步[官方参考](https://testnet.cysic.xyz/m/dashboard/verifier)

同样，也可以用nohup命令，将证明者挂到后台执行。
```
nohup ./start.sh &
```
查看日志用命令:
```
tail -f -n 10 nohup.out
```

## 验证者和证明者奖励规则
从官网Overview界面可以查看当前网络中存在的所有验证者和证明者数量。
![](https://ac63e02.webp.li/cysic-007.png)

目前，Verifer与Prover规则经过多轮调整，奖励分配更合理，细节如下——
>平台（10%）：10CYS + 10CGT
Prover（70%）：总计70CYS + 70CGT
Prover0：49CYS + 49CGT
Prover1：10.5CYS + 10.5CGT
Prover2：10.5CYS + 10.5CGT
如果Prover2未提交结果，其份额（10.5CYS+10.5CGT）将分配给Prover1。
Verifer（20%）：总计20CYS + 20CGT，在所有参与验证的Verifer（最多20人）中平均分配。
每个Verifer将收到 (20/n) CYS + (20/n) CGT，其中 n 为提交结果的Verifer数量（n≤20）。


## Cysic备份key
需要注意的是，不管你是跑验证者还是跑证明者，第一次跑成功的时候，都需要把程序自动生成的key文件备份好，如果你没有备份key，那么后果非常严重，等到领空投的时候，key丢了就啥也没有了。备份了key，后面需要更换机器，则把备份的key文件放到下面👇🏻的路径，重启start.sh脚本即可。
```
# 验证者的key路径：
/root/.cysic/keys/ 

# 证明者的key路径：
/root/cysic-prover/~/.cysic/assets/

```

## Cysic常见问题
1. Cysic什么时候上主网？
答：官方说2025年Q1。

2. 可以跑多号吗？会不会被女巫？
答：可以跑多号，但是一个钱包地址只能跑1个验证者和1个证明者，一台机器上可以跑多个地址，只要你的配置够就行。

3. 我机器的内存没有256GB，我可以跑证明者吗？
答：不行，平常没任务的时候都没问题，接到任务的时候，内存要求很高，不足256GB内存，你的证明者进程就会被程序杀死。

4. 产生的CYS币和CGT币有什么区别？
答：cysic是双代币模型，这两个币可以直接在网页上点Exchange 1:1兑换，后期都会兑换成主网代币。

5. 跑验证者和证明者产生的CYS、CGT代币需要每天领吗？
答：建议每天领，领完兑换成CGT币，到质押界面质押CGT币，质押又可以产生币，当前质押的利息很高。

6. 我为什么没有邀q码？
答：按照规则，需要至少质押12个CGT才有邀q码

7. 为什么我跑了几个小时了还没有分到cys或者cgt币？
答：任务池里的任务是随机分配给所有的验证者或证明者的，只要日志是正常的，一般等1天左右就会轮到，如果太久还没有，那建议到官方dc开票让查一下。

8. 跑验证者/证明者的时候报错如下
```
error while loading shared libraries: libcudart.so 12: cannot open shared object file: No such file or directory.
```
答：是网络不好，文件没下全，建议重新下载完毕之后重试，或者换一台网络好一点的机器(最好能魔法)

9. 我想租GPU显卡机器跑证明者(prover)，有推荐的平台吗？
答：跑证明者需要256GB内存+24GB显存的机器，基本没有符合条件的GPU租赁平台，vast.ai上有少量的，不过价格不算低，1小时大概$0.5，而且目前都被租光了，你可以蹲守下。关于vast.ai GPU显卡租赁的细节，可以参考文章https://heiyetouzi.xyz/minequainetwork/#toc-heading-15, 直接跳到最后看第三部分——GPU显卡挖旷机器配置，其他不用看。


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
[《明星项目QuaiNetwork全节点+GPU节点搭建手把手教程[最新]》](https://heiyetouzi.xyz/minequainetwork)


###  大家都在搜
国内购买比特币，depin小草挂机, taker挖矿, taker钻石, 小草grass空投怎么领, 炒币交易所，okx下载注册，国内okx充值，币安App注册，币安App下载, 币安平台买币教程，币安注册，bianace撸空投注册，币安苹果手机下载，总统币怎么买，狗狗币怎么买，人民币购买比特币，欧易 怎么下载，web3撸毛, web3零撸，bitget大陆下载注册，欧易护照注册，欧易下载,币安下载,炒币副业,欧易合约, 欧易OKX如何充值人民币, 欧易怎么充值, NFT钱包怎么弄, 火币如何充值人民币, 币圈新手入门教程, btc8848.com, 炒合约Tony心法，合约杠杆bit浪浪，Defi挖矿，币圈撸毛，币圈空投还能玩吗，做合约爆仓怎么办，欧易币安货币怎么买总统币，欧易币安以太坊怎么买， Defi质押挖矿怎么玩, NFT还能玩吗, we3空投撸毛, 币圈web3零撸怎么玩, 铭文怎么打, 符文怎么打, 币圈小白入门, 如何炒币, 炒币挣钱吗, 币圈新手教程btc8848.com, 炒币赚钱吗, 什么是合约杠杆, Defi挖矿, 币圈撸毛怎么玩, 欧易okx空投, 节点质押, 爆仓, 财富自由, 黑夜投资heiyetouzi.xyz

如果您觉得我的文章写得不错，对您有帮助，不妨点击文末给黑叶哥打赏一杯咖啡☕️，感谢！
