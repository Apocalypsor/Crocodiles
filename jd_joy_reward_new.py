"""
50 59 7,15,23 * * * jd_joy_reward_new.py
"""

import datetime
import json
import os
import sys
import threading
import time

import requests

from jdUtils import COOKIES, JD_JOY_REWARD_NAME, USER_AGENT

try:
    from sendNotify import send
except:
    from jdSendNotify import send


def main(cookie, validate):
    headers = {
        "Host": "jdjoy.jd.com",
        "accept": "*/*",
        "content-type": "application/json",
        "origin": "https://h5.m.jd.com",
        "User-Agent": USER_AGENT(),
        "referer": "https://jdjoy.jd.com/",
        "accept-language": "zh-cn",
        "cookie": cookie,
    }
    url = f"https://jdjoy.jd.com/common/gift/getBeanConfigs?reqSource=h5&invokeKey=qRKHmL4sna8ZOP9F&validate={validate}"
    tasks = requests.get(url, headers=headers).json()
    h = datetime.datetime.now().hour
    config = {}
    if 0 <= h < 8:
        config = tasks["data"]["beanConfigs0"]
    if 8 <= h < 16:
        config = tasks["data"]["beanConfigs8"]
    if 16 <= h < 24:
        config = tasks["data"]["beanConfigs16"]

    for bean in config:
        sys.stdout.write(f"{bean['id']} {bean['giftName']} {bean['leftStock']}\n")
        if bean["giftValue"] == JD_JOY_REWARD_NAME:
            while 1:
                if datetime.datetime.now().second < 30:
                    break
                time.sleep(0.1)
            sys.stdout.write("exchange()\n")
            url = f"https://jdjoy.jd.com/common/gift/new/exchange?reqSource=h5&invokeKey=qRKHmL4sna8ZOP9F&validate={validate}"
            data = {
                "buyParam": {"orderSource": "pet", "saleInfoId": bean["id"]},
                "deviceInfo": {},
            }
            res = requests.post(url, headers=headers, data=json.dumps(data)).json()
            sys.stdout.write(json.dumps(res, ensure_ascii=False) + "\n")
            if res["errorCode"] == "buy_success":
                sys.stdout.write(
                    f"cookie{cookie.split('pt_pin=')[1].replace(';', '')}兑换成功\n"
                )
                send(
                    "宠汪汪兑换Pro",
                    f"Cookie {cookie.split('pt_pin=')[1].replace(';', '')} 兑换成功 {JD_JOY_REWARD_NAME}",
                )
    lock.release()


if __name__ == "__main__":
    print("🔔宠汪汪兑换Pro,开始！")
    lock = threading.BoundedSemaphore(20)
    if "test" in os.getcwd():
        path = ".."
    else:
        path = "."
    with open(f"{path}/validate.txt", encoding="utf-8") as f:
        validates = f.read().split("\n")

    if os.getenv("JOY_BEAN_PINS"):
        validate_pins = os.getenv("JOY_BEAN_PINS").split(",")
        tmp_cookies = []
        for c in COOKIES:
            if c.split("pt_pin=")[-1].rstrip().rstrip(";") in validate_pins:
                tmp_cookies.append("c")

        COOKIES = tmp_cookies

    print(f"====================共{len(COOKIES)}个京东账号Cookie=========")
    for i in range(min(len(validates), len(COOKIES))):
        lock.acquire()
        threading.Thread(target=main, args=(COOKIES[i], validates[i])).start()
