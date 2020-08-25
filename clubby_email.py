import smtplib

from db import db, InfoSession, Position, Club, Student

contacts = []
students = Student.query.all()
for s in students:
    contacts.append(s.email)
EMAIL_ADDRESS = 'cw655@cornell.edu'
EMAIL_PASSWORD = 'jaayoaduebnvenkv'


smtplibObj = smtplib.SMTP('smtp.gmail.com', 587)
smtplibObj.ehlo()
smtplibObj.starttls()
smtplibObj.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

subject = 'Clubby Email Notification'
body = 'Clubby email notification is working now.'

msg = f'Subject: {subject}\n\n{body}'

for a in contacts:
    smtplibObj.sendmail(EMAIL_ADDRESS, a, msg)
