import pandas as pd
import uuid
from datetime import datetime
import random

def process_csv(file_path):
    # 读取CSV文件
    df = pd.read_csv(file_path, usecols=['Job Title', 'Company', 'Job Description'])
    
    # 为每一行生成UUID和时间戳
    df['id'] = [str(uuid.uuid4()) for _ in range(len(df))]
    df['created_at'] = [datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] for _ in range(len(df))]
    
    # 为每一行随机生成职位类型
    job_types = ['ft', 'pt', 'ct', 'cv']
    df['job_type'] = [random.choice(job_types) for _ in range(len(df))]
    
    # 修改列名
    df.rename(columns={
        'Job Title': 'title',
        'Company': 'company',
        'Job Description': 'description'
    }, inplace=True)

    # 生成SQL文件
    with open(file_path.replace('.csv', '_insert.sql'), 'w') as f:
        # 添加删除所有记录的SQL语句
        f.write("DELETE FROM jobs;\n")
        for _, row in df.iterrows():
            sql = f"INSERT INTO jobs (id, title, company, description, job_type, created_at) VALUES ('{row['id']}', '{row['title'].replace("'", "''")}', '{row['company'].replace("'", "''")}', '{row['description'].replace("'", "''")}', '{row['job_type']}', '{row['created_at']}');\n"
            f.write(sql)

# 调用函数
file_path = 'chunk_0_filtered.csv'
process_csv(file_path)