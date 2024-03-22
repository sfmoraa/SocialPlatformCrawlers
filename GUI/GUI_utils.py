import os
from datetime import datetime
from GUI.Visualize import *

def check_weibo_config(config):
    if len(config['search_keyword'].strip()) == 0:
        return 1, "【搜索关键词不能为空】"
    if not os.path.exists(config['result_save_path']):
        return 2, "【路径不存在】"
    try:
        datetime.strptime(config['search_date_range'][0], '%Y-%m-%d')
        datetime.strptime(config['search_date_range'][1], '%Y-%m-%d')
    except ValueError:
        return 3, "【日期不合法，请使用YYYY-MM-DD格式并确保日期合理】"
    if len(config['weibo_cookies']["SUB"].strip()) == 0:
        return 4, "【微博搜索要求使用cookie，请填入SUB的值】"
    return 0, "【任务设置成功！】"


def check_zhihu_config(config):
    if len(config['question_number_list']) == 0:
        return 1, "【问题号不能为空】"
    if not os.path.exists(config['result_save_path']):
        return 2, "【路径不存在】"
    return 0, "【任务设置成功！】"


def check_bilibili_config(config):
    if len(config['keyword'].strip()) == 0:
        return 1, "【搜索关键词不能为空】"
    if not os.path.exists(config['save_dir']):
        return 2, "【路径不存在】"
    return 0, "【任务设置成功！】"


def check_visualize_config(config):
    try:
        column_number = int(config['time_column'])
        if column_number < 1:
            return 1, "【检查配置！请输入从1开始的列号】",None
    except ValueError:
        return 1, "【检查配置！请输入从1开始的列号】",None
    if not os.path.exists(config['file_path']):
        return 2, "【路径不存在】",None
    pic_save_path = visualize_data_time(config['file_path'], config['time_column'])
    if pic_save_path is None:
        return 3,"【数据格式不正确！无法被读取为时间，请确保此列为时间戳】",None

    return 0, "【正在计算中！】",pic_save_path
