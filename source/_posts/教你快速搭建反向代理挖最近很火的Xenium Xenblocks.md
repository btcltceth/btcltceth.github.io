---
title: 教你快速搭建反向代理挖最近很火的Xenium/Xenblocks
permalink: minexeniumxenblocks/
date: 2023-09-30 13:23:12
updated: 2023-10-02 17:24:26
categories: 挖矿
tags:
- Xenium
- 区块链
- XenBlocks
---

## 自己搭建反向代理
这几天，大家都在抢国外区块链大雕JackLevin搞的新项目——Xenium(XNM)的头矿，据说结合了BTC和ETH的优点，堪称跨时代的产品。你看海外显卡租赁平台[vast.ai](https://cloud.vast.ai/?ref_id=88254)上RTX 4090已经被国人租光了就知道了，现在价格已经很不划算了。

![](https://ac63e02.webp.li/xenium-4090-001.png)

于是乎，群友看准了国内少数几个还能便宜租到4090显卡的网站，不过国内租GPU挖的话，就会有网络问题，反向代理可以解决。但是用别人的反向代理总是不放心啊，挖矿收益抽走多少你不知道，安全不安全也不知道，千万不要自己稀里糊涂执行别人给的一句`sed`命令就开始挖矿。其实自己搭建反向代理一点也不难。这篇教程就来教你如何自己搭建反向代理。

(PS: 国内租GPU的网站有阿里云，腾讯云，AutoDL等，总体来说还是比国外的[vast.ai](https://cloud.vast.ai/?ref_id=88254)便宜不少的，就是需要用到反向代理而已)

### 第一步：注册海外主机
这里我直接用著名的[vultr](https://www.vultr.com/?ref=9542602-8H)了，毕竟它近期有绑卡充值$35以上就送$100的超级活动，如果你是新人的话，最好参加一下，好几年了都没有过这个活动。

直接邮箱注册，绑卡充值即可。路径是左侧栏Account-->Billing，当然那，如果你着急着挖Xenium矿，也可以先用支付宝充点钱，等空了再绑卡。不用充太多，充个20块就够了。

### 第二步：创建服务器
记住，我们只是用来做反向代理，所以选最便宜的就好。
点击右上角蓝色的“Deploy +" --> "Deploy New Server"——
- Server选最便宜的$2.5/mo的Cloud Compute
- CPU选最便宜的intel Regular Performance
- Server地区随便选，不过最好选欧洲的，因为离Jack的[xenminer.mooo.com](xenminer.mooo.com)网站近一些访问快。
- 服务器镜像Server Image选Ubuntu 22.04 LTS x64
- 服务器规格Server Size选最便宜的$6的
- 关闭自动备份，还能省$1.2
 ![](https://ac63e02.webp.li/xenium-4090-002.png)

这样一顿骚操作下来，这台服务器一个月就只需$5就够了，相当于你在[vast.ai](https://cloud.vast.ai/?ref_id=88254)上4090单卡挖1个小时的价格。

### 第三步: 安装反向代理
等待3分钟让机器初始化完毕，可以使用SSH或者"View Console"连接到机器上，机器的ip、用户名、密码都可以点开你上一步创建好的服务器详情看到。
 ![](https://ac63e02.webp.li/xenium-4090-003.png)

建议使用SSH连接上去安装操作方便，它那个"View Console"粘贴功能非常难用，如何使用SSH连接到远程主机，这里不说了，太基础，不会的话自己百度下。


接着执行下面命令，安装nginx
```
apt-get update && apt-get -y install nginx
cd /etc/nginx/sites-available && touch reverse-proxy.conf
```

看清楚当前是在`/etc/nginx/sites-available`目录下，没问题的话执行`vim reverse-proxy.conf`打开，粘贴如下内容，记得将xxx.xxx.xxx.xxx改成你上面自己申请的服务器ip地址，输入`:wq`保存。
```
server {
    listen 80;
    server_name xxx.xxx.xxx.xxx;

    location / {
        proxy_pass http://xenminer.mooo.com;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}


server {
    listen 4445;
    server_name xxx.xxx.xxx.xxx;

    location / {
        proxy_pass http://xenminer.mooo.com:4445;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

server {
    listen 4446;
    server_name xxx.xxx.xxx.xxx;

    location / {
        proxy_pass http://xenminer.mooo.com:4446;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

server {
    listen 4447;
    server_name xxx.xxx.xxx.xxx;

    location / {
        proxy_pass http://xenminer.mooo.com:4447;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

执行`ln -s /etc/nginx/sites-available/reverse-proxy.conf /etc/nginx/sites-enabled/`设置软连接
执行`nginx -t` 检查nginx配置是否正确，返回success或者ok就说明没问题，
执行`systemctl reload nginx`命令重新加载 Nginx 配置。
 ![](https://ac63e02.webp.li/xenium-4090-005.png)

### 第四步：关闭防火墙
玛德这里查了好久，重要的事情说3遍，这里一定要执行`ufw disable`命令关闭防火墙。
 ![](https://ac63e02.webp.li/xenium-4090-006.png)

ok，来测试一下，打开你的浏览器，依次测试反向代理是否有效
访问`http://xxx.xxx.xxx.xxx/difficulty`和`http://xxx.xxx.xxx.xxx:4445/getblocks/lastblock`看看是否都能正常访问。这里xxx.xxx.xxx.xxx仍然是你自己的服务器IP。
 ![](https://ac63e02.webp.li/xenium-4090-007.png)

## 使用反向代理
登录你自己的挖矿机器，进入到XENGPUMiner目录，执行如下命令：
```
sed -i.bak 's@xenminer.mooo.com@xxx.xxx.xxx.xxx@g' syncnode.py merkleroot.py miner.py config.conf
#这里xxx.xxx.xxx.xxx仍然是你自己的服务器IP

```
 ![](https://ac63e02.webp.li/xenium-4090-008.png)

重新启动`xengpuminer`和`python3 miner.py --gpu=true`程序，`difficulty`难度可以正常获取，再也不会一直卡在1727难度了，就说明没问题，反向代理它起作用了。
![](https://ac63e02.webp.li/xenium-4090-009.png)

不得不说，国人热情真高，现在挖Xenium难度直线上升已经到82500了，不过未来只会更高，大家都理性一些哈。

## 小礼物
感谢看到这里，希望文章对你有帮助，最后，有个小礼送给大家，[openbayes](http://openbayes.com/console/signup?r=xiaominghuang_7z1L)最近在做活动，新人(必须填写邀请码)注册立马送60分钟RTX 3090，可以用来挖Xenium哈，拿走不谢。

需要魔法(翻墙)工具的童鞋，可以点开右上角[友情链接](https://heiyetouzi.xyz/friends)里有。

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


