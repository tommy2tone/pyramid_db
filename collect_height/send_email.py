from email.mime.text import MIMEText
import smtplib


def send_email(email, height, average_height, count):
    from_email = "thomas.hildebrand11@gmail.com"
    from_pw = "@Testing1234"
    to_email = email

    subject = "Height Data"
    message = "Hey there, your height is <strong>%s</strong> inches. <br> " \
              "The average height from <strong>%s</strong> entries is <strong>%s</strong> inches. <br>" \
              "Thanks!" % (height, count, average_height)
    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email

    gmail = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    gmail.login(from_email, from_pw)
    gmail.send_message(msg, from_email, to_email)
    gmail.quit()