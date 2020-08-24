import smtplib
import time
EMAIL_ADDRESS = 'cw655@cornell.edu'
EMAIL_PASSWORD = 'jaayoaduebnvenkv'


smtplibObj = smtplib.SMTP('smtp.gmail.com', 587)
smtplibObj.ehlo()
smtplibObj.starttls()
smtplibObj.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

subject = 'Clubby Email Notification'
body = 'Clubby email notification is working now.'

msg = f'Subject: {subject}\n\n{body}'

smtplibObj.sendmail(EMAIL_ADDRESS, 'rz327@cornell.edu', msg)
