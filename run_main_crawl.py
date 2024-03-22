from Weibo.WeiboCrawlMain import WeiboKeywordCrawl, WeiboGetUserInfo
from Zhihu.ZhihuCrawlMain import ZhihuQuestionCrawl
from Bilibili.BilibiliCrawlMain import BilibiliVideoCrawl

weibo_config = {
    'search_keyword': "张雪峰",
    'result_save_path': "./Results",
    'search_date_range': ["2023-12-1", "2023-12-2"],
    'weibo_cookies': {
        "SUB": "_2A25I9WR_DeRhGeFG7FQZ-CrMyTuIHXVri_m3rDV8PUJbkNB-LRPtkW1NeMOQzWA74hlqBFzu9YI637-8pP33q9xT",
    },
    'crawl_comment': True
}

WeiboKeywordCrawl(**weibo_config)
exit(9)
# WeiboGetUserInfo(id_list=[1218966851,3290016493,2222325],weibo_cookies=weibo_config['weibo_cookies'],result_save_path=weibo_config['result_save_path'])

zhihu_config = {
    'question_number_list': ['636636956', '646987953'],
    'result_save_path': "./Results",
}

# ZhihuQuestionCrawl(**zhihu_config)

bilibili_config = {
    'keyword': '梅西',
    'save_dir': './Results',
    'crawl_comments': True
}

# BilibiliVideoCrawl(**bilibili_config)
