import datetime
import logging
import os
import random
import json
import re
import subprocess
from .constants import SILICONFLOW_API_KEY, SILICONFLOW_BASE_URL,AI_MODEL

# apt update
# apt install python3-pip
# pip3.11 install openai --break-system-packages
from openai import OpenAI
from . import wechat
# python3.11 -m pip install openai-whisper --break-system-packages
# import whisper

LOG_NAME = "../auto.log"
VIDEO_OUTPUT_PATH = "./"

logging.basicConfig(
    format="%(asctime)s - INFO - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_NAME, encoding="utf-8", mode="a")
    ]
)

client = OpenAI(
    api_key=SILICONFLOW_API_KEY,
    base_url=SILICONFLOW_BASE_URL,
)


# 根据文章老标题-->生成新标题
def generate_title_from_ai(origin_title):
    logging.info(f"💡💡💡 正在向AI生成新的标题中, 原文章标题: {origin_title}")
    
    try:
        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"返回1个跟我给定的标题差不多意思的标题，只返回结果，不要解释，也不要加任何标点或修饰语。标题是：{origin_title}。"},
            ],
            stream=False,
            temperature=0.6
        )

        if not response or not hasattr(response, "choices") or not response.choices:
            wechat.send_wechat_notification(f"❌❌❌ 【ai.py】AI返回结果为空或格式不对，请检查... 原始标题：{origin_title}，response内容：{repr(response)}")
            return ""

        title = response.choices[0].message.content.strip()
        striped_title = "\n".join([line.strip() for line in title.splitlines() if line.strip()])
        logging.info(f"✅✅✅ 【ai.py】AI生成标题成功：{striped_title}")
        return striped_title.replace(" ", ":")

    except Exception as e:
        error_message = f"❌❌❌ AI生成标题失败，原始标题：{origin_title}\n错误详情：{str(e)}"
        logging.error(error_message)
        wechat.send_wechat_notification(error_message)
        return ""  

#  根据文章老内容 --> 生成新内容
def generate_content_from_ai(origin_content):
    try:
        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业的文本改写助手，严格遵循以下规则：\n"
                               "1. 保留原文所有 **Markdown 格式**（如 ###、**、- 列表等）\n"
                               "2. **绝不修改任何链接**（包括图片链接和注册链接）\n"
                               "3. 保持原文结构和信息完整\n"
                               "4. 只返回改写后的文本，不要额外解释"
                },
                {
                    "role": "user",
                    "content": f"{origin_content}"
                }
            ],
            temperature=0.3, 
            stream=False     
        )
        if not response or not hasattr(response, "choices") or not response.choices:
            wechat.send_wechat_notification(f"❌❌❌ 【ai.py】 AI返回文章内容为空或格式不对，请检查...，response内容：{repr(response)}")
            return ""

        content = response.choices[0].message.content.strip()
        logging.info(f"✅✅✅ 【ai.py】 AI生成文章内容成功：{content[:50]}...")
        return content

    except Exception as e:
        error_message = f"❌❌❌ 【ai.py】 AI生成文章内容失败，请检查...\n错误详情：{str(e)}"
        logging.error(error_message)
        wechat.send_wechat_notification(error_message)
        return ""  

# 根据文章标题 --> 生成摘要
def generate_abstract_from_title(title, max_words):
    logging.info(f"💡💡💡 【ai.py】 正在向AI根据标题生成摘要中, 文章标题: {title}")
    min_words = max_words/2
    try:
        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"根据给你的文章标题，返回{min_words}到{max_words}字之间的摘要，只返回结果，不要解释，也不要加任何标点或修饰语。标题是：{title}。"},
            ],
            stream=False,
            temperature=0.6
        )

        if not response or not hasattr(response, "choices") or not response.choices:
            wechat.send_wechat_notification(f"❌❌❌ 【ai.py】AI返回结果为空或格式不对，请检查... 原始标题：{title}，response内容：{repr(response)}")
            return ""

        abstract = response.choices[0].message.content.strip()
        striped_abstract = "\n".join([line.strip() for line in abstract.splitlines() if line.strip()])
        logging.info(f"✅✅✅ 【ai.py】AI根据文章标题生成摘要成功：{striped_abstract}")
        return striped_abstract
    except Exception as e:
        error_message = f"❌❌❌ 【ai.py】AI根据标题生成摘要失败，标题：{title}\n错误详情：{str(e)}"
        logging.error(error_message)
        wechat.send_wechat_notification(error_message)
        return ""  

def clean_json_codeblock(text):
    # 去除 markdown 中的 ```json 或 ``` 包裹
    return re.sub(r"^```(?:json)?\n?|```$", "", text.strip(), flags=re.IGNORECASE)


def translate(content, instruction="将下列内容翻译为英语，用JSON返回，键为english，只返回JSON，内容中符号或链接不要翻译，也不要解释。"):
    logging.info("🔄 正在向AI请求翻译...")
    try:
        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{instruction}\n\n{content}"},
            ],
            stream=False,
            temperature=0.6
        )

        if not response or not hasattr(response, "choices") or not response.choices:
            wechat.send_wechat_notification(f"❌【AI翻译】返回为空，请检查。response: {repr(response)}")
            return {}

        t_content = response.choices[0].message.content.strip()

        if t_content.startswith("```json"):
            t_content = t_content.replace("```json", "").replace("```", "").strip()

        logging.info("✅ AI翻译成功")
        return json.loads(t_content)

    except Exception as e:
        error_message = f"❌【AI翻译失败】：{str(e)}"
        logging.error(error_message)
        wechat.send_wechat_notification(error_message)
        return {}

def extract_audio(video_path, audio_path="temp_audio.wav"):
    """使用 ffmpeg 从视频中提取音频"""
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", audio_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    logging.info(f"音频已提取到 {audio_path}")
    return audio_path

def transcribe_audio(audio_path):
    """使用 Whisper 模型进行语音识别"""
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    logging.info("语音识别完成")
    return result['text']

def summarize_to_markdown(text):
    """调用 SiliconFlow API 进行总结和 Markdown 化"""
    system_prompt = (
        "你是一位优秀的内容创作者，请将以下视频逐字稿整理为一篇结构清晰的Markdown文章，"
        "包括合适的标题、小节、要点，语言通顺，逻辑清晰："
    )
    response = client.chat.completions.create(
        model=AI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        temperature=0.7
    )
    markdown_output = response.choices[0].message.content
    logging.info("生成 Markdown 成功")
    return markdown_output

def save_markdown(content, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    logging.info(f"Markdown 已保存到 {output_path}")

def video_to_markdown(video_path):
    try:
        logging.info(f"开始处理视频：{video_path}")
        audio_path = extract_audio(video_path)
        transcript = transcribe_audio(audio_path)
        markdown = summarize_to_markdown(transcript)
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        output_path = f"{base_name}_{date_str}.md"
        save_markdown(markdown, output_path)
    except Exception as e:
        logging.error(f"处理失败：{e}")   
          