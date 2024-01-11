# app.py
import sys
from import_document import import_document_file

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python app.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    # Your application logic with the file_path parameter
    print(f"Received file: {file_path}")
