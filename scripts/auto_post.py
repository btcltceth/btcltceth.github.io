import os
import random
import time
import logging
import json
import datetime
import subprocess
from utils import ai, wechat
from utils.constants import ARTICLE_TEMPLATE_DIR, COUNTS_FILE, SOURCE_POST_DIR, POST_TAG_LIST, HEIYE_DIR, JIKETOUZI_CMD_DIR, JIKETOUZI_CRYPTO_DIR

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    handlers=[
        logging.StreamHandler(),  # 输出到控制台（Jenkins能捕获）
        logging.FileHandler("./auto.log", encoding="utf-8")  # 同时写文件
    ]
)

def load_counts():
    if not os.path.exists(COUNTS_FILE):
        return {}
    with open(COUNTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_counts(counts):
    with open(COUNTS_FILE, "w", encoding="utf-8") as f:
        json.dump(counts, f, ensure_ascii=False, indent=2)

def get_article(counts):
    files = [f for f in os.listdir(ARTICLE_TEMPLATE_DIR)
             if os.path.isfile(os.path.join(ARTICLE_TEMPLATE_DIR, f))]
    if not files:
        raise FileNotFoundError(f"❌❌❌目录{ARTICLE_TEMPLATE_DIR}中没有找到任何文章,请检查...")

    titles = [os.path.splitext(f)[0] for f in files]
    min_count = min(counts.get(t, 0) for t in titles)
    candidates = [f for f in files if counts.get(os.path.splitext(f)[0], 0) == min_count]

    chosen_file = random.SystemRandom().choice(candidates)
    title = os.path.splitext(chosen_file)[0]
    file_path = os.path.join(ARTICLE_TEMPLATE_DIR, chosen_file)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    logging.info(f"📚📚📚 本次选取文章《{title}》（已选{counts.get(title, 0)}次）")
    return title, content

def create_post(title, content):
    new_title = title.replace("'", "").replace(" ", "_")

    translated = ai.translate(title, "将下列中文标题翻译为英语，用JSON返回，键为english，只返回JSON，不要解释。")
    if not translated or "english" not in translated:
        logging.error("❌❌❌ 翻译标题失败，跳过本轮")
        return None

    english_title = translated.get("english", new_title)
    permalink = "-".join(english_title.lower().replace("'", "").split()) + "/"

    start_date = datetime.date(2024, 4, 1)
    end_date = datetime.date.today()
    delta_days = (end_date - start_date).days
    random_date = start_date + datetime.timedelta(days=random.randint(0, delta_days))
    date_str = f"{random_date} {random.randint(8,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}"

    updated_date = random_date + datetime.timedelta(days=random.randint(3, 10))
    updated_str = f"{updated_date} {random.randint(8,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}"

    categories = random.choice(["撸空投", "区块链入门", "web3空投", "虚拟货币", "交易", "币圈", "港美股"])
    tags = random.sample(POST_TAG_LIST, random.randint(3, 5))
    tags_str = "\n".join([f"- {tag}" for tag in tags])

    front_matter = f"""---
title: {title}
permalink: {permalink}
date: {date_str}
updated: {updated_str}
categories: {categories}
tags: 
{tags_str}
---
> 作者 黑叶(black leaf)，币圈从业13年，早年活跃在微博，雪球，入场比大多数KOL都早。巅峰持仓200枚BTC，见过账户七位数归零，也见过一夜暴富。LUNA崩盘那晚没睡，312那天没跑。亏过，赚过，活下来了。现在研究怎么让你也活下来。加密/量化/合约/Web3撸毛/港美股。

"""

    file_path = os.path.join(SOURCE_POST_DIR, f"{new_title}.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(front_matter + content)

    logging.info(f"✅✅✅ 黑叶新文章已生成：{file_path}")
    return permalink, file_path

def execute_hexo_push():
    logging.info("🚀🚀🚀 开始执行 hexo clean && hexo g && hexo d ...")
    try:
        result = subprocess.run(
            "hexo clean && hexo g && hexo d",
            shell=True,
            cwd=HEIYE_DIR,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            logging.info(f"✅✅✅ hexo 执行成功！\n{result.stdout}")
            return True
        else:
            error_msg = f"❌❌❌ hexo 执行失败！\n{result.stderr}"
            logging.error(error_msg)
            wechat.send_wechat_notification(error_msg)
            return False
    except Exception as e:
        error_msg = f"❌❌❌ hexo 执行异常：{str(e)}"
        logging.error(error_msg)
        wechat.send_wechat_notification(error_msg)
        return False    

def create_jiketouzi_post(title, content):
    new_title = title.replace("'", "").replace(" ", "_")

    # 翻译标题生成permalink
    translated = ai.translate(title, "将下列中文标题翻译为英语，用JSON返回，键为english，只返回JSON，不要解释。")
    if not translated or "english" not in translated:
        logging.error("❌❌❌ 翻译标题失败，跳过本轮")
        return None

    # 从内容生成description
    description = ai.generate_abstract_from_title(title, 100)
    if not description:
        logging.error("❌❌❌ 生成摘要失败，跳过本轮")
        return None

    # 随机日期
    start_date = datetime.date(2024, 4, 1)
    end_date = datetime.date.today()
    delta_days = (end_date - start_date).days
    random_date = start_date + datetime.timedelta(days=random.randint(0, delta_days))
    updated_date = random_date + datetime.timedelta(days=random.randint(3, 10))
    published_at = str(random_date)
    updated_at = str(updated_date)

    # 随机tags（3~5个）
    tags = random.sample(POST_TAG_LIST, random.randint(3, 5))
    tags_str = str(tags).replace('"', "'")  # 转成 ['tag1', 'tag2'] 格式

    read_time = random.randint(10, 30)

    front_matter = f"""---
title: '{title}'
description: '{description}'
publishedAt: '{published_at}'
updatedAt: '{updated_at}'
author: '投资猫'
category: 'crypto'
tags: {tags_str}
cover: 'https://images.unsplash.com/photo-1518546305927-5a555bb7020d?w=1200&q=80'
readTime: {read_time}
---
> 作者 投资猫(invest cat)，港美股、币圈从业25年，早年活跃在微博，雪球，推特。A8.5,巅峰持仓800枚BTC， 以"拿住英伟达赚了110倍而著名"，目前专注加密/量化/合约/Web3撸毛/港美股。

"""

    file_path = os.path.join(JIKETOUZI_CRYPTO_DIR, f"{new_title}.mdx")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(front_matter + content)

    logging.info(f"✅✅✅ 极客投资新文章已生成：{file_path}")
    return file_path


def execute_jiketouzi_push():
    logging.info("🚀🚀🚀 开始执行 git add . && git commit && git push ...")
    try:
        result = subprocess.run(
            "git add . && git commit -m '.' && git push -u origin main",
            shell=True,
            cwd=JIKETOUZI_CMD_DIR,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            logging.info(f"✅✅✅ jiketouzi git push 成功！\n{result.stdout}")
            return True
        else:
            error_msg = f"❌❌❌ jiketouzi git push 失败！\n{result.stderr}"
            logging.error(error_msg)
            wechat.send_wechat_notification(error_msg)
            return False
    except Exception as e:
        error_msg = f"❌❌❌ jiketouzi git push 异常：{str(e)}"
        logging.error(error_msg)
        wechat.send_wechat_notification(error_msg)
        return False


def publish_jiketouzi(title, content):
    file_path = create_jiketouzi_post(title, content)
    if not file_path:
        return False
    return execute_jiketouzi_push()


def main():
    counts = load_counts()
    origin_title, origin_content = get_article(counts)

    ai_generated_title = ai.generate_title_from_ai(origin_title)
    if not ai_generated_title:
        logging.error("❌❌❌ AI生成标题失败，跳过本轮")
        return

    ai_generated_content = ai.generate_content_from_ai(origin_content)
    if not ai_generated_content:
        logging.error("❌❌❌ AI生成内容失败，跳过本轮")
        return
    permalink, file_path = create_post(ai_generated_title, ai_generated_content)
    if not file_path:
        return
    success = execute_hexo_push()
    if success:
        counts[origin_title] = counts.get(origin_title, 0) + 1
        save_counts(counts)
        success_msg = f"✅✅✅ 文章《{ai_generated_content}》已发表到黑叶投资网站:heiyetouzi.xyz/{permalink}，当前模板已被发表次数：{counts[origin_title]}\n\n"
        logging.info(success_msg)
        wechat.send_wechat_notification(success_msg)

    jiketouzi_success = publish_jiketouzi(ai_generated_title, ai_generated_content)
    if jiketouzi_success:
        msg = f"✅✅✅ 文章《{ai_generated_title}》已同步发布到 jiketouzi.com"
        logging.info(msg)
        wechat.send_wechat_notification(msg)

if __name__ == "__main__":
    main()