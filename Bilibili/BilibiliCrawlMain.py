import requests
from utils import _debug_show_resp, calculate_md5
from urllib.parse import quote
from lxml import etree
from pprint import pprint
import json
from datetime import datetime
import re
from Bilibili.data_processing import *

bilibili_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
}


def KeywordSearch(search_keyword=None):
    rst_urls = set()
    bilibili_session = requests.Session()
    first_page = bilibili_session.get(f"https://search.bilibili.com/all?keyword={quote(search_keyword)}&from_source=webtop_search&spm_id_from=333.1007&search_source=3", headers=bilibili_headers)
    html = first_page.text
    tree = etree.HTML(html)
    videos = tree.xpath('//*[@id="i_cecream"]/div/div[2]/div[2]/div/div/div/div[2]/div/div')
    for video in videos:
        rst_urls.add("https:" + video.xpath('./div/div[2]/a/attribute::href')[0])

    All_loaded = False
    page = 2
    while not All_loaded:
        layout = bilibili_session.get(f"https://search.bilibili.com/all?keyword={quote(search_keyword)}&from_source=webtop_search&spm_id_from=333.1007&search_source=3&page={page}&o={42 * (page - 1)}", headers=bilibili_headers)
        page += 1
        videos = etree.HTML(layout.text).xpath('//*[@id="i_cecream"]/div/div[2]/div[2]/div/div/div[1]/div')
        if len(videos) == 0:
            All_loaded = True

        for video in videos:
            rst_urls.add("https:" + video.xpath('./div/div[2]/a/attribute::href')[0])
        print('\rGot urls:', len(rst_urls), end='')
    return set(rst_urls)


def SingleVideoCrawl(bilibili_session, url):
    video_page = bilibili_session.get(url, headers=bilibili_headers)
    try:
        initial_states = re.search(r"window\.__INITIAL_STATE__=(.*?)\};", etree.HTML(video_page.text).xpath('/html/head/script/text()')[4]).group((1)) + '}'
    except:
        print(etree.HTML(video_page.text).xpath('/html/head/script/text()'))
        exit(9)
    initial_states = json.loads(initial_states)
    title = initial_states['videoData']['title']
    aid = initial_states['aid']
    bvid = initial_states['bvid']
    createtime = initial_states['videoData']['ctime']
    desc = initial_states['videoData']['desc']
    ownertoken = initial_states['videoData']['owner']['mid']
    like = initial_states['videoData']['stat']['like']
    coin = initial_states['videoData']['stat']['coin']
    reply = initial_states['videoData']['stat']['reply']
    share = initial_states['videoData']['stat']['share']
    favorite = initial_states['videoData']['stat']['favorite']
    view = initial_states['videoData']['stat']['view']
    danmaku = initial_states['videoData']['stat']['danmaku']
    video_rst = {'title': title, 'aid': aid, 'link': 'https://www.bilibili.com/video/' + bvid, 'createtime': createtime, 'desc': desc, 'ownertoken': ownertoken, 'like': like, 'coin': coin, 'reply': reply, 'share': share, 'favorite': favorite, 'view': view, 'danmaku': danmaku}
    return video_rst


def CommentCrawl(session, oid, save_path):
    initial_data = '{"offset":""}'
    initial_comment_url = gen_comment_url(oid, initial_data)
    json_rsp = session.get(initial_comment_url, headers=bilibili_headers).json()
    replies = comment_batch_process(session, oid, json_rsp)
    dict_list_save(save_path, replies)
    if len(replies) == 0:
        return
    while not json_rsp['data']['cursor']['is_end']:
        next_cursor = json_rsp['data']['cursor']['next']
        data = '{"offset":"{\\"type\\":3,\\"direction\\":1,\\"Data\\":{\\"cursor\\":' + str(next_cursor) + '}}"}'
        url = gen_comment_url(oid, data)
        json_rsp = session.get(url, headers=bilibili_headers).json()
        replies = comment_batch_process(session, oid, json_rsp)
        dict_list_save(save_path, replies)
        if 'data' not in json_rsp:
            print(222)
            pprint(json_rsp)
            exit(9)


def comment_batch_process(session, oid, json_rsp):
    reply_list = []
    try:
        if json_rsp['code'] != 0:
            return []
        if json_rsp['data']['replies'] is None:
            return []
    except:
        print(111)
        print(json_rsp,type(json_rsp))
        exit(8)
    for reply in json_rsp['data']['replies']:
        sub_reply, comment_data = extract_data_from_single_reply(reply)
        reply_list.append(comment_data)
        if sub_reply is not None:
            sub_replies = get_sub_comments(session, oid, sub_reply)
            reply_list += sub_replies
    return reply_list


def get_sub_comments(session, oid, root):
    url = 'https://api.bilibili.com/x/v2/reply/reply?oid=' + str(oid) + '&type=1&root=' + str(root) + '&ps=10&pn=1&web_location=333.788'
    sub_comments = session.get(url, headers=bilibili_headers).json()
    replies = comment_batch_process(session, oid, sub_comments)
    return replies


def BilibiliVideoCrawl(keyword, save_dir, crawl_comments=False, log_function=print):
    save_dir += '/' + keyword
    os.makedirs(save_dir, exist_ok=True)
    video_data_path = save_dir + '/' + keyword + '.csv'
    comment_dir = save_dir + '/VideoComments'
    os.makedirs(comment_dir, exist_ok=True)

    log_function(f"收集“{keyword}”相关视频链接中...")
    related_urls = KeywordSearch(keyword)
    for idx, url in enumerate(related_urls):
        session = requests.Session()
        video_rst = SingleVideoCrawl(session, url)
        dict_list_save(video_data_path, [video_rst])
        if crawl_comments:
            comment_data_path = comment_dir + '/' + str(video_rst['aid']) + '.csv'
            CommentCrawl(session, video_rst['aid'], comment_data_path)
        if idx % (len(related_urls) // 10) == 0:
            log_function(f"收集进度{idx}/{len(related_urls)}")


if __name__ == "__main__":
    # BilibiliKeywordSearch("撤军")
    # SingleVideoCrawl('https://www.bilibili.com/video/BV1fw4m1Z7q9')
    # CommentCrawl(requests.Session(), 1201392710, './result.csv')

    BilibiliVideoCrawl('撤军', './', True)
