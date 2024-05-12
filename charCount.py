import requests
import json
import base64
import os
from dotenv import load_dotenv
from collections import Counter


def github_read_file(base_url, repository_name, file_path, username, token):
 
    # Construct the url of the file that is to be read and request for the content
    file_url = f"{base_url}/repos/{repository_name}/contents/{file_path}"
    response = requests.get(file_url, auth=(username,token))

    # If successful response is received, continue with further processing
    if response.status_code == 200:
        data = response.json()
        file_content = data['content']
        file_content_encoding = data.get('encoding')
        # Decode the file if the content is encoded
        if file_content_encoding == 'base64':
            file_content = base64.b64decode(file_content).decode()

    # Display the error code if we fail to retrieve the file
    else:
        print(f"Failed to retrieve file. Status code: {response.status_code}")

    return file_content


def github_repo_char_count(base_url, repository_name, username, token):

    # Construct the url of the repository to be connected and request for the tree
    repositories_url = f"{base_url}/repos/{repository_name}/git/trees/main?recursive=1"
    response = requests.get(repositories_url, auth=(username,token))
    
    # If successful response is received, continue with further processing
    if response.status_code == 200:
        repositories = response.json()
        d = Counter()

        # Loop over each file in the tree
        for file in repositories['tree']:
            if file['path'].endswith(".js") or file['path'].endswith(".ts"):
                # If the file is .js or .ts, call the function to read it's content
                content = github_read_file(base_url, repository_name, file['path'], username, token)
                # Collect all the letters in the file in a list
                char_list = [char for char in content.lower() if char.isalpha()]
                # Update the global counter with each list
                d.update(Counter(char_list))

        # Print the final counts of each letter in descending order
        for key, count in d.most_common():
            print("{}: {}".format(key, count))
 
   # Display the error code if we fail to retrieve the repository
    else:
        print(f"Failed to retrieve repositories. Status code: {response.status_code}")


def main():

    # Load .env file to access all the necessary environmental variables
    load_dotenv()
    base_url = os.environ['GITHUB_BASE_URL'] 
    repository_name = os.environ['GITHUB_REPO']
    username = os.environ['GITHUB_USERNAME']
    token = os.environ['GITHUB_TOKEN']

    # Function that calculates and displays the count of each character in the repository
    github_repo_char_count(base_url, repository_name, username, token)


if __name__ == '__main__':
    main()
