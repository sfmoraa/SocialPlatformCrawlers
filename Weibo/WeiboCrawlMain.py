import requests
from lxml import etree
from urllib.parse import quote
from Weibo.data_processing import *
from tqdm import trange
import time
import re
import json

weibo_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
}


def create_weibo_search_url(topic, search_days_range, weibo_session):
    """ 创建指定日期范围内逐小时的特定关键词的搜索网址链接

    :param topic: 用于搜索的关键词
    :param search_days_range: 搜索的时间区间，以列表形式传入，形如["2023-12-18", "2023-12-28"]，左闭右开区间
    :param weibo_session: 建立好的微博会话
    :return:
    """
    print(f"Preparing urls within {search_days_range} in weibo to search...\n")
    start_datetime = datetime.strptime(search_days_range[0], "%Y-%m-%d")
    end_datetime = datetime.strptime(search_days_range[1], "%Y-%m-%d")
    current_datetime = start_datetime
    date_range = []
    while current_datetime <= end_datetime:
        date_range.append(current_datetime.strftime("%Y-%m-%d-%H"))
        current_datetime += timedelta(days=1)

    url_list = []
    for day_idx in trange(len(date_range) - 1):
        base_url = "https://s.weibo.com/weibo?q=" + quote(topic) + "&typeall=1&suball=1&timescope=custom%3A" + date_range[day_idx] + "%3A" + date_range[day_idx + 1] + "&Refer=g&page="
        test = weibo_session.get(base_url + '1', headers=weibo_headers)
        html = test.text
        tree = etree.HTML(html)
        pages = tree.xpath('//*[@id="pl_feedlist_index"]/div[3]/div/span/ul/li')
        if len(pages) == 0:
            # 当天无数据
            url_list.append(base_url + '1')
        elif len(pages) == 50:
            this_day = datetime.strptime(date_range[day_idx], "%Y-%m-%d-%H")
            for hour in range(24):
                this_day_base_url = "https://s.weibo.com/weibo?q=" + quote(topic) + "&typeall=1&suball=1&timescope=custom%3A" + this_day.strftime("%Y-%m-%d-%H") + "%3A"
                this_day += timedelta(hours=1)
                this_day_base_url += this_day.strftime("%Y-%m-%d-%H") + "&Refer=g&page="
                test = weibo_session.get(this_day_base_url + '1', headers=weibo_headers)
                html = test.text
                tree = etree.HTML(html)
                pages = tree.xpath('//*[@id="pl_feedlist_index"]/div[3]/div/span/ul/li')
                if len(pages) == 0:
                    url_list.append(this_day_base_url + '1')
                else:
                    for i in range(1, len(pages) + 1):
                        url_list.append(this_day_base_url + str(i))
        else:
            # 当天数据不足50页，无需按小时爬取
            for i in range(1, len(pages) + 1):
                url_list.append(base_url + str(i))
    return url_list


def extract_data_from_weibo_response(rsp, weibo_session, get_user_info=True, get_comment=True):
    """

    :param rsp: 微博高级搜索页面的响应
    :param weibo_session: 建立的微博会话，用于提取用户信息
    :param get_user_info: 是否爬取用户的ip信息
    :param get_comment: 是否爬取主贴下的评论
    :return:
    """
    results = []
    html = rsp.text
    tree = etree.HTML(html)
    comments = tree.xpath('//*[@id="pl_feedlist_index"]/div[2]/div')
    for comment in comments:
        texts = comment.xpath('./div/div[1]/div[2]/p/text()')
        comment_time = comment.xpath('./div/div[1]/div[2]/div[2]/a[1]/text()')
        likes = comment.xpath('./div/div[2]/ul/li[3]/a/button/span[2]/text()')
        selflink = comment.xpath('./div/div[1]/div[2]/div[1]/div[2]/a')[0].get('href')
        userid = re.search(r"//weibo.com/(\d+)\?refer_flag", selflink).group(1)
        if get_user_info:
            location, gender = get_weibo_user_info(userid, weibo_session)
        else:
            location = None
            gender = None
        processed_text = processed_time = ''
        for string in texts:
            string = string.strip().replace('\u200b', '')
            if not string:
                continue
            processed_text += string
        for string in comment_time:
            string = string.strip()
            if not string:
                continue
            processed_time += convert_weibo_time_format(string, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if likes[0] == '赞':
            likes = 0
        else:
            likes = int(likes[0])
        results.append([processed_text, processed_time, likes, location, gender])
    return results


def get_comment(mid, session):
    url = ""


def get_first_comments(mid, session):
    max_id = 0
    max_id_type = 0
    url = '<https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id={}&max_id_type={}>'
    while True:
        response = session.get(url.format(mid, mid, max_id, max_id_type), headers=weibo_headers)
        content = json.loads(response)
        max_id = content['data']['max_id']
        max_id_type = content['data']['max_id_type']
        text_list = content['data']['data']
        for text in text_list:
            text_data = text['text']
            # save_text_data(text_data)
            if int(max_id) == 0:  # 如果max_id==0表明评论已经抓取完毕了
                break


def get_weibo_user_info(user_id, session, mode=0):
    """

    :param user_id: 被查询用户的id号，即个人主页https://weibo.com/u/{id}中的id号
    :param session: 微博会话
    :param mode: mode为0是爬取帖子时使用，只返回位置和性别，较快；mode为1时是拉取具体信息时使用，还会拉取ip属地、账号创建时间等数据
    :return:
    """
    # try:
    #     user_info = session.get("https://weibo.com/ajax/profile/info?custom=" + str(user_id), headers=weibo_headers).json()
    #     location = user_info['data']['user']["location"].split()
    #     if len(location) > 1:
    #         location = location[0]
    #     else:
    #         location = user_info['data']['user']["location"]
    #     gender = user_info['data']['user']["gender"]
    #     if mode == 0:
    #         return [location, gender]
    #     elif mode == 1:
    #         id = user_info['data']['user']["id"]
    #         name = user_info['data']['user']["screen_name"]
    #         friends_count = user_info['data']['user']["friends_count"]
    #         followers_count = user_info['data']['user']["followers_count"]
    #         detail_info = session.get("https://weibo.com/ajax/profile/detail?uid=" + str(user_id), headers=weibo_headers).json()
    #         created_at = detail_info['data']['created_at']
    #         ip_location = detail_info['data']['ip_location']
    #         desc_text = detail_info['data']['desc_text']
    #         return [id, name, gender, location, ip_location, friends_count, followers_count, created_at, desc_text]
    # except Exception as e:
    #     print("Too many requests!sleeping",e)
    #     time.sleep(10)
    #     return get_weibo_user_info(user_id, session)
    try:
        user_info = session.get("https://weibo.com/ajax/profile/info?custom=" + str(user_id), headers=weibo_headers).json()
    except:
        print("Failed to get id:",user_id)
        return None
    gender = user_info['data']['user']["gender"]
    if mode == 0:
        location = user_info['data']['user']["location"].split()
        if len(location) > 1:
            location = location[0]
        else:
            location = user_info['data']['user']["location"]
        return [location, gender]
    elif mode == 1:
        location=user_info['data']['user']["location"]
        name = user_info['data']['user']["screen_name"]
        friends_count = user_info['data']['user']["friends_count"]
        followers_count = user_info['data']['user']["followers_count"]
        detail_info = session.get("https://weibo.com/ajax/profile/detail?uid=" + str(user_id), headers=weibo_headers).json()
        created_at = detail_info['data']['created_at']
        ip_location = detail_info['data']['ip_location']
        desc_text = detail_info['data']['desc_text']
        return [user_id, name, gender, location, ip_location, friends_count, followers_count, created_at, desc_text]

def WeiboKeywordCrawl(search_keyword=None, result_save_path='./Results', search_date_range=None, weibo_cookies=None, crawl_user_ip_and_gender=True, crawl_comment=True):
    weibo_session = requests.Session()
    weibo_session.cookies.update(weibo_cookies)

    url_list = create_weibo_search_url(search_keyword, search_date_range, weibo_session)
    print(f"Ready to crawl [{len(url_list)}] url of weibo, the first is {url_list[0]}", '\n')

    total_rst = []
    for i in trange(len(url_list)):
        target_url = url_list[i]
        try:
            request_rsp = weibo_session.get(target_url, headers=weibo_headers)
            if request_rsp.status_code == 200:
                page_rst = extract_data_from_weibo_response(request_rsp, weibo_session, get_user_info=crawl_user_ip_and_gender, get_comment=crawl_comment)
                total_rst += page_rst
            else:
                print("Failed to crawl the page:", request_rsp.status_code)
        except Exception as e:
            print("ERROR:", e, " in url:", target_url)

    file_name = result_save_path + "/WEIBO_" + search_keyword + '_' + datetime.now().strftime("%Y%m%d_%H-%M-%S") + ".csv"
    weibo_store_data(total_rst, file_name, search_keyword, 'Query time: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def WeiboGetUserInfo(id_list: list, weibo_cookies,result_save_path):
    weibo_session = requests.Session()
    weibo_session.cookies.update(weibo_cookies)
    total_result = []
    for idx in trange(len(id_list)):
        total_result.append(get_weibo_user_info(id_list[idx], weibo_session, mode=1))
    df = pd.DataFrame(total_result, columns=["user_id", "name", "gender", "location", "ip_location", "friends_count", "followers_count", "created_at","desc"])
    df.to_csv(result_save_path+"/WEIBO_USERINFO", index=False, encoding='utf-8-sig')
