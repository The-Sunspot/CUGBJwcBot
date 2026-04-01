# main.py
from bot import log_, get_jwc_notifications
from mail import sendEmail
import datetime


def main():
    log_.debug("CUGB JWC Bot 任务启动")

    try:
        # 1. 执行爬虫逻辑并获取结果
        has_new, mail_content = get_jwc_notifications()

        # 2. 根据是否有新消息决定操作
        if has_new:
            print("检测到新通知，正在准备发送邮件...")
            subject = f"【有新通知】教务处信息汇报_{datetime.date.today()}"
            sendEmail(mail_content, subject)
            log_.debug("新通知已通过邮件发送")
        else:
            # 如果没有新通知，可以选择仅在本地打印或发送一封“一切正常”的邮件
            print("教务处网站暂无更新。")
            log_.debug("本次运行未发现新通知")

    except Exception as e:
        print(f"程序运行崩溃: {e}")
        log_.error(f"Main模块捕获到未处理异常: {e}")


if __name__ == "__main__":
    main()