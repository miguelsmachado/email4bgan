from tkinter import *
from tkinter import scrolledtext
import time, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

root = Tk()
root.title('SMTP4BGAN')
root.geometry("500x500")

label_sender = Label(root, text="Digite seu e-mail:")
label_sender.pack()
s_mail = Entry(root, width=20)
s_mail.insert(INSERT, "GMAIL")
s_mail.pack()

label_senha = Label(root, text="Digite a senha:")
label_senha.pack()
senha = Entry(root, width=20)
senha.pack()

label_vazio = Label(root, text="")
label_vazio.pack()

label_remail = Label(root, text="Digite o e-mail de destino")
label_remail.pack()
remail = Entry(root, width=20)
remail.pack()

label_assunto = Label(root, text="Digite o assunto:")
label_assunto.pack()
assunto = Entry(root, width=20)
assunto.pack()

label_texto = Label(root, text="Digite a menasagem:")
label_texto.pack()
texto =  scrolledtext.ScrolledText(root, width=50, bd=4, relief="raised")
texto.pack()

label_anexo = Label(root, text="Digite o nome do arquivo a ser anexeado (com extensão):")
label_anexo.pack()
anexo = Entry(root, width=20)
anexo.pack()


def iniciar():
    print(str(texto.get("1.0", END)))


myButton = Button(root, text="Enviar", command=iniciar)
myButton.pack()

root.mainloop()