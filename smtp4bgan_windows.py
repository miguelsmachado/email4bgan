from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time, smtplib

root = Tk()

root.geometry("480x570")
root.title("SMTP4BGAN - V1.1.1")
root.configure(background='#D3D3D3')
root.iconbitmap("fav.ico")
root.resizable(height=False, width=False)

Label(root, text="Dados para Login", bg="#D3D3D3").place(x = 10, y = 10, width=120, height=25)
Label(root, text="E-mail: ", bg="#D3D3D3").place(x = 45, y = 40, width=120, height=25)
Label(root, text="Senha: ", bg="#D3D3D3").place(x = 45, y = 80, width=120, height=25)
s_mail = Entry(root, width=35)
s_mail.place(x=135, y=40)
senha = Entry(root, show='*', width=35)
senha.place(x=135, y=80)


Label(root, text="Mensagem", bg="#D3D3D3").place(x=10, y=130, width=120, height=25)
Label(root, text="E-mail de destino: ", bg="#D3D3D3").place(x = 10, y = 160, width=120, height=25)
Label(root, text="Assunto: ", bg="#D3D3D3").place(x = 37, y = 200, width=120, height=25)
Label(root, text="Corpo do Texto: ", bg="#D3D3D3").place(x = 12, y = 240, width=120, height=25)

remail = Entry(root, width=35)
remail.place(x = 135, y = 160)
assunto = Entry(root, width=35)
assunto.place(x = 135, y = 200)
texto = scrolledtext.ScrolledText(root,width=60,height=12, bd=1, relief=RIDGE)
texto.place(x=15, y=265)

anexo1_check = IntVar()
anexo1_check.set(False)
anexo1 = Checkbutton(root, text="Anexo", variable=anexo1_check,
                    onvalue=True, offvalue=False, bg="#D3D3D3").place(x = 15, y = 445)

filename = ""


def anexo():
    global filename
    filename = askopenfilename()
    Label(root, text=filename, bg="#D3D3D3", justify=RIGHT).place(x=15, y=470, height=25)

# -------------------------------------------------------------------------

tentativas = 1
enviado = False
servidor = ""
s_port = 0
email_end = ""
s_email = ""


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
            if anexo1_check.get() == 1:
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
        print(filename)
        if anexo1_check.get() == 1:
            print("[*] - E-mail com anexo.")
        print(f"[*] - {tentativa}a tentativa... (pressione Ctrl + C para cancelar)")
        envia_email(fromaddr, password, msg, toaddr, filename, anexo1)


# -------------------------------------------------------------------------
Button(root, text="Selecionar", width=10, command=anexo).place(x = 90, y = 445)
Button(root, text="Enviar", width=10, command=main).place(x=370, y= 530)
Label(root,
      text="Desenvolvido por:\nCap Inf Miguel Sant'Anna Machado\nCap Inf Guilherme André Cassanego\nJunho/2020 - V1.1.1",
      bg="#D3D3D3", justify='left').place(x=5, y=500)

root.mainloop()