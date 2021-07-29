# _*_ coding:utf-8 _*_

"""
23 * * * * jd_cleancookies.py
"""

import json
import os
import re
import time

import requests

from jdUtils import printT, USER_AGENT

try:
    from sendNotify import send
except:
    from jdSendNotify import send


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
        api_endpoint, headers=headers, data=json.dumps(put_data, ensure_ascii=False).encode('utf-8')
    ).json()
    if resp["code"] == 200:
        return True
    return False


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


def main(token):
    remark_regex = os.getenv("CLEAN_REMARK_REGEX")

    if not remark_regex:
        printT("缺少备注匹配正则!")
    else:
        remark_regex_obj = re.compile(remark_regex)
        printT("开始获取JD_COOKIE环境变量")
        envs = getEnvs(token)
        cookies_env = []

        for e in envs["data"]:
            if e["name"] == "JD_COOKIE" and remark_regex_obj.search(e["remarks"]):
                cookies_env.append(e)

        for cookies in cookies_env:
            printT("开始检测Cookie状态 (" + cookies["remarks"] + ")")

            cks = cookies["value"].split("&")
            valid_cks = []
            for c in cks:
                if checkCookie(c):
                    valid_cks.append(c)
                else:
                    ck_name = c.split("pt_pin=")[-1].rstrip(";")
                    printT(c + " 已失效")
                    send("失效Cookie自动清理", f"Cookie {ck_name} 已失效")

            if len(valid_cks) != len(cks):
                printT("检测到Cookie失效 (" + cookies["remarks"] + ")")
                cookies["value"] = "&".join(valid_cks)
                if putEnv(token, cookies):
                    printT("自动替换Cookie成功 (" + cookies["remarks"] + ")")
                else:
                    printT("自动替换Cookie失败 (" + cookies["remarks"] + ")")


if __name__ == "__main__":
    ql_path = "/ql"
    auth_file = ql_path + "/config/auth.json"
    with open(auth_file, "r") as f:
        token = json.load(f)["token"]

    main(token)
