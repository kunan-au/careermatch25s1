import pandas as pd

def split_csv(file_path, line_count=10000, max_splits=10):
    # Read Large Files
    with pd.read_csv(file_path, chunksize=line_count) as reader:
        for i, chunk in enumerate(reader):
            if i >= max_splits:  # Stop when reach the maximum number of iterations
                break
            # Add an index to the file name of each chunk
            chunk.to_csv(f'chunk_{i}.csv', index=False)

# Call the function
split_csv('job_descriptions.csv')
