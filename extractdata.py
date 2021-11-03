import email
import imaplib
import os
import shutil

import config
from config import *
import imapclient




def load_file_from_email_imap4(
        mail_from,
        imap_server,
        login,
        password,
        save_data_dir,
        filetype,
):

    print("- подключаемся к ", imap_server)
    mail = imaplib.IMAP4_SSL(imap_server)
    print("-- логинимся")
    mail.login(login, password)
    mail.list()
    print("-- подключаемся к inbox")
    mail.select("inbox")
    print("-- получаем UID последнего письма")

    try:
        result, data = mail.search(None, 'FROM', mail_from)
    except Exception as ex:
        print(f'Error reads file {ex}')
    else:
        print('-----'*5, result, len(data[0]))

    for num in data[0].split():
        result, data = mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]
        try:
            email_message = email.message_from_string(raw_email)
            print(raw_email)
        except TypeError as te:
            email_message = email.message_from_bytes(raw_email)
            print(f'Ошибка соединения {te}')

        print("--- нашли письмо от: ", email.header.make_header(email.header.decode_header(email_message['From'])))
        print(type(email.header.make_header(email.header.decode_header(email_message['From']))))
        for part in email_message.walk():
            print(part.get_content_type())
            if "application" in part.get_content_type():
                filename = part.get_filename()
                filename = str(email.header.make_header(email.header.decode_header(filename)))
                if not filename:
                    filename = "test.txt"
                print("---- нашли вложение ", filename)
                # mime = magic.Magic(mime=True)
                # type_of_file = mime.from_file(filename)
                # print(f'Тип файла {type_of_file}')

                if filename.endswith(filetype):
                    try:
                        with open(os.path.join(save_data_dir, filename), 'wb') as fp:
                            fp.write(part.get_payload(decode=True))
                        print("-- удаляем письмо")
                    except Exception as ex:
                        print(f'Возникло исключение при попытке записи файла {ex}')

                    try:
                        mail.store(num, '+FLAGS', '(\Deleted)')
                        mail.expunge()
                    except Exception as ex:
                        print(f'Возникло исключение при попытке записи файла {ex}')

                    try:
                        shutil.copy2(os.path.join(save_data_dir, filename),
                                     os.path.join(config.TODAY_TMP_DIR, filename))
                    except Exception as ex:
                        print(f'Возникло исключение при попытке записи файла {ex}')

    try:
        mail.close()
        mail.logout()
    except Exception as ex:
        print(f'Возникло исключение при попытке записи файла {ex}')



if __name__ == '__main__':

    load_file_from_email_imap4(
        mail_from='"listing.distributeri@putevi-srbije"',
        imap_server=IMAP_SERVER,
        login=MAIL_LOGIN_DAILY_REPORTS,
        password=MAIL_PASSWORD1,
        save_data_dir=DAILY_PS_TRANSACTION,
        filetype='..csv',
    )
