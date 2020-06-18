import smtplib
import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

fromaddr = input(str("Digite seu e-mail: "))
password = getpass.getpass(prompt='Digite sua Senha: ', stream=None)
password = str(password)
toaddr = input(str('Digite o destinatario: '))


msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = input(str('Digite o assunto: '))
body = input(str('Digite o corpo do mensagem e pressione ENTER para confirmar:\n'))
msg.attach(MIMEText(body, 'plain'))


def envia_email(fromaddr, password, msg, toaddr, text):

    filename = "anexo.zip"
    attachment = open("anexo.zip", "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)

    print('\nE-MAIL ENVIADO COM SUCESSO!!!')
    print('QUEM SAO ELES!!! SELVA!!!')

    s.quit()


envia_email(fromaddr, password, msg, toaddr)