# _*_ coding:utf-8 _*_

"""
50 59 7,15,23 * * * jd_joy_reward_new.py
"""

import datetime
import json
import os
import re
import sys
import time

import requests

from multiprocessing import Pool

from jdUtils import COOKIES, printT, USER_AGENT

try:
    from sendNotify import send
except:
    from jdSendNotify import send

JD_JOY_REWARD_NAME = (
    int(os.getenv("JD_JOY_REWARD_NAME")) if os.getenv("JD_JOY_REWARD_NAME") else 500
)

remote_reward = requests.get("https://raw.githubusercontent.com/DovFork/jd-scripts/master/jd_joy_reward.ts").text

invoke_key = re.search(r"&invokeKey=(\w+)&", remote_reward).group(1)


def main(cookie_tuple):
    cookie, validate = cookie_tuple

    account_name = cookie.split("pt_pin=")[-1].strip(";")

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

    url = f"https://jdjoy.jd.com/common/gift/getBeanConfigs?reqSource=h5&invokeKey={invoke_key}&validate={validate}"

    tasks = requests.get(url, headers=headers).json()

    if not tasks["errorMessage"]:
        h = datetime.datetime.now().hour
        config = {}
        if 0 <= h < 8:
            config = tasks["data"]["beanConfigs0"]
        if 8 <= h < 16:
            config = tasks["data"]["beanConfigs8"]
        if 16 <= h < 24:
            config = tasks["data"]["beanConfigs16"]

        for bean in config:
            printT(
                f"账号{account_name}库存信息: {bean['giftName']}({bean['id']})剩余{bean['leftStock']}\n"
            )
            if bean["giftValue"] == JD_JOY_REWARD_NAME:
                while 1:
                    if datetime.datetime.now().second < 30:
                        break
                    time.sleep(0.1)

                printT(f"账号{account_name}: 开始兑换!\n")

                url = f"https://jdjoy.jd.com/common/gift/new/exchange?reqSource=h5&invokeKey={invoke_key}&validate={validate}"
                data = {
                    "buyParam": {"orderSource": "pet", "saleInfoId": bean["id"]},
                    "deviceInfo": {},
                }

                res = requests.post(url, headers=headers, data=json.dumps(data)).json()
                printT(
                    f"账号{account_name}兑换信息: "
                    + str(json.dumps(res, ensure_ascii=False))
                    + "\n"
                )
                if res["errorCode"] == "buy_success":
                    send(
                        "宠汪汪兑换Pro",
                        f"账号{cookie.split('pt_pin=')[1].replace(';', '')}兑换成功: {JD_JOY_REWARD_NAME}豆",
                    )

    else:
        error_message = tasks["errorMessage"]

        send(
            "宠汪汪兑换Pro",
            f"账号{account_name}兑换出错: {error_message}",
        )


if __name__ == "__main__":
    printT("🔔宠汪汪兑换Pro,开始！")

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
                tmp_cookies.append(c)

        COOKIES = tmp_cookies

    valid_account = min(len(COOKIES), len(validates))

    printT(f"共{valid_account}个有效京东账号及验证码")

    mix_input = [(COOKIES[i], validates[i]) for i in range(valid_account)]

    with Pool(valid_account) as p:
        p.map(main, mix_input)
