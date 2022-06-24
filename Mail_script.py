import sys, os, time, threading, subprocess,datetime
import re
import smtplib
from email.mime.text import MIMEText
import psycopg2
from datetime import date

#postgresql connection
POSTGRES_HOST="3.227.146.142"
POSTGRES_DATABASE="gdh_prod"
POSTGRES_USER="gdh_prod_jobs"
POSTGRES_PASSWORD="Jobs@GDHProd_2021"

conn = psycopg2.connect(host=POSTGRES_HOST, database=POSTGRES_DATABASE, user=POSTGRES_USER, password=POSTGRES_PASSWORD)
cur = conn.cursor()

def test():
    query = """select gro.order_id, cm.unique_identifier_1 as cin, cm.name as entity_name, gro.order_status
                from config.gdh_report_orders gro 
                inner join dbo.company_master cm 
                on gro.company_id = cm.company_id 
                inner join dbo.dim_tenant dt
                on dt.tenant_id = gro.tenant_id where gro.aud_date::date = Now()::date""" 
    cur.execute(query)
    data = cur.fetchall()
    print(data)
    #result = [dict(row) for row in data]
    table=[]
    for row in data:
        message = """<table width="60%" style="text-align: center;"><col style="width:5%"><col style="width:30%"><col style="width:50%"><col style="width:5%"><tr><td style="text-align:center">{0}</td><td style="text-align:center;">{1}</td><td style="text-align:center;">{2}</td><td style="text-align:center;">{3}</td></tr></table>""".format(row[0],row[1],row[2],row[3])
        table.append(message)

    sender = 'shubhamnachare08@gmail.com'
    passward = 'viipnljkzumfbbfj'
    receivers = ["shubham@mosaikanalytics.com"]
    subject = """51Rc Reports due on {0}""".format(date.today().strftime("%d/%m/%Y"))
    
    body_no= """<!DOCTYPE html>
                <html lang="en-US">
                    <body>
                        <h4 style="font-weight:100;">Dear User,<br><br>
                        No reports are due today.
                        <br>
                        <br>
                        Regards,<br>
                        GDH Support Team.</h4>
                        <br>
                        This is a system-generated email, and this inbox is not monitored. For any support queries, please reach out to support@mosaikanalytics.com
                    </body>
                <html>"""

    body = """<!DOCTYPE html>
                <html lang="en-US">
                    <body>
                        Hi All,<br><br>
                        Below are the reports due for today.
                        <div id="table content">
                        <table width=60%" style="text-align: center;"><tr><th style="width:5%">Orderd Id</th><th style="width:30%">Cin</th><th style="width:50%">Name</th><th style="width:5%">Order Status</th></tr></table>
                        {0}
                        </div>
                        <br>
                        <br>
                        Regards,<br>
                        GDH Support Team.
                        <br>
                        <br>
                        This is a system-generated email, and this inbox is not monitored. For any support queries, please reach out to support@mosaikanalytics.com
                    </body>
                <html>""".format(''.join(table))

    if data:
        msg=MIMEText(body,"html")
    else:
        msg=MIMEText(body_no,"html")
    msg['Subject']=subject
    msg['From']=sender
    msg['To']=', '.join(receivers)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(sender,passward)
        server.sendmail(sender, receivers, msg.as_string())
        server.close()
        print('Successfully sent email')
    except Exception as e:
        print('Something went wrong...', e)

    return ({"status": "success"}), 200
print(test())
