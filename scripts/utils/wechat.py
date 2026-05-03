import logging
import requests
LOG_NAME = "auto.log"
from .constants import WECHAT_WEBHOOK_KEY

logging.basicConfig(
    format="%(asctime)s - INFO - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=LOG_NAME,        
    filemode="a"               
)


def send_wechat_notification(message):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={WECHAT_WEBHOOK_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        logging.info(f"📦📦📦 【wechat.py] {message}")
        logging.info(f"📦📦📦 【wechat.py] {response.text}")
    except Exception as e:
        logging.error(f"❌❌❌ 【wechat.py] 发送WeChat通知失败: {e}")