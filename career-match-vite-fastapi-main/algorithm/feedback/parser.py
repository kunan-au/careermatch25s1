import os
from llama_parse import LlamaParse

def parse_pdf(pdf_path, api_key=None):
    """
    Parse a PDF file and return its content as a string.
    
    :param pdf_path: Path to the PDF file
    :param api_key: LlamaParse API key (optional, will use environment variable if not provided)
    :return: String containing the text content of the PDF
    """
    # Get the API key from the parameter or environment variable
    llmaparse_api_key = api_key or os.getenv("LLMAPARSE_API_KEY")

    if not llmaparse_api_key:
        raise ValueError("LlamaParse API key is not provided and LLMAPARSE_API_KEY environment variable is not set.")

    try:
        # Initialize LlamaParse
        parser = LlamaParse(api_key=llmaparse_api_key, result_type="markdown")
        
        # Parse the PDF
        result = parser.load_data(pdf_path)
        
        # Extract text from the result
        if isinstance(result, list):
            return "\n\n".join(doc.text if hasattr(doc, 'text') else str(doc) for doc in result)
        elif hasattr(result, 'text'):
            return result.text
        else:
            return str(result)
    
    except Exception as e:
        print(f"Error parsing PDF: {str(e)}")
        return None

# Example usage (can be removed when using as a module)
if __name__ == "__main__":
    # Example PDF path
    example_pdf_path = "/Users/zhongyusi/COMP8715/career-match-vite-fastapi/algorithm/archive/data/data/ACCOUNTANT/10554236.pdf"
    
    # Check if the file exists
    if not os.path.exists(example_pdf_path):
        print(f"The file {example_pdf_path} does not exist.")
    else:
        # Parse the PDF
        pdf_text = parse_pdf(example_pdf_path)
        
        if pdf_text:
            print("Parsed PDF content:")
            print(type(pdf_text))
            print(pdf_text)
        else:
            print("Failed to parse the PDF.")