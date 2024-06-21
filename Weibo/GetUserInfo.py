import requests
import csv
import time
import os

"""************************************************ 修改cookie的SUB为自己的.weibo.com对应值 ************************************************"""

weibo_cookie = {'SUB': '_2AkMRKb0Xf8NxqwFRmfwRxG7iZYt1yA3EieKndUzMJRMxHRl-yT8XqhcstRB6OqmT-L-NMDuEAncPNUPVjLyAIFzAX48E'}

data_path = "../Results/WeiboUserInfo/UserData.csv"
avatar_directory_path = "../Results/WeiboUserInfo/Avatars"

weibo_headers = {
    'authority': 'weibo.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
}


def download_and_show_image(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
    else:
        print(f"无法下载{save_path}图片，HTTP状态码: {response.status_code}")


def save_data(data):
    title = ['id', 'name', 'description', 'followers_count', 'friends_count', 'statuses_count', 'total_cnt', 'location', 'gender', 'verified', 'verified_reason', 'birthday', 'created_at', 'sunshine_credit', 'mbrank', 'mbtype', 'company', 'school']
    file_exists = os.path.isfile(data_path)
    with open(data_path, "a", encoding="utf-8", newline="") as fi:
        writer = csv.writer(fi)
        if not file_exists:
            writer.writerow(title)  # 写入列头
        writer.writerow([data.get(k, '') for k in title])  # 追加数据


def get_data(mysession, id):
    responses1 = mysession.get(f"https://weibo.com/ajax/profile/info?uid={id}", headers=weibo_headers)
    responses2 = mysession.get(f"https://weibo.com/ajax/profile/detail?uid={id}", headers=weibo_headers)

    try:
        data1 = responses1.json()['data']['user']
        data2 = responses2.json()['data']
    except:
        print("【ID", id, "Failed to load】")
        return

    download_and_show_image(data1["avatar_large"], f'{avatar_directory_path}/{id}.jpg')

    data = {'id': id}
    data['name'] = data1['screen_name']  # 名字
    data['description'] = data1['description']  # 个人简介
    data['followers_count'] = data1['followers_count']  # 粉丝数量
    data['friends_count'] = data1['friends_count']  # 关注数量
    data['statuses_count'] = data1['statuses_count']  # 博文数量
    data['total_cnt'] = data1["status_total_counter"]["total_cnt"]  # 转评赞
    data['location'] = data1['location']  # 所在地区
    data['gender'] = data1['gender']  # 性别：f:女, m:男
    data['verified'] = data1['verified']  # 是否认证
    try:
        data['verified_reason'] = data1['verified_reason']  # 认证信息
    except KeyError:
        data['verified_reason'] = ""
    data['mbrank'] = data1['mbrank']
    data['mbtype'] = data1['mbtype']
    try:
        data['birthday'] = data2['birthday']  # 生日
    except KeyError:
        data['birthday'] = ""
    try:
        data['created_at'] = data2['created_at']  # 注册时间
    except KeyError:
        data['created_at'] = ""
    try:
        data['sunshine_credit'] = data2['sunshine_credit']['level']  # 阳光信用
    except KeyError:
        data['sunshine_credit'] = ""
    try:
        data['company'] = data2['career']['company']  # 公司
    except KeyError:
        data['company'] = ""
    try:
        data['school'] = data2['education']['school']  # 学校
    except KeyError:
        data['school'] = ""

    save_data(data)


def removeDuplicateIds(file_path):
    with open(file_path, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)

    id_map = {}
    for row in rows:
        id_map[row['id']] = row

    # 保留靠后的结果
    unique_data = list(id_map.values())

    with open(file_path, 'w', newline='', encoding='utf-8') as outfile:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(unique_data)

    print("Duplicates removed and file updated.")


if __name__ == '__main__':
    uid = ['6318319468', '6251534126', '7203075998', '5625727476', '5615418877', '7916854426', '7626514031', '5286147999', '7760921692']

    weibo_session = requests.Session()
    weibo_session.cookies.update(weibo_cookie)
    for id in uid:
        print(id)
        get_data(weibo_session, id)
        time.sleep(3)
    removeDuplicateIds(data_path)
