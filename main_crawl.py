from Weibo.WeiboCrawlMain import WeiboKeywordCrawl,WeiboGetUserInfo

weibo_config = {
    'search_keyword': "张雪峰",
    'result_save_path': "./Results",
    'search_date_range': ["2023-12-25", "2023-12-26"],
    'weibo_cookies': {
        "SUB": "_2A25ImS9HDeRhGeFG7FQZ-CrMyTuIHXVr1y6PrDV8PUJbkNANLRjzkW1NeMOQzQYCnfRz0RERO3421FpC-CrzExXg",
    },
    'crawl_user_ip_and_gender':True,
    'crawl_comment':True
}

WeiboKeywordCrawl(**weibo_config)

# WeiboGetUserInfo(id_list=[1218966851,3290016493,1691328753],weibo_cookies=weibo_config['weibo_cookies'],result_save_path=weibo_config['result_save_path'])