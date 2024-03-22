import pandas as pd
from datetime import datetime,timedelta


def convert_weibo_time_format(time_str, current_time):
    current_datetime = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
    if '秒前' in time_str:
        seconds = int(time_str.replace('秒前', ''))
        converted_datetime = current_datetime - timedelta(seconds=seconds)
    elif '分钟前' in time_str:
        minutes = int(time_str.replace('分钟前', ''))
        converted_datetime = current_datetime - timedelta(minutes=minutes)
    elif '今天' in time_str:
        time_only = time_str.replace('今天', '')
        time_parts = time_only.split(':')
        converted_datetime = datetime(current_datetime.year, current_datetime.month, current_datetime.day,
                                      int(time_parts[0]), int(time_parts[1]))
    elif '年' in time_str:
        converted_datetime = datetime.strptime(time_str, '%Y年%m月%d日 %H:%M')
    else:
        converted_datetime = datetime.strptime(time_str, '%m月%d日 %H:%M')
        converted_datetime=converted_datetime+timedelta(days=(datetime(datetime.now().year, 1, 1) - datetime(converted_datetime.year, 1, 1)).days)

    # return converted_datetime.strftime('%Y-%m-%d %H:%M')
    return str(int(converted_datetime.timestamp()))


def convert_weibo_comment_time_format(time_str):
    date_object = datetime.strptime(time_str, "%a %b %d %H:%M:%S %z %Y")
    # formatted_date = date_object.strftime("%Y-%m-%d %H:%M")
    formatted_date = str(int(date_object.timestamp()))
    return formatted_date


def weibo_store_data(data_list, output_path, topic, query_time):
    df = pd.DataFrame(data_list, columns=["main_post_id","if_comment_id","if_reply_root_id","type","content","post_time","likes","user_id"])
    df.to_csv(output_path, index=False, encoding='utf-8-sig')



