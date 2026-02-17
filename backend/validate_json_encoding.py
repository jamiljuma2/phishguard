import sys

file_path = sys.argv[1] if len(sys.argv) > 1 else "serviceAccountKey.json"

try:
    with open(file_path, "rb") as f:
        raw = f.read()
    try:
        decoded = raw.decode("utf-8")
        print("File is valid UTF-8.")
    except UnicodeDecodeError as e:
        print(f"File is NOT valid UTF-8: {e}")
        sys.exit(1)
    import json
    try:
        json.loads(decoded)
        print("File contains valid JSON.")
    except Exception as e:
        print(f"File does NOT contain valid JSON: {e}")
        sys.exit(2)
except Exception as e:
    print(f"Error reading file: {e}")
    sys.exit(3)
