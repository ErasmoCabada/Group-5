import json
import requests
import csv
import os

# Make sure the data folder exists
if not os.path.exists("data"):
    os.makedirs("data")

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lsttoken)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        print(f"Error: {e}")
    return jsonData, ct

def collect_author_touches(lstTokens, repo):
    ct = 0
    ipage = 1
    
    # Prepare the CSV file
    fileOutput = 'data/rootbeer_author_touches.csv'
    fileCSV = open(fileOutput, 'w', newline='', encoding='utf-8')
    writer = csv.writer(fileCSV)
    writer.writerow(["Filename", "Author", "Date"]) # Header row

    try:
        while True:
            spage = str(ipage)
            commitsUrl = f'https://api.github.com/repos/{repo}/commits?page={spage}&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lstTokens, ct)

            if not jsonCommits or len(jsonCommits) == 0:
                break

            for commitObj in jsonCommits:
                sha = commitObj['sha']
                # Get author name and date from the commit object
                # When 'author' is None in GitHub API, use 'commit' info
                author_name = commitObj['commit']['author']['name']
                commit_date = commitObj['commit']['author']['date']

                # Get the specific files for this commit
                shaUrl = f'https://api.github.com/repos/{repo}/commits/{sha}'
                shaDetails, ct = github_auth(shaUrl, lstTokens, ct)
                
                if 'files' in shaDetails:
                    for fileObj in shaDetails['files']:
                        filename = fileObj['filename']
                        
                        # Only look for source files
                        source_extensions = ('.java', '.kt', '.cpp', '.c', '.h')
                        if filename.lower().endswith(source_extensions):
                            # Write a row for every single touch
                            writer.writerow([filename, author_name, commit_date])
                            print(f"Recorded: {filename} by {author_name}")

            ipage += 1
    except Exception as e:
        print(f"Error during mining: {e}")
    finally:
        fileCSV.close()

# --- RUN SCRIPT ---
repo = 'scottyab/rootbeer'
# Insert Token
lstTokens = ["Lord Farquaad"] 

collect_author_touches(lstTokens, repo)
print("Done! Check data/rootbeer_author_touches.csv")