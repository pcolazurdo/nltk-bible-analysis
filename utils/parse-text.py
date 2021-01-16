# This sample code uses Bible API to download a JSON representation of a full Bible book
# to get the list of available Bibles: https://bibliaapi.com/docs/Available_Bibles
# to get your own personal key: https://api.biblia.com/v1/Users/SignIn

import json
import urllib3
from configparser import ConfigParser


config = ConfigParser()
config.read('parse-text.ini')
_key = config.get('main', 'biblia_key')
print(_key)
exit()


def get_text(passage):
    # print(passage)
    r = http.request(
        'GET',
        _url_root,
        fields={
            'key': _key,
            'passage': passage}
    )
    # print(r.status)
    if (r.status != 200):
        return None
    else:
        return json.loads(r.data.decode('utf-8'))


def download_book(version_name='RVR60', book_name='Revelation'):
    break_counter = 0
    json_dict = {
        "book": book_name,
        "chapters": []
    }
    for chap in range(1, 25):
        if (break_counter > 1):
            break
        verses_arr = []
        for verse in range(1, 100):
            r = get_text('{}{}:{}'.format(book_name, chap, verse))
            # print(r)
            if (r and 'text' in r):
                break_counter = 0
                verses_arr.append({
                    "verse": verse,
                    "text": r["text"]
                })
            else:
                break_counter = break_counter + 1
                break
        if (len(verses_arr) > 0):
            json_dict["chapters"].append({
                "chapter": chap,
                "verses": verses_arr
            })

    return json_dict


_url_root = 'https://api.biblia.com/v1/bible/content/RVR60.txt.js'  # need to customize
http = urllib3.PoolManager()
r = download_book()
print(json.dumps(r))
