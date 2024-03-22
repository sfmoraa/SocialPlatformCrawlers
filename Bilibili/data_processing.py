import hashlib
from urllib.parse import quote
from datetime import datetime
import csv
import os
from pprint import pprint


def calculate_md5(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode('utf-8'))
    return md5_hash.hexdigest()


def gen_comment_url(oid, data):
    timestamp_str = str(int(datetime.now().timestamp()))
    Jt = 'mode=2&oid=' + str(oid) + '&pagination_str=' + quote(data) + '&plat=1&type=1&web_location=1315875&wts=' + timestamp_str
    Wt = 'ea1db124af3c7062474693fa704f4ff8'
    w_rid = calculate_md5(Jt + Wt)
    url = 'https://api.bilibili.com/x/v2/reply/wbi/main?oid=' + str(oid) + '&type=1&mode=2&pagination_str=' + quote(data) + '&plat=1&web_location=1315875&w_rid=' + w_rid + '&wts=' + timestamp_str
    return url


def extract_data_from_single_reply(reply):
    rst = {'message': reply['content']['message'], 'rpid_str': reply['rpid_str'], 'parent': reply['parent_str'], 'ctime': reply['ctime'], 'like': reply['like'], 'mid': reply['member']['mid'], 'sex': reply['member']['sex']}
    if reply['replies'] is not None and len(reply['replies']) > 0:
        return reply['rpid_str'], rst
    else:
        return None, rst


def dict_list_save(save_path, dict_list):
    if not isinstance(dict_list, list):
        raise ValueError("Data Not List")
    if len(dict_list) == 0:
        return
    file_exists = os.path.isfile(save_path)
    with open(save_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=dict_list[0].keys(), extrasaction='ignore')
        if not file_exists:
            writer.writeheader()
        for item in dict_list:
            writer.writerow(item)


if __name__ == '__main__':
    # print(gen_comment_url(1001488046, '{"offset":"{\\"type\\":3,\\"direction\\":1,\\"Data\\":{\\"cursor\\":7300}}"}'))
    input_text = "Hello, 📷! 你好！"
    print(input_text.encode('gbk', errors='replace').decode('gbk'))
