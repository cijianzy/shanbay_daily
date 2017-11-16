# -*- coding: UTF-8 -*-
# Title: $END$
# Author: cijian
# Email: cijianzy@gmail.com


import requests
import browsercookie
import time
import sys
import json
import re
import os

reload(sys)
sys.setdefaultencoding('utf-8')

cj = browsercookie.chrome()

page_num_limit = 70

if not os.path.exists('data'):
    os.makedirs('data')

file = open('data/daily.json','w')
for page_num in range(1, page_num_limit):
    time.sleep(5)
    r = requests.get('https://www.shanbay.com/api/v1/bdc/library/today/?page=' + str(page_num) + '&_=1490277104875',cookies=cj)
    content = r.content
    content = content.strip()
    content = re.sub(r'"false"[^,]', '\\\"false\\\"', content)
    content = re.sub(r'"true"[^,]', '\\\"false\\\"', content)
    print(content)
    dict = json.loads(content, encoding='utf-8')
    a = dict['data']['objects']
    for word in a:
        word_json = {}
        word_json['word'] = word['content']

        word_json['pronunciation_us'] = word['pronunciations']['us']
        word_json['defn'] = word['cn_definition']['defn']
        word_json['us_audio'] = word['us_audio']
        file.write(str(word_json) + '\n')



