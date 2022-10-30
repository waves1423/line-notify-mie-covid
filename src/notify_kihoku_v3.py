import requests
from bs4 import BeautifulSoup as bs4
import lxml
import csv
import os
import pandas as pd

text = 'https://www.pref.mie.lg.jp/YAKUMUS/HP/m0068000066_{}.htm'
mat = []

def send_line_notify(notification_message):
    with open('line_token.txt', 'r') as f:
        tokens = [s.strip() for s in f.readlines()]
        print(tokens) 
    for token in tokens:
        line_notify_token = token
        line_notify_api = 'https://notify-api.line.me/api/notify'
        headers = {'Authorization': f'Bearer {line_notify_token}'}
        data = {'message': f'{notification_message}'}
        requests.post(line_notify_api, headers = headers, data = data)
        print(token)

def job():
    with open('url_number.txt', 'r', encoding='utf-8') as f:
        data = f.read()
        data = data.rstrip().zfill(5)
    url = text.format(data)
    print(url)

    try:
        res = requests.get(url)
        soup = bs4(res.content, 'lxml')
        for td in soup.find_all('td', attrs={'colspan': '1'}):
            td.decompose()
        tables = soup.find('table', class_='undefined').find_all('tr')

        for table in tables:
            case = [case.text for case in table.find_all('td')]
            mat.append(case)  
    except Exception:
        pass

    with open('new_cases.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n')
        for case in mat:
            writer.writerow(case)

    df_last_cases = pd.read_csv('cases.csv', names=('例目', '居住地', '性別', '年代', '職業', '発症日', '陽性判明日', '属性', '症状等'), dtype=str)
    df_new_cases = pd.read_csv('new_cases.csv', names=('例目', '居住地', '性別', '年代', '職業', '発症日', '陽性判明日', '属性', '症状等'), dtype=str)
    df_dup = df_new_cases[~df_new_cases['例目'].isin(df_last_cases['例目'])]
    df_dup_bool = (df_dup['居住地'] == '紀北町')
    df_dup_sum = df_dup_bool.values.sum()

    #紀北町が入っていた場合のみ通知するとき
    #if df_dup_sum != 0:
    if df_dup.empty == False:
        send_text = '紀北町の新規陽性者は{}名です。{}'
        send_line_notify(send_text.format(df_dup_sum, url))
        os.remove('cases.csv')
        os.rename('new_cases.csv', 'cases.csv')
    else:
        urlCheck()

def urlCheck():
    with open('url_number.txt', 'r', encoding='utf-8') as f:
        data = f.read()
    i = 1
    try:
        while True:
            next_data = int(data) + i
            next_data_str = str(next_data).zfill(5)
            next_url = text.format(next_data_str)
            print(next_url)
            next_res = requests.get(next_url)
            next_soup = bs4(next_res.content, 'lxml')
            i += 1
            if next_soup.find('th', text=['公表日']) != None:
                with open('url_number.txt', 'w') as f:
                    f.write(next_data_str)
                    job()
                    break
            elif i >= 6:
                break
    except Exception:
        pass

def main():
    job()

if __name__=="__main__":
    main()
