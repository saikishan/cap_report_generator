import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
#from codehub.config import get_config

class PostMan:
    config_data = {
        "email_sender": "codehub.sender@gmail.com",
        "password": "pythonc++",
        "default": None,
    }
    developers = ['saikishan2008@gmail.com', '15pa1a05d0@vishnu.edu.in']

    def __init__(self, source, server='smtp.gmail.com', port=587):
        self.source = source+" - "
        self.smtp = smtplib.SMTP(server, port)
        self.smtp.starttls()
        self.smtp.login(self.config_data["email_sender"], self.config_data["password"])

    def send_mail(self, send_to, subject, text, files=None):
        # assert isinstance(send_to, list)
        send_from = self.config_data["email_sender"]
        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = COMMASPACE.join(send_to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = self.source + subject

        msg.attach(MIMEText(text))

        for f in files or []:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)
        self.smtp.sendmail(send_from, send_to, msg.as_string())

    def __del__(self):
        self.smtp.close()

    def developer_alert(self, subject, text, files=None):
        for x in self.developers:
            self.send_mail(x, subject=subject, text=text, files=files)