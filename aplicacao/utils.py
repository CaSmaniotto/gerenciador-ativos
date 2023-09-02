import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from aplicacao import sg

def sendgrid_mail(email_para, mensagem, titulo):
    message = Mail(
        from_email = 'smaniottocaetano@gmail.com',
        to_emails = email_para,
        subject = mensagem,
        html_content = titulo)
        # to_emails='jaod79014@gmail.com',
        # subject='Sending with Twilio SendGrid is Fun',
        # html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        # sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)