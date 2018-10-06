# -*- coding: utf-8 -*-
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

def send_email(email, password, email_dest, log_path):
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = COMMASPACE.join(email_dest)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = u'Log Geogig'

    msg.attach(MIMEText(u'Segue log em anexo!'))

    for f in [log_path]:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email_dest, msg.as_string())
    server.close()