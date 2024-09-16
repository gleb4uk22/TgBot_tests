import PyPDF2
import re
import clickhouse_connect
from clickhouse_driver import Client
import environ
import os

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()


def convert():
    # creating a pdf reader object\n",
    #reader = PyPDF2.PdfReader('C:/gkonev/Telegram/tst_text.pdf')
    #reader = PyPDF2.PdfReader('C:/gkonev/Telegram/tst3.pdf')
    reader = PyPDF2.PdfReader('utils/data/MedGosa22_3.pdf')
    # print the number of pages in pdf file
    print("Длина импортируемого файла "+str(len(reader.pages))+" страниц")
    # print the text of the first page
    #print(reader.pages[0].extract_text().encode('UTF-8'))
    #print('d')

    text = reader.pages[5].extract_text()
    #print(text[(text.find(istitle())-1) + 1:45])

    #print(re.findall('[A-Z][^A-Z]*', text))

    # убираем мешающий заголовое
    text = text.replace('БИОЭТИКА','')

    pos = [i for i,e in enumerate(text+'A') if e.isupper()]
    #parts = [text[pos[j]:pos[j+1]] for j in range(len(pos)-1)]
    splitted_line = [text[pos[j]:pos[j+1]] for j in range(len(pos)-1)]

    #print('kaka')
    #print(splitted_line[0])
    #print('makakaka')


    #print(text)

    # разобьем файл по вопросам
    #splitted_line = text.split('ffkfkfk ')
    #splitted_line = re.sub( r"([A-Z])", r" \1", text).split()
    #print(splitted_line)
    #re.sub( r"([A-Z])", r" \1", s).split()

    #print("СТАРТ")

    # подключение к БД
    #client = clickhouse_connect.get_client(host='localhost', username='root', password='password')
    client = clickhouse_connect.get_client(host=os.environ.get('CL_DB_HOST')
                             , database=os.environ.get('CL_SCHEMA')
                             , user=os.environ.get('CL_USER')
                             , password=os.environ.get('CL_PASSWORD'))
    client2 = Client(host=os.environ.get('CL_DB_HOST')
                             , database=os.environ.get('CL_SCHEMA')
                             , user=os.environ.get('CL_USER')
                             , password=os.environ.get('CL_PASSWORD'))

    cnt = 0
    for rows in splitted_line:
            cnt = cnt + 1
       #if rows == splitted_line[3]:
            # весь кусочек линии
            #   print(rows)
            # проверяем на остуствие мусора, номер вопроса должен содержать цифру
            #if rows[0:1].isdigit() or rows[0:2].isdigit():
             # номер вопроса
             #  print('номер вопроса')
             # print(rows[0:1])
             #print(' ')
             #if rows[0:2].isdigit():
            qnum = 3050+cnt
             #else:
             #    qnum = rows[0:1]
             # вопрос
             #print('вопрос')
             #print(rows[2:(rows.find("*")-1)].strip())
             #print(' ')
            #q = rows[2:(rows.find("*")-1)].strip()
            q = rows[:(rows.find(":"))].strip()
             # варианты ответа
             #print('варианты ответа')
             #print(rows[(rows.find("*")-1) + 1:])
             # разобьем ответы в массив
            a = rows[(rows.find(":")) + 1:].strip().split('\n')
            # print(a)

             # убираю переносы строк в вопросах
            q = re.sub("^\s+|\n|\r|\s+$", '', q)

            print(qnum,q)
            print(a)
          #  p1 = a[0]
          #  p2 = a[1]
          #  p3 = a[2]
          #  p4 = a[3]
            if a[0].find('*') == 0:
                p1 = a[0]
                p2 = a[1]
                p3 = a[2]
                p4 = a[3]
            elif a[1].find('*') == 0:
                p1 = a[1]
                p2 = a[0]
                p3 = a[2]
                p4 = a[3]
            elif a[2].find('*') == 0:
                p1 = a[2]
                p2 = a[0]
                p3 = a[1]
                p4 = a[3]
            elif a[3].find('*') == 0:
                p1 = a[3]
                p2 = a[0]
                p3 = a[1]
                p4 = a[2]

            # проверка данных
            print(qnum,q,p1,p2,p3,p4)

            #print(p1,p2,p3,p4)
            #print(len(q))
            #print(qnum)
            #print(q)
             #q = '48j'
             #insRow = [qnum, q, a[0],a[1],a[2],a[3]]

             #data = [insRow,insRow]
             #client.insert('test_obstetrics_and_gynecology_2022'
             #              , data
             #              , column_names=['questionNum', 'question'
             #                              , 'a','b','c','d'])
             #client.command('INSERT INTO test_obstetrics_and_gynecology_2022 (questionNum,question,a,b,c,d) Select p1 %d, p2 %d, p3 %d, p4 %d, p5 %d, p6 %d' % (qnum, q, a[0],a[1],a[2],a[3]))
             #client.command(f"INSERT INTO test_obstetrics_and_gynecology_2022 (questionNum,question,a,b,c,d) Select p1 %d, p2 %d, {p1}, {p2}, {p3}, {p4}")
             #client.command(f"INSERT INTO test_obstetrics_and_gynecology_2022 (questionNum,question,a,b,c,d) Select {qnum}, {q}, {p1}, {p2}, {p3}, {p4}")
             #client.command(f'INSERT INTO test_obstetrics_and_gynecology_2022 (questionNum,question,a,b,c,d) Select {qnum}, 2, 1, {p1},1, 1')
            client2.execute(
                'INSERT INTO test_obstetrics_and_gynecology_2022 (questionNum,question,a,b,c,d) VALUES',
                [{
                    'questionNum'   : int(qnum),
                    'question'      : q,
                    'a' : p1,
                    'b' : p2,
                    'c' : p3,
                    'd' : p4
                }])


    # 'foo %d, bar %d' % (foo, bar)

    # найти символ в строке
    #print(text.find('*'))

    #print(text.partition('*')[0])
    #print(text.find('Вопрос'))

    #print(text[(text.find("Вопрос ")-1) + 1:45])

    #print('СТАРТ')

    #if 'Вопрос' in text:
    #    splitted_line = text.split()
    #    print(splitted_line)

    #print(text.partition("\nВопрос "))

    #>>> s = 'text text: one two three'
    #>>> s[s.find(":") + 1:]
    # ' one two three'

    #with pdfplumber.open("C:/gkonev/Telegram/tst_text.pdf") as pdf:
     #   first_page = pdf.pages[0]
      #  print(first_page.extract_text())

    #print('g')


    #from pdfminer import high_level

    #with open('C:/gkonev/Telegram/tst_text.pdf', 'rb') as f:
     #   text = high_level.extract_text(f)
    #    print(text)
