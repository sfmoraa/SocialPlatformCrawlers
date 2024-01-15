import requests
from Weibo.data_processing import convert_weibo_comment_time_format
from time import sleep

comments_headers = {
    'authority': 'weibo.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
}


def GetFullComments(mid, uid):
    """ 爬取某帖子下的所有评论

    :param mid: 帖子的mid
    :param uid: 发帖人id
    :return: 爬取结果
    """
    comments_session = requests.Session()
    full_rst, max_id = get_first_comment_page(mid, uid, comments_session)
    while max_id != 0:
        flow_page_rst, max_id = get_flow_comment_page(mid, uid, max_id, comments_session)
        full_rst.extend(flow_page_rst)
    # 主贴子id 本评论id，子回复的根id，类型，内容，发布时间，赞数，发布者id
    return full_rst


def process_single_comment(comment, post_id, uid, session):
    """ 处理单条评论，并爬取其子评论（评论回复）

    :param comment: json格式的单条评论
    :param post_id: 隶属于的主贴子id
    :param uid: 发帖人id
    :param session: 微博会话
    :return: 本条评论及子评论的内容
    """
    comment_rsts = [[post_id, comment['id'], None, comment['readtimetype'], comment['text_raw'], convert_weibo_comment_time_format(comment['created_at']), comment['like_counts'], comment['user']['id']]]
    if len(comment['comments']) > 0:
        comment_rsts.extend(get_sub_comments(comment['id'], post_id, uid, session))
    return comment_rsts


def get_first_comment_page(mid, uid, session):
    """ 处理首个评论数据包

    :param mid: 主贴子id
    :param uid: 发帖人id
    :param session: 微博会话
    :return: 评论结果和下一个包的max_id
    """
    first_comment_params = {
        'flow': '1',
        'is_reload': '1',
        'id': f'{mid}',
        'is_show_bulletin': '2',
        'is_mix': '0',
        'count': '10',
        'uid': f'{uid}',
        'fetch_level': '0',
        'locale': 'zh-CN',
    }
    while True:
        try:
            first_comments_json = session.get('https://weibo.com/ajax/statuses/buildComments', params=first_comment_params, headers=comments_headers).json()
            break
        except Exception as e:
            print(e)
            sleep(3)
    rst = []
    for comment in first_comments_json['data']:
        rst.extend(process_single_comment(comment, mid, uid, session))
    if 'max_id' in first_comments_json.keys():
        max_id = first_comments_json['max_id']
    else:
        max_id=0

    return rst, max_id


def get_flow_comment_page(mid, uid, max_id, session):
    """ 爬取后续所有评论数据包

    :param mid: 帖子的mid
    :param uid: 用户id
    :param max_id: 指定的max_id
    :param session: 微博会话
    :return: 评论结果和下一个包的max_id
    """
    flow_comment_params = {
        'flow': '1',
        'is_reload': '1',
        'id': f'{mid}',
        'is_show_bulletin': '2',
        'is_mix': '0',
        'max_id': f'{max_id}',
        'count': '20',
        'uid': f'{uid}',
        'fetch_level': '0',
        'locale': 'zh-CN',
    }
    flow_comment_json = session.get('https://weibo.com/ajax/statuses/buildComments', params=flow_comment_params, headers=comments_headers).json()
    rst = []
    for comment in flow_comment_json['data']:
        rst.extend(process_single_comment(comment, mid, uid, session))
    max_id = flow_comment_json['max_id']
    return rst, max_id


def get_sub_comments(mid, post_id, uid, session):
    """ 爬取评论的子评论（评论回复）

    :param mid: 评论的mid
    :param post_id: 评论隶属的主贴子id
    :param uid: 发帖人id
    :param session: 微博会话
    :return: 子评论
    """
    sub_comments_rst = []
    sub_comment_params = {
        'is_reload': '1',
        'id': f'{mid}',
        'is_show_bulletin': '2',
        'is_mix': '1',
        'fetch_level': '1',
        'max_id': '0',
        'count': '20',
        'uid': f'{uid}',
        'locale': 'zh-CN',
    }
    sub_comment_rsp = session.get('https://weibo.com/ajax/statuses/buildComments', params=sub_comment_params, headers=comments_headers)
    while sub_comment_rsp.status_code!=200:
        print("ERROR!retry after 5 seconds. ",sub_comment_rsp.content)
        sleep(5)
        sub_comment_rsp = session.get('https://weibo.com/ajax/statuses/buildComments', params=sub_comment_params, headers=comments_headers)

    sub_comment_json=sub_comment_rsp.json()
    for sub_comment in sub_comment_json['data']:
        sub_comments_rst.append([post_id, sub_comment['id'], sub_comment['rootid'], sub_comment['readtimetype'], sub_comment['text_raw'], convert_weibo_comment_time_format(sub_comment['created_at']), sub_comment['like_counts'], sub_comment['user']['id']])
    max_id = sub_comment_json['max_id']
    while max_id != 0:
        sub_comment_flow_params = {
            'flow': '0',
            'is_reload': '1',
            'id': f'{mid}',
            'is_show_bulletin': '2',
            'is_mix': '1',
            'fetch_level': '1',
            'max_id': f'{max_id}',
            'count': '20',
            'uid': f'{uid}',
            'locale': 'zh-CN',
        }
        sub_comment_flow_json = session.get('https://weibo.com/ajax/statuses/buildComments', params=sub_comment_flow_params, headers=comments_headers).json()
        for sub_comment in sub_comment_flow_json['data']:
            sub_comments_rst.append([post_id, sub_comment['id'], sub_comment['rootid'], sub_comment['readtimetype'], sub_comment['text_raw'], convert_weibo_comment_time_format(sub_comment['created_at']), sub_comment['like_counts'], sub_comment['user']['id']])
        max_id = sub_comment_flow_json['max_id']
    return sub_comments_rst
