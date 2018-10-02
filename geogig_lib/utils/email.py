# -*- coding: utf-8 -*-
import smtplib

def send_email(email, password, msg, email_dest):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email_dest, msg)
    server.quit()