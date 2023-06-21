import imaplib
import email
import os
 
# Параметры подключения
mail_username = 'login'
mail_password = 'password'
 
imap_server = 'imap.yandex.ru'
imap_port = 993
 
# Установка соединения с сервером
mail = imaplib.IMAP4_SSL(imap_server, imap_port)
mail.login(mail_username, mail_password)
 
# Выбор папки
folder_name = 'inbox'
mail.select(folder_name)
 
# Определение адресата и формата вложения
search_query = '(FROM "##@##.ru")'
file_extension = 'xlsx'
 
# Путь для сохранения вложений
download_path = os.path.join(os.getcwd(), 'prace_auto_dow')
 
# Создание папки, если ее не существует
if not os.path.exists(download_path):
    os.makedirs(download_path)
 
# Поиск писем
_, search_data = mail.search(None, search_query)
 
# Получение списка номеров найденных писем
message_numbers = search_data[0].split()
 
# Итерация по найденным письмам
for msg_num in message_numbers:
    # Получение сообщения
    _, msg_data = mail.fetch(msg_num, '(RFC822)')
 
    # Извлечение данных из сообщения
    msg = email.message_from_bytes(msg_data[0][1])
    date_str = msg['Date']
    date_tuple = email.utils.parsedate(date_str)
    date = f'{date_tuple[0]}-{date_tuple[1]:02d}-{date_tuple[2]:02d}'
    subject = email.header.decode_header(msg['Subject'])[0][0]
    if isinstance(subject, bytes):
        subject = subject.decode('utf-8')

 
    # Обработка вложения
    for part in msg.walk():

        if "application" in part.get_content_type():
            filename = part.get_filename()
            filename_bytes = email.header.decode_header(filename)[0][0]
            if isinstance(filename_bytes, bytes):
                filename_str = filename_bytes.decode('utf-8')
            else:
                filename_str = filename_bytes

            filepath = os.path.join(download_path, f'{date}_{filename_str}')
            
            # Сохранение вложения
            if os.path.isfile(filepath):
                print(f'File {filepath} already exists')
            else:
                with open(filepath, 'wb') as f:
                    f.write(part.get_payload(decode=True))
                print(f'Successfully downloaded {filename_str}')

# Закрытие соединения
mail.close()
mail.logout()