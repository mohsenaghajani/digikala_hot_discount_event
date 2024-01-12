
from random import randrange
import requests
from headers import headers


def get_headers():
    return headers[randrange(0, 4)]


def get_id():
    while True:
        url = 'https://api.digikala.com/v1/hot-discount/'
        response = requests.get(url, headers=get_headers())
        if response.status_code == 200:
            data = response.json()
            url_id = data['data']['active_hot_discount']['id']
            print(url_id)
            return url_id


def get_gift(url_id, header):
    product_id = {'product_id': '12212857'}
    url = f'https://api.digikala.com/v1/hot-discount-assign/{url_id}/'
    response = requests.post(url, headers=header, json=product_id)
    get_status = response.json()
    print(get_status['data'])


def main():
    answer = 6
    url_id = get_id()
    for header in headers:
        answer = {'answer': answer}
        response = requests.post(f'https://api.digikala.com/v1/hot-discount-captcha/{url_id}/',
                                 json=answer,
                                 headers=header)
        check_answer = response.json()
        try:
            if check_answer['data']['is_correct'] is True:
                get_gift(url_id, header)
        except:
            print(check_answer)
        else:
            answer += 1


if __name__ == '__main__':
    main()
