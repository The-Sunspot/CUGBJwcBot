import datetime


# 获取当前系统日期和某个日期的差值
def get_date_diff(date_str: str) -> int:
    now = datetime.datetime.now()
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    diff = date - now
    return abs(diff.days)


kaoYan23 = "2022-12-24"
liuJi22s = "2022-06-11"


def getFooterTxt():
    # 打开out.txt文件
    f = open("footer.txt", "w", encoding="utf-8")
    f.write("\n---------------------------------\n")
    f.write("距离四六级考试还有" + str(get_date_diff(liuJi22s)) + "天\n")
    f.write("距离2023考研初试还有" + str(get_date_diff(kaoYan23)) + "天\n")
    f.write("本周是学期第" + str(getWeeks()) + "周\n")


def getWeeks() -> int:
    diff = get_date_diff("2022-04-25")
    print(diff)
    return (diff // 7) + 10
