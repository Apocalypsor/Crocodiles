# _*_ coding:utf-8 _*_

"""
23 * * * * jd_cleancookies.py
"""

import json
import os
import re

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
