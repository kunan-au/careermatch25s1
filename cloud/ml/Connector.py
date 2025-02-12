import pandas as pd
import random

# Step 1: Create the department DataFrame from the provided data
department_data = {
    "department_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
    "department": [
        "frozen", "other", "bakery", "produce", "alcohol", "international", "beverages", "pets", "dry goods pasta", "bulk", "personal care",
        "meat seafood", "pantry", "breakfast", "canned goods", "dairy eggs", "household", "babies", "snacks", "deli", "missing"
    ]
}
departments_df = pd.DataFrame(department_data)

# Step 2: Load the product data from the provided CSV file
products_file_path = "/home/kunan/eCommerce_DEproject/existingData/products.csv"
products_df = pd.read_csv(products_file_path)

# Step 3: Simulate the ML results as a dictionary (replace this with your actual ML output)
ml_results = {
    "dairy": 5,
    "vegetables": 10,
    "grains": 8,
    "fruits": 3,
    "meat": 2
}

# Step 4: Combine ML results with departments, making up for missing values
# Map ML categories to department_id
category_to_department = {
    "dairy": 16,
    "vegetables": 4,
    "grains": 9,
    "fruits": 4,
    "meat": 12
}

combined_results = []
for category, count in ml_results.items():
    department_id = category_to_department.get(category, 21)  # Default to 'missing'
    combined_results.extend([department_id] * count)

# Make up missing entries by sampling from available departments
num_missing = 10  # Adjust the number of missing entries as needed
missing_entries = random.choices(department_data["department_id"], k=num_missing)
combined_results.extend(missing_entries)

# Convert to DataFrame
results_df = pd.DataFrame({"department_id": combined_results})

# Step 5: Merge results with products to extract relevant products
relevant_products_df = products_df[products_df["department_id"].isin(results_df["department_id"].unique())]

# Save the relevant products to a new CSV file
output_file_path = "/home/kunan/eCommerce_DEproject/ml/extracted_relevant_products.csv"
relevant_products_df.to_csv(output_file_path, index=False)

print(f"Relevant products have been saved to: {output_file_path}")
