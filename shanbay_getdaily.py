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
import urllib2
import shutil


reload(sys)
sys.setdefaultencoding('utf-8')

# 获取浏览器脚本
b_cookie = browsercookie.chrome()

# 获取配置中的用户名和每日单词的页面数
config = json.load(open('configuration.json'))
user_id = config['user_id']
page_num_limit = config['daily_page_num'] + 1

if not os.path.exists('data'):
    os.makedirs('data')

if os.path.exists('data/mp3'):
    shutil.rmtree('data/mp3')
os.makedirs('data/mp3')

file = open('data/daily.json','w')

for page_num in range(1, page_num_limit + 1):
    time.sleep(5)
    r = requests.get('https://www.shanbay.com/api/v1/bdc/library/today/?page=' + str(page_num) + '&_=' + user_id, cookies=b_cookie)
    content = r.content
    content = content.strip()
    content = re.sub(r'"false"[^,]', '\\\"false\\\"', content)
    content = re.sub(r'"true"[^,]', '\\\"false\\\"', content)
    dict = json.loads(content, encoding='utf-8')
    a = dict['data']['objects']
    for word in a:
        word_json = {}
        word_json['word'] = word['content']

        word_json['pronunciation_us'] = word['pronunciations']['us']
        word_json['defn'] = word['cn_definition']['defn']
        word_json['us_audio'] = word['us_audio']

        try:
            mp3file = urllib2.urlopen(word_json['us_audio'])
            mp3file_save_path = 'data/mp3/'+ word_json['us_audio'].split('/')[-1]
            with open(mp3file_save_path, 'wb') as output:
                output.write(mp3file.read())
        except:
            print('Error: ' + word_json['word'] + ' audio file download failure.' )
            pass

        word_json['mp3'] = mp3file_save_path

        file.write(str(word_json) + '\n')
    print('Download Page ' + str(page_num) + ': success' )

file.close()
print('Download success')



