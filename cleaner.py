import json
import os

def extract_url_values(data, key='url'):
    if isinstance(data, dict):
        for k, v in data.items():
            if k == key:
                yield v
            else:
                yield from extract_url_values(v, key)
    elif isinstance(data, list):
        for item in data:
            yield from extract_url_values(item, key)

# Specify the file path and encoding
file_path = 'localhost.json'
file_encoding = 'utf-8'

# Load JSON data from file with specified encoding
with open(file_path, 'r', encoding=file_encoding) as f:
    json_data = json.load(f)

# Recursively extract URL values from JSON data
url_values = list(extract_url_values(json_data))

# Filter URL values to keep only those containing "localhost" and not ending with "/"
filtered_urls = [url for url in url_values if 'localhost' in url and not url.endswith('/')]

# Define the prefix to remove
prefix_to_remove = 'http://localhost/mycrolinks.com/'

# Create a list to store modified URLs (without the prefix)
retained_files = []

# Create a set to store unique first parts of split URLs
folder_names = set()

# Process each filtered URL
for url in filtered_urls:
    if url.startswith(prefix_to_remove):
        # Remove the prefix from the URL
        url_without_prefix = url[len(prefix_to_remove):]
        # Add the modified URL to the list
        url_without_prefix = url_without_prefix.replace("/", "\\")
        retained_files.append("C:\\xampp\\htdocs\\mycrolinks.com\\"+url_without_prefix)
        
        # Split the URL by '/' and get the first part
        parts = url_without_prefix.split('\\')
        if parts:
            folder_names.add(parts[0])

# Print the list of URLs without the prefix
print("Required_files:")
retained_files.sort()
for url in retained_files:
    print(url)

#remove duplicates
retained_files = list(dict.fromkeys(retained_files))

# Print the unique first parts extracted from URLs
# print("\nFolders:")
# for part in folder_names:
#     print(part)

# Create a list to store the file names
file_names = []
current_directory = "C:\\xampp\\htdocs\\mycrolinks.com"
for part in folder_names:
    # Get all files within the folders, including nested files
    for root, dirs, files in os.walk(os.path.join(current_directory, part)):
        for file in files:
            file_path = os.path.join(root, file)
            file_names.append(file_path)


# Print the list of non-existing files
# print("\nFile Names:")
# for file in file_names:
#     print(file)

# create a list of file names that exist in file_names but not in required_files
unwanted_files = [file for file in file_names if file not in retained_files]
print("\nUnwanted Files:")
for file in unwanted_files:
    print(file)

# Delete unwanted files
for file in unwanted_files:
    try:
        os.remove(file)
        print(f"Deleted file: {file}")
    except OSError as e:
        print(f"Failed to delete file: {file}, Error: {e}")

def delete_empty_directories(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir in dirs:
            folder_path = os.path.join(root, dir)
            if not os.listdir(folder_path):
                try:
                    os.rmdir(folder_path)
                    print(f"Deleted empty directory: {folder_path}")
                except OSError as e:
                    print(f"Failed to delete directory: {folder_path}, Error: {e}")

# Call the function to delete empty directories
delete_empty_directories(current_directory)
