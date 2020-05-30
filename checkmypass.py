import requests
import hashlib
import sys


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError('Error fetching:{},check the api and try again'.format(res.status_code))
    return res


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def check_my_pass(password):
    hashed_pass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = hashed_pass[:5], hashed_pass[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)


def main(args):
    for password in args:
        count = check_my_pass(password)
        if count:
            print('{} was found {} times....you should change it.'.format(password, count))
        else:
            print('{} was NOT found. Carry on!'.format(password))
    


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
