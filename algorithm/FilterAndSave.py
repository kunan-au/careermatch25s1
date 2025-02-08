import pandas as pd

def filter_csv(file_path, columns_to_keep):
    # 读取指定列
    df = pd.read_csv(file_path, usecols=columns_to_keep)
    # 构建新的文件名
    new_file_path = file_path.replace('.csv', '_filtered.csv')
    # 保存到相同目录
    df.to_csv(new_file_path, index=False)

# 要保留的列
columns_to_keep = ['Job Title', 'Company', 'Job Description']

# 要处理的特定文件路径
file_path = 'chunk_0.csv'

# 调用函数
filter_csv(file_path, columns_to_keep)
