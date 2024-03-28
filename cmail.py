import  smtplib
from smtplib import SMTP
from email.message import EmailMessage
def sendmail(to,subject,body):
    server=smtplib.SMTP_SSL("smtp.gmail.com",465)    
    server.login("devipriyanka9227@gmail.com","phps eedo ojko hstp")
    msg=EmailMessage()
    msg["from"]="devipriyanka9227@gmail.com"
    msg["subject"]=subject
    msg["TO"]=to
    msg.set_content(body)
    server.send_message(msg)
    server.quit()                                                                                                                              