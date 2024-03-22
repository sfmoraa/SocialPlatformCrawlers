import json
import time

from utils import _debug_show_resp
import requests
from lxml import etree
from datetime import datetime
from bs4 import BeautifulSoup
from Zhihu.data_processing import *
from pprint import pprint


def get_zhihu_user_info(name):
    url = "https://www.zhihu.com/people/" + name
    try:
        html = requests.get(url).text
    except:
        print("Too Many Requests! Wait a second...")
        time.sleep(1)
        return get_zhihu_user_info(name)
    tree = etree.HTML(html)
    try:
        location = tree.xpath('//*[@id="ProfileHeader"]/div/div[1]/div/div/span/text()')[0][5:]
    except:
        location = "未知"
    return location


def extract_data_from_zhihu_response(json_data):
    mydata = []
    for data in json_data['data']:
        try:
            urltoken = data["target"]["author"]["url_token"]
        except:
            urltoken = data["target"]["author"]["urlToken"]
        try:
            commentcount = data["target"]["comment_count"]
        except:
            commentcount = data["target"]["commentCount"]
        try:
            voteupcount = data["target"]["voteup_count"]
        except:
            voteupcount = data["target"]["voteupCount"]
        try:
            updatedtime = data["target"]["updated_time"]
        except:
            updatedtime = data["target"]["updatedTime"]

        IP = get_zhihu_user_info(urltoken)
        # mydata.append([BeautifulSoup(data["target"]["content"], 'html.parser').get_text(), data["target"]["author"]["gender"], commentcount, voteupcount, datetime.fromtimestamp(updatedtime).strftime('%Y-%m-%d %H:%M'), IP])
        mydata.append([BeautifulSoup(data["target"]["content"], 'html.parser').get_text(), data["target"]["author"]["gender"], commentcount, voteupcount, updatedtime, IP])
    return mydata


def ZhihuQuestionCrawl(question_number_list, result_save_path='./Results',log_function=print):
    for question_number in question_number_list:
        zhihu_session = requests.Session()

        questions_url = "https://www.zhihu.com/question/" + str(
            question_number) + "/answers/updated"
        zhihu_first_rsp = zhihu_session.get(questions_url)
        html = zhihu_first_rsp.text
        tree = etree.HTML(html)
        initial_states = json.loads(tree.xpath('//*[@id="js-initialData"]/text()')[0])
        if initial_states['spanName']=='NotFoundErrorPage':
            log_function(f"{question_number}号问题不存在，已跳过")
            continue
        topic_cursor = initial_states['initialState']['question']['updatedAnswers'][str(question_number)]['ids'][0]['cursor']
        next_url = initial_states['initialState']['question']['updatedAnswers'][str(question_number)]['next']
        topic_name = initial_states['initialState']['entities']['questions'][str(question_number)]['title']

        total_data = []
        page_count = 1
        log_function(f'收集{question_number}号问题 “{topic_name}“回答中...')
        end_flag = False
        first_batch = initial_states['initialState']['entities']['answers']
        json_data = {'data': [{"target": first_batch[ans_id]} for ans_id in first_batch]}
        while not end_flag:
            total_data += extract_data_from_zhihu_response(json_data)
            json_data = zhihu_session.get(next_url).json()
            end_flag = json_data['paging']['is_end']
            next_url = json_data['paging']['next']
            if page_count % 10 == 0:
                log_function(f'进行中...{page_count}轮中读取了{len(total_data)}个回答')
            page_count += 1

        log_function(f"总计收集到{len(total_data)}个回答\n")
        question_path = result_save_path + "/ZHIHU_" + topic_name + ".csv"
        zhihu_store_data(total_data, question_path, topic_name)


if __name__=='__main__':
    ZhihuQuestionCrawl(['636636956', '646987953'], result_save_path='../Results')
