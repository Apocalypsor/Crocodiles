# _*_ coding:utf-8 _*_

"""
19 * * * * cro_crawlcks.py
"""

import json
import os
import re

import requests

from jdUtils import checkCookie, getEnvs, putEnv, printT

try:
    from sendNotify import send
except:
    from jdSendNotify import send


def main(token):
    remark_regex = os.getenv("CLEAN_REMARK_REGEX")

    if not remark_regex:
        printT("缺少备注匹配正则!")
    else:
        remark_regex_obj = re.compile(remark_regex)
        printT("开始获取JD_COOKIE环境变量")
        envs = getEnvs(token)
        cookies_env = None

        for e in envs["data"]:
            if e["name"] == "JD_COOKIE" and remark_regex_obj.search(e["remarks"]):
                cookies_env = e
                break

        jd_cookies = os.getenv("JD_COOKIE").split("&")
        new_cookies = cookies_env["value"].rstrip("&")

        urls = []
        for env in os.environ:
            if "CRO_CRAWL_URL" in env:
                urls.append(os.environ[env])

        for u in urls:
            printT(f"开始爬取 {u}")
            resp = requests.get(u).json()

            if resp.get("data"):
                for d in resp["data"]:
                    if (
                        d.get("value")
                        and d["value"] not in jd_cookies
                        and checkCookie(d["value"])
                    ):
                        jd_cookies.append(d["value"])

                        ck_name = d["value"].split("pt_pin=")[-1].rstrip(";")
                        send("自动爬取Cookie", f"自动添加有效Cookie: {ck_name}")
                        new_cookies += "&" + d["value"]

        if cookies_env["value"].rstrip("&") != new_cookies:
            cookies_env["value"] = new_cookies
            if putEnv(token, cookies_env):
                printT("自动替换Cookie成功 (" + cookies_env["remarks"] + ")")
            else:
                printT("自动替换Cookie失败 (" + cookies_env["remarks"] + ")")


if __name__ == "__main__":
    ql_path = "/ql"
    auth_file = ql_path + "/config/auth.json"
    with open(auth_file, "r") as f:
        token = json.load(f)["token"]

    main(token)
