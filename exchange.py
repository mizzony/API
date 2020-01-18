import requests  #to get api using method get
import smtplib  # defines an SMTP client session object that can be used to send mail to any Internet machine with an SMTP or ESMTP listener daemon.
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

print("Start fetch exchange")

def main():
    response = requests.get('https://api.exchangeratesapi.io/latest?base=USD')
    json_response = response.json()
    print('data on ' + json_response['date'])

    subject = 'Exchange rate of ' + json_response['date']

#normally in older version of python you use .format but in py3.6 version you can use just f
    body = f"""<html>
    <head></head>
    <body>
      <h1>Exchange rate of {json_response['date']}</h1>
      <p>Base: {json_response['base']}<p>
      <table style="border-collapse: collapse; border: 1px solid black;">
        <tr><th style="border: 1px solid black">Currency</th><th style="border: 1px solid black">Rate</th></tr>"""

    for currency, rate in json_response['rates'].items():
        body += f"""
            <tr>
                <td style="border: 1px solid black">{currency}</td>
                <td style="border: 1px solid black">{rate}</td>
            </tr>
        """

    body += """</table></body></html>"""

    sendmail('sthanombun@gmail.com', subject, body)


def sendmail (recipient, subject, body_html):
    print("Start send email")
    # Replace sender@example.com with your "From" address. 
    # This address must be verified.
    SENDER = 'sup.harrots@gmail.com'  
    SENDERNAME = 'Support Harrots'

    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT  = recipient

    # Replace smtp_username with your Amazon SES SMTP user name.
    USERNAME_SMTP = "AKIARQT5HOHUPBAXTLTZ"

    # Replace smtp_password with your Amazon SES SMTP password.
    PASSWORD_SMTP = "BGSHu8/V/TfFfVO+4GM9wTzVsktozlWTlx7Gvb+sJE1b"

    # If you're using Amazon SES in an AWS Region other than US West (Oregon), 
    # replace email-smtp.us-west-2.amazonaws.com with the Amazon SES SMTP  
    # endpoint in the appropriate region.
    HOST = "email-smtp.ap-south-1.amazonaws.com"
    PORT = 587

    # The subject line of the email.
    SUBJECT = subject

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = "Open via GMail"

    # The HTML body of the email.
    BODY_HTML = body_html

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
    msg['To'] = RECIPIENT

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(BODY_TEXT, 'plain')
    part2 = MIMEText(BODY_HTML, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Try to send the message.
    try:  
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        server.starttls()
        #stmplib docs recommend calling ehlo() before & after starttls()
        server.ehlo()
        server.login(USERNAME_SMTP, PASSWORD_SMTP)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())
        server.close()
    # Display an error message if something goes wrong.
    except Exception as e:
        print ("Error: ", e)
    else:
        print ("Email sent!")


if __name__ == '__main__':
    main()