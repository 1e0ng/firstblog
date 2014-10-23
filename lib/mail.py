#!/usr/bin/env python
#fileencoding=utf-8

import os
import logging
import smtplib
from email.mime.text import MIMEText

from tornado.options import options


class MailError(Exception):
    pass


def send_via_smtp(to, subject, content):
    msg = MIMEText(content, _subtype="html", _charset="utf-8")

    msg['Subject'] = subject
    msg['From'] = options.smtp_username
    msg['To'] = to

    s = None
    try:
        s = smtplib.SMTP_SSL(options.smtp_host, options.smtp_port)
        s.login(options.smtp_username, options.smtp_password)
        s.sendmail(msg['From'], [to], msg.as_string())
    except Exception as ex:
        logging.warning("send mail failed. detail: %s", str(ex))
        raise MailError(str(ex))
    finally:
        if s:
            s.quit()

def send(to, subject, content):
    SENDMAIL = "/usr/sbin/sendmail" # sendmail location

    FROM = options.smtp_username
    TO = [to]

    SUBJECT = "Welcome to %s" % options.site_name

    TEXT = content

    message = """\
From: %s
To: %s
Subject: %s

%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)

    p = os.popen("%s -t -i -f %s" % (SENDMAIL, FROM), "w")
    p.write(message)
    status = p.close()
    if status:
        logging.error("Sendmail exit status %s", status)
