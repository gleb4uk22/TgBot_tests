import pandas as pd
from clickhouse_driver import Client
import environ
import os

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

def load_xlsx_kollok7():
    client2 = Client(host=os.environ.get('CL_DB_HOST')
                             , database=os.environ.get('CL_SCHEMA')
                             , user=os.environ.get('CL_USER')
                             , password=os.environ.get('CL_PASSWORD'))
    xls = pd.ExcelFile('utils/data/Anatomy_kollok7.xlsx')
    df = pd.read_excel(xls)

    for i in df.index:
        #print(df.loc[i])
        print('num_q = ' + str(df.loc[i]['num_q']))
        num_q = df.loc[i]['num_q']
        num_a = int(df.loc[i]['num_a'])
        #print('correct = ' + str(df.loc[i]['correct']))
        #print('name = ' + str(df.loc[i]['name']))
        #print('what = ' + str(df.loc[i]['what']))
        #print('num_a = ' + str(df.loc[i]['num_a']))

        client2.execute(
            'INSERT INTO TgBot_tests.Anatomy_kollok7 (num_q,correct,name,what,num_a) VALUES',
            [{
                'num_q':  num_q, #int(df.loc[i]['num_q']),
                'correct': df.loc[i]['correct'],
                'name': df.loc[i]['name'],
                'what': df.loc[i]['what'],
                'num_a': num_a
            }])