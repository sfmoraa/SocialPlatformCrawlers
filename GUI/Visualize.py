import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = 'SimHei'
import os
from pprint import pprint

def visualize_data_time(file_path, time_column):
    df = pd.read_csv(file_path)
    try:
        time_series = df.iloc[:, int(time_column) - 1]
        time_series = pd.to_datetime(time_series, unit='s')
    except:
        return None
    hourly_counts = time_series.groupby(time_series.dt.floor('D')).count()
    full_date_range = pd.date_range(start=time_series.min().floor('D'), end=time_series.max().floor('D'), freq='D')
    hourly_counts = hourly_counts.reindex(full_date_range, fill_value=0)

    fig, ax = plt.subplots()
    ax.plot(hourly_counts.index, hourly_counts.values)
    ax.set_title('时序变化趋势图')
    ax.set_xlabel('日期')
    ax.set_ylabel('总数')
    ax.set_aspect('auto')
    rst_save_path=os.path.splitext(file_path)[0]+'.png'
    fig.savefig(rst_save_path)
    plt.show()
    return rst_save_path

if __name__=='__main__':
    visualize_data_time('E:\pycharm\codes\SocialPlatformCrawlers\Results\WEIBO_张雪峰_20240312_22-57-41.csv', 5)
    # df=pd.read_csv('E:\pycharm\codes\SocialPlatformCrawlers\Results\梅西\梅西.csv')
    # df.to_excel('./output.xlsx', index=False)