# _*_ coding:utf-8 _*_

import datetime
import os
import random
import re
import sys
import time

import requests

COOKIES = os.getenv("JD_COOKIE").split("&") if os.getenv("JD_COOKIE") else []


def printT(s):
    sys.stdout.write(
        "[{0}]: {1}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), s)
    )
    sys.stdout.flush()


def USER_AGENT():
    uuid = "".join(
        random.sample(
            "123456789abcdef123456789abcdef123456789abcdef123456789abcdef", 40
        )
    )
    addressid = "".join(random.sample("1234567898647", 10))
    iosVer = "".join(
        random.sample(
            [
                "14.5.1",
                "14.4",
                "14.3",
                "14.2",
                "14.1",
                "14.0.1",
                "13.7",
                "13.1.2",
                "13.1.1",
            ],
            1,
        )
    )
    iosV = iosVer.replace(".", "_")
    iPhone = "".join(random.sample(["8", "9", "10", "11", "12", "13"], 1))
    ADID = (
        "".join(random.sample("0987654321ABCDEF", 8))
        + "-"
        + "".join(random.sample("0987654321ABCDEF", 4))
        + "-"
        + "".join(random.sample("0987654321ABCDEF", 4))
        + "-"
        + "".join(random.sample("0987654321ABCDEF", 4))
        + "-"
        + "".join(random.sample("0987654321ABCDEF", 12))
    )

    return f"jdapp;iPhone;10.0.4;{iosVer};{uuid};network/wifi;ADID/{ADID};model/iPhone{iPhone},1;addressid/{addressid};appBuild/167707;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS {iosV} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/null;supportJDSHWK/1"


def checkCookie(cookie):
    url = "https://me-api.jd.com/user_new/info/GetJDUserInfoUnion"
    headers = {
        "Host": "me-api.jd.com",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "User-Agent": USER_AGENT(),
        "Accept-Language": "zh-cn",
        "Referer": "https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&",
        "Accept-Encoding": "gzip, deflate, br",
    }
    res = requests.get(url, headers=headers)
    data = res.json()
    if data["retcode"] == "1001":
        return False
    return True


def getEnvs(token):
    api_endpoint = "http://localhost:5600/api/envs?t=" + str(int(time.time()))
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer " + token,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "http://localhost:5700",
        "Referer": "http://localhost:5700/env",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    }

    envs = requests.get(api_endpoint, headers=headers).json()

    return envs


def putEnv(token, env):
    put_data = {
        "name": env["name"],
        "remarks": env["remarks"],
        "value": env["value"],
        "_id": env["_id"],
    }
    api_endpoint = "http://localhost:5600/api/envs?t=" + str(int(time.time()))
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer " + token,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "http://localhost:5700",
        "Referer": "http://localhost:5700/env",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    }

    resp = requests.put(
        api_endpoint,
        headers=headers,
        data=json.dumps(put_data, ensure_ascii=False).encode("utf-8"),
    ).json()
    if resp["code"] == 200:
        return True
    return False


if __name__ == "__main__":
    print(USER_AGENT())
