import pandas as pd

def zhihu_store_data(data_list, output_path, topic):
    df = pd.DataFrame(data_list, columns=[topic, "gender", "comments", "likes", "updated_time","IP"])
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
