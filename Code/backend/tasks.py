from celery import shared_task
import smtplib
from celery.schedules import crontab
from models import db, Sum, Cart, Item, User
import time
from app import cel_app
import datetime
from io import StringIO
import csv
from jinja2 import Template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import pdfkit
from email import encoders




@cel_app.task
def add(a,b):
    time.sleep(5)
    return a+b


@cel_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    #sender.add_periodic_task(crontab(minute=0,hour=0), daily_reminder.s())
    #sender.add_periodic_task(crontab(minute=0,hour=0,day_of_month=1), monthly_reminder.s())
    sender.add_periodic_task(10, daily_reminder.s())
    sender.add_periodic_task(10, monthly_reminder.s())


@cel_app.task
def daily_reminder():
    items = Cart.query.filter(Cart.time>=datetime.date.today()).all()
    userid = []
    for item in items :
        userid.append(item.user_id)

    users= User.query.filter(User.id.not_in(userid)).all()
    for user in users:
        message= MIMEMultipart()
        message["From"]="ree@gmail.com"
        message["To"]=user.email
        message["Subject"]="Daily reminder"
        message.attach(MIMEText("Dear user,\n We are missing you!"))
        with smtplib.SMTP("localhost", 1025) as server:
            server.login("sender_email", "password")
            server.sendmail("sender_email", user.email, message.as_string())



@cel_app.task
def monthly_reminder():
    admin= User.query.filter_by(userType='admin').first()
    items= Item.query.all()
    rows=[]

    for item in items:
        item_purchase=Cart.query.filter_by(item_id=item.id).all()
        total=0
        for each in item_purchase:
            total+= each.quantity
        row = {
             "id":item.id,
             "name":item.name,
             "description":item.description,
             "manufacture_date":item.manufacture_date,
             "expiry_date":item.expiry_date,
             "price":item.price,
             "rate_per_unit":item.rate_per_unit,
             "tags":item.tags,
             "iimg":item.iimg,
             "item_in_stock":item.item_in_stock,
             "category_id":item.category_id,
             "category_name": item.category.name,
             "total":total
        }
        rows.append(row)
    with open ("templates/report.html") as file:
        template=Template(file.read())
        month=datetime.date.today().strftime("%B")
        result=template.render(items=rows, month=month)

    message= MIMEMultipart()
    message["From"]="ree@gmail.com"
    message["To"]=admin.email
    message["Subject"]="Monthly Report"
    html_report= MIMEText(result,"html")
    html_report.add_header("Content-Disposition", f"attachment; filename={month}.html")
    message.attach(html_report)


    content= pdfkit.from_string(result, False)
    pdf_report = MIMEBase("application", "octet-stream")
    pdf_report.set_payload(content)
    encoders.encode_base64(pdf_report)
    pdf_report.add_header("Content-Disposition", f"attachment; filename={month}.pdf")
    message.attach(pdf_report)
    
    

    with smtplib.SMTP("localhost", 1025) as server:
        server.login("sender_email", "password")
        server.sendmail("sender_email", admin.email,message.as_string())


daily_reminder()        
monthly_reminder()
