import PyPDF2
import re
from clickhouse_driver import Client
import environ
import os

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()


def convert():
    # creating a pdf reader object\n",
    #reader = PyPDF2.PdfReader('C:/gkonev/Telegram/tst_text.pdf')
    #reader = PyPDF2.PdfReader('C:/gkonev/Telegram/tst2.pdf')
    reader = PyPDF2.PdfReader('utils/data/MedGosa22_2.pdf')
    # print the number of pages in pdf file
    print("Длина импортируемого файла " + str(len(reader.pages)) + " страниц")
    # print the text of the first page
    #print(reader.pages[0].extract_text().encode('UTF-8'))
    #print('d')

    text = reader.pages[4].extract_text()
    #print(text)

    # разобьем файл по вопросам
    splitted_line = text.split('Вопрос ')
    #print(splitted_line)

    #print("СТАРТ")

    # подключение к БД
    client = Client(host=os.environ.get('CL_DB_HOST')
                     , database=os.environ.get('CL_SCHEMA')
                     , user=os.environ.get('CL_USER')
                     , password=os.environ.get('CL_PASSWORD')
                    )

    for rows in splitted_line:
        #if rows == splitted_line[3]:
        # весь кусочек линии
        #   print(rows)
        # проверяем на остуствие мусора, номер вопроса должен содержать цифру
        if rows[0:1].isdigit() or rows[0:2].isdigit():
            # номер вопроса
            #  print('номер вопроса')
            # print(rows[0:1])
            #print(' ')
            if rows[0:2].isdigit():
                qnum = rows[0:2]
            else:
                qnum = rows[0:1]
            # вопрос
            #print('вопрос')
            #print(rows[2:(rows.find("*")-1)].strip())
            #print(' ')
            q = rows[2:(rows.find("*") - 1)].strip()
            # варианты ответа
            #print('варианты ответа')
            #print(rows[(rows.find("*")-1) + 1:])
            # разобьем ответы в массив
            a = rows[(rows.find("*") - 1) + 1:].split('\n')
            # print(a)

            # убираю переносы строк в вопросах
            q = re.sub("^\s+|\n|\r|\s+$", '', q)

            # проверка данных
            print(qnum, q, a)

            p1 = a[0]
            p2 = a[1]
            p3 = a[2]
            p4 = a[3]

            print(len(q))
            print(qnum)
            print(q)
            print("question work " + str(qnum))
            client.execute(
                'INSERT INTO TgBot_tests.test_obstetrics_and_gynecology_2022 (questionNum,question,a,b,c,d) VALUES',
                [{
                    'questionNum': int(qnum),
                    'question': q,
                    'a': p1,
                    'b': p2,
                    'c': p3,
                    'd': p4
                }])
            print("question done " + str(qnum))