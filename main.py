from concurrent.futures import ThreadPoolExecutor
from random import randrange
import requests
from headers import headers



def get_headers():
    return headers[randrange(0, 4)]


def get_id():
    while True:
        url = 'https://api.digikala.com/v1/hot-discount/'
        response = requests.get(url, headers=get_headers())
        data = response.json()
        if data['status'] == 200:
            if 'id' in data['data']['active_hot_discount']:
                url_id = data['data']['active_hot_discount']['id']
                print(url_id)
                return url_id
            else:
                print('id has not found')
        else:
            print(data['message'])



def get_gift(url_id, header):
    product_id = {'product_id': '12212857'}
    url = f'https://api.digikala.com/v1/hot-discount-assign/{url_id}/'
    response = requests.post(url, headers=header, json=product_id)
    get_status = response.json()
    print(get_status['data'])


def thread():
    url_id = get_id()
    count = 7
    executor = ThreadPoolExecutor(max_workers=15)
    for header in headers:
        executor.submit(main, header, url_id, count)
        count += 1


def main(header, url_id, answer):
    answer1 = {'answer': answer}
    response = requests.post(f'https://api.digikala.com/v1/hot-discount-captcha/{url_id}/',
                             json=answer1,
                             headers=header)
    check_answer = response.json()
    print(answer)
    if check_answer['status'] == 200:
        if check_answer['data']['is_correct'] is True:
            get_gift(url_id, header)
    else:
        print(check_answer['message'])


if __name__ == '__main__':
    main()
