import sys

# A simple test function
def main():
    print("Hello, AWS Glue!")
    print("This is a test script to verify Glue job functionality.")
    print(f"Number of arguments passed: {len(sys.argv)}")
    print("Arguments:", sys.argv)

if __name__ == "__main__":
    main()
