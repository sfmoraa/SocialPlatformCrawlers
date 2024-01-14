V1.0 

*实现了对微博主贴内容的爬取，以及对用户信息的爬取*

# 关键词爬取
在`main_crawl.py`中配置weibo_config的参数，然后调用`WeiboKeywordCrawl`函数，参数意义如下：

1. search_keyword：需要搜索的关键词
2. result_save_path：爬取结果的保存目录
3. search_date_range：搜索的日期范围，用一个列表指明搜索开始日期和结束日期（不含结束日期），格式形如 ["2023-12-25", "2023-12-26"]
4. weibo_cookies：为访问微博页面所必须的cookies，如果爬取失败考虑是否是cookies过期
5. crawl_user_ip_and_gender：是否在爬取贴文时一并爬取用户属地和性别，设置为False会提高爬取速度
6. crawl_comment：是否爬取主贴文之下的评论，在V2.0中实现

- 爬取结果以csv格式存储，各列意义分别为：

| comment | comment_time | likes | location | gender | 
|---------|--------------|-------|----------|--------|
| 评论内容    | 评论时间     | 赞数    | 评论者地区    | 评论者性别  |


# 爬取用户信息
使用`main_crawl.py`中的`WeiboGetUserInfo`函数，参数意义如下：
1. id_list：需要爬取的用户的id号列表
2. weibo_cookies：用于建立会话的用户cookie，可使用weibo_config['weibo_cookies']
3. result_save_path：爬取结果的保存目录，可使用weibo_config['result_save_path']

- 爬取结果以csv格式存储，各列意义分别为：

| user_id | name | gender | location | ip_location | friends_count | followers_count | created_at | desc | 
|---------|------|--------|----------|-------------|---------------|-----------------|------------|------|
| 用户id    | 用户名  | 性别     | 用户地区     | 用户ip属地      | 用户关注数         | 用户粉丝数           | 用户账号创建时间   | 用户描述 |                                                                                                                                      |