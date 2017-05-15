import smtplib
from email.mime.text import MIMEText


def send_verification_code(email, verification):
    content = 'Your verification code is {}'.format(verification)
    send_email(email, content)


def send_email(email, content):
    msg = MIMEText(content)
    msg['Subject'] = 'Verification Code'
    msg['From'] = 'tsinghua_noreply@163.com'
    msg['To'] = email
    s = smtplib.SMTP_SSL('smtp.163.com')
    s.login(msg['From'], 'welcome0')
    s.sendmail(msg['From'], [email], msg.as_string())
    s.quit()
