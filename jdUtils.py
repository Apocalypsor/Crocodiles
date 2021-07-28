import datetime
import os
import random
import re
import sys

JD_JOY_REWARD_NAME = (
    int(os.getenv("JD_JOY_REWARD_NAME")) if os.getenv("JD_JOY_REWARD_NAME") else 500
)

COOKIES = os.getenv("JD_COOKIE").split("&") if os.getenv("JD_COOKIE") else []


def printT(s):
    print("[{0}]: {1}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), s))
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


if __name__ == "__main__":
    print(USER_AGENT())
