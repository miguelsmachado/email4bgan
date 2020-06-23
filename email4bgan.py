import sys, getopt, time, smtplib, getpass, email, imaplib, os
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
receber = False


def usage():
    print()
    print("_____________________________________________________________________________________________________")
    print("| ######## ##     ##    ###    #### ##          ##           ########   ######      ###    ##    ## |")
    print("| ##       ###   ###   ## ##    ##  ##          ##    ##     ##     ## ##    ##    ## ##   ###   ## |")
    print("| ##       #### ####  ##   ##   ##  ##          ##    ##     ##     ## ##         ##   ##  ####  ## |")
    print("| ######   ## ### ## ##     ##  ##  ##          ##    ##     ########  ##   #### ##     ## ## ## ## |")
    print("| ##       ##     ## #########  ##  ##          #########    ##     ## ##    ##  ######### ##  #### |")
    print("| ##       ##     ## ##     ##  ##  ##                ##     ##     ## ##    ##  ##     ## ##   ### |")
    print("| ######## ##     ## ##     ## #### ########          ##     ########   ######   ##     ## ##    ## |")
    print("|___________________________________________________________________________________________________|")
    print("                                                       ______________________________________________")
    print("                                                      | Developed by: Cap. Miguel Sant'Anna Machado |")
    print("                                                      |              Cap. Guilherme Andre Cassanego |")
    print("                                                      |                         Maio/2020 - V 2.1.1 |")
    print("                                                      |_____________________________________________|")
    print()
    print()
    print("modo de uso: python3 email4bgan.py [opcao] -s servidor_de_email -u nome_do_usuario -a arquivo.ext")
    print()
    print("-s --servidor       - servidor da conta de email (gmail, hotmail, yahoo)")
    print("                      opcao obrigatoria para envio ou recebimento de emails")
    print("-u --username       - usuario da conta email. Ex: fulano@email.com -> fulano")
    print("                      opcao obrigatoria para envio ou recebimento de emails")
    print("-a --anexo          - nome do arquivo em anexo")
    print("                      deve conter a extensão do arquivo. Ex: anexo.zip")
    print("                      o arquivo deve estar na mesma pasta do executável")
    print("                      apenas um arquivo podera ser anexado")
    print("-r --receber        - ativa o modo de recebimento de emails")
    print("                      por defaut, o programa inicia no modo envio")
    print("-h --help           - menu de ajuda")
    print()
    print()
    print("Exemplos: ")
    print("1- Enviando com anexo:")
    print("python3 email4bgan.py -s gmail -u capfulano -a arquivo.pdf")
    print("python3 email4bgan.py --servidor yahoo -username tenselva --anexo arquivo.docx")
    print("2 - Enviando sem anexo:")
    print("python3 email4bgan.py -s yahoobr -u sgtselvatico")
    print("python3 email4bgan.py --servidor hotmail --usename instrutorcigs")
    print("3 - Recebimento de emails")
    print("python3 email4bgan.py -r -s gmail -u recrutazero")
    print("python3 email4bgan.py -r --servidor hotmail --usename gs5431")

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
    global receber

    if len(sys.argv[1:]) < 1:
        usage()

    try:

        opts, args = getopt.getopt(sys.argv[1:], "rhs:u:a:",
                                   ["receber", "help", "servidor=", "username=", "anexo="])

    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-r", "--receber"):
            receber = True
        elif o in ("-s", "--servidor"):
            if receber:
                if a == "gmail":
                    servidor = 'imap.gmail.com'
                    email_end = "@gmail.com"
                if a == "hotmail":
                    servidor = 'smtp.live.com'
                    email_end = "@hotmail.com"
                if a == "yahoo":
                    servidor = 'smtp.mail.yahoo.com'
                    email_end = "@yahoo.com"
            else:
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
    print("_____________________________________________________________________________________________________")
    print("| ######## ##     ##    ###    #### ##          ##           ########   ######      ###    ##    ## |")
    print("| ##       ###   ###   ## ##    ##  ##          ##    ##     ##     ## ##    ##    ## ##   ###   ## |")
    print("| ##       #### ####  ##   ##   ##  ##          ##    ##     ##     ## ##         ##   ##  ####  ## |")
    print("| ######   ## ### ## ##     ##  ##  ##          ##    ##     ########  ##   #### ##     ## ## ## ## |")
    print("| ##       ##     ## #########  ##  ##          #########    ##     ## ##    ##  ######### ##  #### |")
    print("| ##       ##     ## ##     ##  ##  ##                ##     ##     ## ##    ##  ##     ## ##   ### |")
    print("| ######## ##     ## ##     ## #### ########          ##     ########   ######   ##     ## ##    ## |")
    print("|___________________________________________________________________________________________________|")
    print("                                                       ______________________________________________")
    print("                                                      | Developed by: Cap. Miguel Sant'Anna Machado |")
    print("                                                      |              Cap. Guilherme Andre Cassanego |")
    print("                                                      |                         Maio/2020 - V 2.1.1 |")
    print("                                                      |_____________________________________________|")
    print()
    print()

    if not receber:
        print("MODO ENVIO")
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
                print('E-MAIL ENVIADO COM SUCESSO!!')
                s.quit()

            except:
                tentativa += 1
                time.sleep(1)

        while not enviado:
            print(f"[*] - {tentativa}a tentativa... (pressione Ctrl + C para cancelar)")
            envia_email(fromaddr, password, msg, toaddr, filename, anexo)

    else:
        print("MODO RECEBIMENTO")
        print()
        EMAIL = s_email
        PASSWORD = getpass.getpass(prompt='Digite sua senha para prosseguir:', stream=None)
        PASSWORD = str(PASSWORD)
        SERVER = servidor
        all_emails = []
        continuar = True

        print()
        print("LISTA DE E-MAILs")
        print("Email id -> Remetente -> Assunto")
        mail = imaplib.IMAP4_SSL(SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select('inbox')

        status, data = mail.search(None, 'ALL')
        mail_ids = []
        for block in data:
            mail_ids += block.split()

        for i in mail_ids:
            status, data = mail.fetch(i, '(RFC822)')

            for response_part in data:
                if isinstance(response_part, tuple):
                    message = email.message_from_bytes(response_part[1])

                    mail_from = message['from']
                    mail_subject = message['subject']

                    if not 'mixed' in message.get_content_type():
                        mail_content = ''

                        for part in message.get_payload():
                            if part.get_content_type() == 'text/plain':
                                mail_content += part.get_payload()
                    else:
                        mail_content = message.get_payload()[0]
                        mail_content = (str(mail_content).split('\n\n')[2])

                    email_id_show = str(i).split("'")[1]
                    print(f'E-mail id: {email_id_show}')
                    print(f'Remetente: {mail_from}')
                    print(f'Assunto: {mail_subject}')
                    print()
                    email_unico = [email_id_show, mail_from, mail_subject, mail_content]
                    all_emails.append(email_unico)

        while continuar:
            while True:
                selecao = (input("Selecione o e-mail id do e-mail que deseja ler: "))
                if selecao.isnumeric():
                    selecao = int(selecao)
                    num = str(selecao).encode()
                    if selecao > len(all_emails):
                        print("----------OPCAO INVALIDA----------")
                        print()
                    else:
                        selecao -= 1
                        break
                else:
                    print("----------OPCAO INVALIDA----------")
                    print()
                    continue

            print()
            print(f'Remetente: {all_emails[selecao][1]}')
            print(f'Assunto: {all_emails[selecao][2]}')
            print(f'Conteudo: {all_emails[selecao][3]}')

            typ, data = mail.fetch(num, '(RFC822)')
            raw_email = data[0][1]

            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)

            for part in email_message.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                fileName = part.get_filename()
                if bool(fileName):
                    filePath = os.path.join('', fileName)
                    if not os.path.isfile(filePath):
                        fp = open(filePath, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()
                    print()
                    print('Download do anexo: "{file}".'.format(file=fileName))
                    print()

            while True:
                opcao = input("Deseja ler mais algum e-mail? (s/n): ")
                if opcao.lower().strip() == 'n':
                    continuar = False
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

                    break
                elif opcao.lower().strip() == 's':
                    continuar = True
                    break
                else:
                    print("----------OPCAO INVALIDA----------")
                    print()

main()
