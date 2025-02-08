import pandas as pd

# 加载数据
df = pd.read_csv('chunk_0_filtered.csv')  # 修改为你的文件路径

# 检查数据列名，并根据实际情况调整列名
print(df.columns)

# 合并列
df['Combined'] = ("Job Description: " + df['Job Description'] + "\n" +
                  "Skills: " + df['skills'] + "\n" +
                  "Responsibilities: " + df['Responsibilities'])

# 输出到新的 CSV 文件
df['Combined'].to_csv('chunk_0_filtered_combined.csv', index=False)  # 修改输出文件的路径
