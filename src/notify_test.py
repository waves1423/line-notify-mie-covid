import requests
#import schedule
#import time

def main():
    #send_line_notify('テストメッセージ')
    send_line_notify('(gcp)テストメッセージ')
    #schedule.every(1).minutes.do(send_line_notify)

   # while True:
        #schedule.run_pending()
        #time.sleep(10)


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

if __name__=="__main__":
    main()
