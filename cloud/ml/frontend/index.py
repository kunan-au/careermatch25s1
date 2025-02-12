from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Key for session management

# Load Relevant Products
def load_relevant_products():
    file_path = "/home/kunan/eCommerce_DEproject/ml/extracted_relevant_products.csv"
    df = pd.read_csv(file_path)
    return df

products_df = load_relevant_products()

# Function to get most popular departments (Admin only)
def get_most_popular():
    if products_df.empty:
        return []  # Return empty list if DataFrame is empty
    popular = products_df['department_id'].value_counts().head(5).reset_index()
    popular.columns = ['department_id', 'count']
    return popular.to_dict(orient='records')

# Function to get recommendations (User only)
def get_recommendations():
    if not products_df.empty:
        return products_df.sample(min(10, len(products_df))).to_dict(orient='records')  # Recommend up to 10 products
    return []

# Function to get popular products (User-specific)
def get_popular_products():
    if products_df.empty:
        return []  # Return empty list if DataFrame is empty
    # Fetch top 5 popular products based on department counts
    popular_products = (
        products_df.groupby(["department_id", "product_id", "product_name"])
        .size()
        .reset_index(name="count")
        .sort_values(by="count", ascending=False)
        .head(5)
    )
    return popular_products.to_dict(orient="records")

# Function to get data for admin visualizations
def get_visualizations():
    if products_df.empty:
        return {}
    department_counts = products_df['department_id'].value_counts().to_dict()
    return department_counts

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == '111' and password == '111':
            session['username'] = username
            if request.form.get('admin'):
                session['user_type'] = 'admin'
                return redirect(url_for('admin_dashboard'))
            session['user_type'] = 'user'
            return redirect(url_for('user_dashboard'))
        return "Invalid credentials! Please try again."
    return render_template('login.html')

@app.route('/user_dashboard')
def user_dashboard():
    if 'username' not in session or session.get('user_type') != 'user':
        return redirect(url_for('login'))

    recommendations = get_recommendations()  # User-specific recommendations
    popular_products = get_popular_products()  # Popular products for the user
    return render_template('user_dashboard.html', recommendations=recommendations, popular_products=popular_products)

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'username' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('login'))

    most_popular = get_most_popular()  # Most popular products for admin
    visualization_data = get_visualizations()  # Visualization data for admin
    return render_template('admin_dashboard.html', most_popular=most_popular, visualization_data=visualization_data)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
