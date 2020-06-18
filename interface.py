from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time, smtplib

root = Tk()

root.geometry("500x600")
root.title("SMTP4BGAN - V1.1.1")
root.configure(background='black')
root.iconbitmap("fav.ico")

login_frame = Frame(root, width=800, height=200, background="#D3D3D3")
login_frame.pack(side=TOP)

mensagem_frame = Frame(root, width=800, height=495, background="#D3D3D3")
mensagem_frame.pack(side=BOTTOM)

Label(login_frame, text="Dados para Login", bg="#D3D3D3").place(x = 30, y = 30, width=120, height=25)
Label(login_frame, text="E-mail: ", bg="#D3D3D3").place(x = 70, y = 80, width=120, height=25)
Label(login_frame, text="Senha: ", bg="#D3D3D3").place(x = 70, y = 140, width=120, height=25)
s_mail = Entry(login_frame, width=40)
s_mail.place(x = 180, y = 80)
senha = Entry(login_frame, show='*', width=40)
senha.place(x = 180, y = 140)


Label(mensagem_frame, text="Mensagem", bg="#D3D3D3").place(x = 30, y = 30, width=120, height=25)
Label(mensagem_frame, text="E-mail de destino: ", bg="#D3D3D3").place(x = 50, y = 80, width=120, height=25)
Label(mensagem_frame, text="Assunto: ", bg="#D3D3D3").place(x = 75, y = 120, width=120, height=25)
Label(mensagem_frame, text="Corpo do Texto: ", bg="#D3D3D3").place(x = 52, y = 155, width=120, height=25)

remail = Entry(mensagem_frame, width=40)
remail.place(x = 180, y = 80)
assunto = Entry(mensagem_frame, width=40)
assunto.place(x = 180, y = 120)
texto = scrolledtext.ScrolledText(mensagem_frame,width=60,height=10, bd=1, relief=RIDGE,
                                  font=('arial', 14))
texto.place(x=49, y=185)

anexo1_check = IntVar()
anexo1_check.set(False)
anexo1 = Checkbutton(mensagem_frame, text="Anexo", variable=anexo1_check,
                    onvalue=True, offvalue=False, font=('arial', 14), bg="#D3D3D3").place(x = 49, y = 360)

Label(mensagem_frame, text="(O anexo deverá estar na mesma pasta deste executável)",
      bg="#D3D3D3", font=('arial', 10)).place(x = 115, y = 363)

Label(mensagem_frame, text="Nome do anexo: ", bg="#D3D3D3").place(x = 50, y = 390)
anexo = Entry(mensagem_frame, width=40)
anexo.place(x = 180, y = 390)

# -------------------------------------------------------------------------

tentativas = 1
enviado = False
servidor = ""
s_port = 0
email_end = ""
s_email = ""
filename = ""


def main():
    global tentativas
    global enviado
    global servidor
    global s_port
    global email_end
    global s_email
    global filename
    global anexo1

    fromaddr = str(s_mail.get())
    password = str(senha.get())
    toaddr = str(remail.get())

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = str(assunto.get())
    body = str(texto.get("1.0", END))
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()
    tentativa = 1
    enviado = False

    def envia_email(fromaddr, password, msg, toaddr, filename, anexo1):

        global enviado
        global tentativa

        try:
            if anexo1_check == 1:
                attachment = open(str(filename), "rb")
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

            enviado = True
            messagebox.showinfo('SMTP4BGAN', 'E-MAIL ENVIADO COM SUCESSO!!!')
            s.quit()

        except:
            tentativa += 1
            time.sleep(1)

    while not enviado:
        envia_email(fromaddr, password, msg, toaddr, filename, anexo1)

# -------------------------------------------------------------------------

Button(mensagem_frame, text="Enviar", width=10, command=main).place(x=455, y= 440)
Label(mensagem_frame,
      text="Desenvolvido por:\nCap Inf Miguel Sant'Anna Machado\nCap Inf Guilherme André Cassanego\nJunho/2020 - V1.1.1",
      bg="#D3D3D3", justify='left', font=('arial', 10)).place(x=5, y=445)

root.mainloop()