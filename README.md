V2.0 

*实现了对微博主贴内容及所有可见评论的爬取，对账号信息的爬取*

# 关键词爬取
在`main_crawl.py`中配置weibo_config的参数，然后调用`WeiboKeywordCrawl`函数，参数意义如下：

1. search_keyword：需要搜索的关键词
2. result_save_path：爬取结果的保存目录
3. search_date_range：搜索的日期范围，用一个列表指明搜索开始日期和结束日期（不含结束日期），格式形如 ["2023-12-25", "2023-12-26"]
4. weibo_cookies：为访问微博页面所必须的cookies，如果爬取失败考虑是否是cookies过期
5. crawl_comment：是否爬取主贴文之下的评论

- 爬取结果以csv格式存储，各列意义分别为：
main_post_id,,,,,,,

| main_post_id | if_comment_id        | if_reply_root_id         | type                           | content | post_time | likes | user_id | 
|--------------|----------------------|--------------------------|--------------------------------|---------|-----------|-------|---------|
| 主贴子的id       | 若本条为评论，则代表本条id号，否则为空 | 若本条为回复，则代表本条回复所在的根评论的id号 | 本条内容类型，包括content、comment、comment_reply | 内容    | 发布时间      | 赞数    | 用户id    |


# 爬取用户信息
使用`main_crawl.py`中的`WeiboGetUserInfo`函数，参数意义如下：
1. id_list：需要爬取的用户的id号列表
2. weibo_cookies：用于建立会话的用户cookie，可使用weibo_config['weibo_cookies']
3. result_save_path：爬取结果的保存目录，可使用weibo_config['result_save_path']

- 爬取结果以csv格式存储，各列意义分别为：

| user_id | name | gender | location | ip_location | friends_count | followers_count | created_at | desc | 
|---------|------|--------|----------|-------------|---------------|-----------------|------------|------|
| 用户id    | 用户名  | 性别     | 用户地区     | 用户ip属地      | 用户关注数         | 用户粉丝数           | 用户账号创建时间   | 用户描述 |                                                                   

# 文件主要内容：
## WeiboCrawlMain
主要的爬取任务实现
### GetFullComments
爬取指定帖子的评论和子评论（评论回复）
### data_processinig
处理格式转换以及结果存储

# 各函数具体功能在对应文档内注明