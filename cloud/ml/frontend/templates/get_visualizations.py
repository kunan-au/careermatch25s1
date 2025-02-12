import matplotlib.pyplot as plt

def get_visualizations():
    department_counts = products_df['department_id'].value_counts()

    # Save a bar chart
    plt.figure(figsize=(8, 6))
    department_counts.plot(kind='bar', color='skyblue')
    plt.title('Product Distribution by Department')
    plt.xlabel('Department ID')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig('/home/kunan/eCommerce_DEproject/ml/frontend/static/department_distribution.png')
    plt.close()

    # Return the raw data for admin dashboard
    return department_counts.to_dict()
