import sys, getopt, time, smtplib, getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# definindo algumas variaveis
tentativas = 1
enviado = False
servidor = ""
s_port = 0
email_end = ""
s_email = ""
anexo = False
filename = ""


def usage():
    print()
    print("________________________________________________________________________________________________")
    print("|  ######  ##     ## ######## ########     ##           ########   ######      ###    ##    ## |")
    print("| ##    ## ###   ###    ##    ##     ##    ##    ##     ##     ## ##    ##    ## ##   ###   ## |")
    print("| ##       #### ####    ##    ##     ##    ##    ##     ##     ## ##         ##   ##  ####  ## |")
    print("|  ######  ## ### ##    ##    ########     ##    ##     ########  ##   #### ##     ## ## ## ## |")
    print("|       ## ##     ##    ##    ##           #########    ##     ## ##    ##  ######### ##  #### |")
    print("| ##    ## ##     ##    ##    ##                 ##     ##     ## ##    ##  ##     ## ##   ### |")
    print("|  ######  ##     ##    ##    ##                 ##     ########   ######   ##     ## ##    ## |")
    print("|______________________________________________________________________________________________|")
    print("                                                  ______________________________________________")
    print("                                                 | Developed by: Cap. Miguel Sant'Anna Machado |")
    print("                                                 |              Cap. Guilherme Andre Cassanego |")
    print("                                                 |                           Maio/2020 - V 2.0 |")
    print("                                                 |_____________________________________________|")
    print()
    print()
    print("modo de uso: email4bgan.py -s servidor_de_email -u nome_do_usuario -a arquivo.ext")
    print()
    print("-s --servidor       - servidor da conta de email (gmail, hotmail, yahoo)")
    print("-u --username       - usuario da conta email. Ex: fulano@email.com -> fulano")
    print("-a --anexo          - nome do arquivo em anexo")
    print("                      deve conter a extensão do arquivo. Ex: anexo.zip")
    print("                      o arquivo deve estar na mesma pasta do executável")
    print("                      apenas um arquivo podera ser anexado")
    print("-h --help           - menu de ajuda")
    print()
    print()
    print("Exemplos: ")
    print("1- Com anexo:")
    print("email4bgan.py -s gmail -u capfulano -a arquivo.pdf")
    print("email4bgan.py --servidor yahoo -username tenselva --anexo arquivo.docx")
    print("2 - Sem anexo:")
    print("email4bgan.py -s yahoobr -u sgtselvatico")
    print("email4bgan.py --servidor hotmail --usename instrutorcigs")
    print()
    sys.exit(0)


def main():
    global tentativas
    global enviado
    global servidor
    global s_port
    global email_end
    global s_email
    global filename
    global anexo

    if 4 > len(sys.argv[1:]) > 6:
        usage()

    try:

        opts, args = getopt.getopt(sys.argv[1:], "lhs:u:a:e:",
                                   ["leitura=", "help", "servidor=", "username=", "anexo=", "email="])

    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-s", "--servidor"):
            if a == "gmail":
                servidor = 'smtp.gmail.com'
                s_port = 587
                email_end = "@gmail.com"
            if a == "hotmail":
                servidor = 'smtp.live.com'
                s_port = 465
                email_end = "@hotmail.com"
            if a == "yahoo":
                servidor = 'smtp.mail.yahoo.com'
                s_port = 587
                email_end = "@yahoo.com"
        elif o in ("-u", "--username"):
            s_email = str(a) + email_end
        elif o in ("-a", "--anexo"):
            anexo = True
            filename = str(a)
        else:
            assert False, "Opcao invalida"

    print()
    print("________________________________________________________________________________________________")
    print("|  ######  ##     ## ######## ########     ##           ########   ######      ###    ##    ## |")
    print("| ##    ## ###   ###    ##    ##     ##    ##    ##     ##     ## ##    ##    ## ##   ###   ## |")
    print("| ##       #### ####    ##    ##     ##    ##    ##     ##     ## ##         ##   ##  ####  ## |")
    print("|  ######  ## ### ##    ##    ########     ##    ##     ########  ##   #### ##     ## ## ## ## |")
    print("|       ## ##     ##    ##    ##           #########    ##     ## ##    ##  ######### ##  #### |")
    print("| ##    ## ##     ##    ##    ##                 ##     ##     ## ##    ##  ##     ## ##   ### |")
    print("|  ######  ##     ##    ##    ##                 ##     ########   ######   ##     ## ##    ## |")
    print("|______________________________________________________________________________________________|")
    print("                                                  ______________________________________________")
    print("                                                 | Developed by: Cap. Miguel Sant'Anna Machado |")
    print("                                                 |              Cap. Guilherme Andre Cassanego |")
    print("                                                 |                           Maio/2020 - V 2.0 |")
    print("                                                 |_____________________________________________|")
    print()
    print()

    fromaddr = str(s_email)
    password = getpass.getpass(prompt='Digite sua senha para prosseguir:', stream=None)
    password = str(password)
    toaddr = input(str('Digite o destinatario: '))

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = input(str('Digite o assunto: '))
    body = input(str('Digite o corpo do mensagem e pressione ENTER para confirmar:\n'))
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()
    tentativa = 1
    enviado = False

    def envia_email(fromaddr, password, msg, toaddr, filename, anexo):

        global enviado
        global tentativa

        try:
            if anexo:
                attachment = open(str(filename), "rb")
                p = MIMEBase('application', 'octet-stream')
                p.set_payload((attachment).read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                msg.attach(p)

            s = smtplib.SMTP(servidor, s_port)
            s.starttls()
            s.login(fromaddr, password)
            text = msg.as_string()
            s.sendmail(fromaddr, toaddr, text)

            enviado = True
            print()
            print()
            print("                       ___......----:'"":--....(\\")
            print("                .-':'"":   :  :  :   :     :.(1\.`-.  ")
            print("              .'`.  `.  :  :      :   : :   : : :  .';")
            print("             :-`. :   .    :  `.        :.   : :`.`. a;")
            print("             : ;-. `-.-._.  :      :  ::. .' `. `., =  ;")
            print("             :-:.` .-. _-.,     :     :,.'.-' ;-. ,'''\"")
            print("           .'.' ;`. .-' `-.:  :  : : :;.-'.-.'   `-'")
            print("    :.   .'.'.-' .'`-.' -._;..:---'''\"~;._.-;")
            print("    :`--'.'  : :'     ;`-.;            :.`.-'`. ")
            print("     `'\"`    : :      ;`.;             :=; `.-'`.")
            print("             : '.    :  ;              :-:   `._-`.")
            print("              `'\"'    `. `.            `--'     `._;")
            print("                        `'\"'")
            print("")
            print("")
            print("	  ____    _____   _      __     __     _      _   _   _ ")
            print("	 / ___|  | ____| | |     \ \   / /    / \    | | | | | |")
            print("	 \___ \  |  _|   | |      \ \ / /    / _ \   |_| |_| |_|")
            print(" 	  ___) | | |___  | |___    \ V /    / ___ \  |_| |_| |_|")
            print("	 |____/  |_____| |_____|    \_/    /_/   \_\ (_) (_) (_)")
            print()
            print('E-MAIL ENVIADO COM SUCESSO!!!')
            s.quit()

        except:
            tentativa += 1
            time.sleep(1)

    while not enviado:
        print(f"[*] - {tentativa}a tentativa... (pressione Ctrl + C para cancelar)")
        envia_email(fromaddr, password, msg, toaddr, filename, anexo)

main()
