import email
import imaplib
import os

EMAIL = 'miguelsm.319@gmail.com'
PASSWORD = 'Mi314159'
SERVER = 'imap.gmail.com'
all_emails = []
continuar = True

print("LISTA DE E-MAILs")
# abriremos uma conexão com SSL com o servidor de emails
# logando e navegando para a inbox
mail = imaplib.IMAP4_SSL(SERVER)
mail.login(EMAIL, PASSWORD)
# selecionamos a caixa de entrada neste caso
# mas qualquer outra caixa pode ser selecionada
mail.select('inbox')

# faremos uma busca com o critério ALL para pegar
# todos os emails da inbox, esta busca retorna
# o status da operação e uma lista com
# os ids dos emails
status, data = mail.search(None, 'ALL')
# data é uma lista com ids em blocos de bytes separados
# por espaço neste formato: [b'1 2 3', b'4 5 6']
# então para separar os ids primeiramente criaremos
# uma lista vazia
mail_ids = []
# e em seguida iteramos pelo data separando os blocos
# de bytes e concatenando a lista resultante com nossa
# lista inicial
for block in data:
    # a função split chamada sem nenhum parâmetro
    # transforma texto ou bytes em listas usando como
    # ponto de divisão o espaço em branco:
    # b'1 2 3'.split() => [b'1', b'2', b'3']
    mail_ids += block.split()

# agora para cada id baixaremos o email
# e extrairemos seu conteúdo
for i in mail_ids:
    # a função fetch baixa o email passando id e o formato
    # em que você deseja que a mensagem venha
    status, data = mail.fetch(i, '(RFC822)')

    # data no formato '(RFC822)' vem em uma lista com a
    # tupla onde o conteúdo está e o byte de fechamento b')'
    # por isso vamos iterar pelo data extraindo a tupla
    for response_part in data:
        # se for a tupla a extraímos o conteúdo
        if isinstance(response_part, tuple):
            # o primeiro elemento da tupla é o cabeçalho
            # de formatação e o segundo elemento possuí o
            # conteúdo que queremos extrair
            message = email.message_from_bytes(response_part[1])

            # com o resultado conseguimos pegar as
            # informações de quem enviou o email e o assunto
            mail_from = message['from']
            mail_subject = message['subject']

            # agora para o texto do email precisamos de um
            # pouco mais de trabalho pois ele pode vir em texto puro
            # ou em multipart, se for texto puro é só ir para o
            # else e extraí-lo do payload, caso contrário temos que
            # separar o que é anexo e extrair somente o texto
            if not 'mixed' in message.get_content_type():
                mail_content = ''

                # no caso do multipart vem junto com o email
                # anexos e outras versões do mesmo email em
                # diferentes formatos como texto imagem e html
                # para isso vamos andar pelo payload do email
                for part in message.get_payload():
                    # se o conteúdo for texto text/plain que é o
                    # texto puro nós extraímos
                    if part.get_content_type() == 'text/plain':
                        mail_content += part.get_payload()
            else:
                mail_content = message.get_payload()[0]
                mail_content = (str(mail_content).split('\n\n')[2])

            # por fim vamos mostrar na tela o resultado da extração
            email_id_show = str(i).split("'")[1]
            print(f'E-mail id: {email_id_show}')
            print(f'Remetente: {mail_from}')
            print(f'Assunto: {mail_subject}')
            print()
            email_unico = [email_id_show, mail_from, mail_subject, mail_content]
            all_emails.append(email_unico)
            # print(f'Content: {mail_content}')

while continuar:
    while True:
        selecao = (input("Selecione o e-mail id do e-mail que deseja ler: "))
        if selecao.isnumeric():
            selecao = int(selecao)
            num = str(selecao).encode()
            if selecao > len(all_emails):
                print("OPCAO INVALIDA")
                print()
            else:
                selecao -= 1
                break
        else:
            print("OPCAO INVALIDA")
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
            break
        elif opcao.lower().strip() == 's':
            continuar = True
            break
        else:
            print("OPCAO INVALIDA")
            print()


