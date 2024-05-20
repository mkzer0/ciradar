import pandas as pd
from github import Github, GithubException
from tqdm import tqdm
import time
import datetime
import requests  # For handling requests specific exceptions
import os

def execute(token, repo_name, csv_file_path, batch_size=500):
    g = Github(token, timeout=60)  # Timeout increased to 60 seconds
    last_processed_file = 'last_processed_pr.txt'  # File to store last processed PR ID

    def get_last_processed_pr():
        try:
            with open(last_processed_file, 'r') as file:
                return int(file.read().strip())
        except FileNotFoundError:
            return None

    def set_last_processed_pr(pr_id):
        with open(last_processed_file, 'w') as file:
            file.write(str(pr_id))

    def write_data_to_csv(data, path, write_header=True):
        df = pd.DataFrame(data)
        df.to_csv(path, mode='a', header=write_header, index=False)

    while True:
        try:
            repo = g.get_repo(repo_name)
            pulls_main = repo.get_pulls(state='closed', base='main')
            pulls_master = repo.get_pulls(state='closed', base='master')
            pulls = list(pulls_main) + list(pulls_master)
            total_pulls = len(pulls)
            print(f"Total Pull Requests: {total_pulls}")

            last_processed_pr = get_last_processed_pr()
            start_index = 0
            if last_processed_pr is not None:
                for i, pr in enumerate(pulls):
                    if pr.id == last_processed_pr:
                        start_index = i + 1
                        break

            # Check if CSV file already exists to determine if headers should be written
            write_header = not os.path.exists(csv_file_path)

            for pr in tqdm(pulls[start_index:], desc='Processing PRs'):
                if pr.merged:
                    commits = pr.get_commits()
                    total_additions = 0
                    total_deletions = 0
                    total_commits = commits.totalCount if commits.totalCount > 0 else 0
                    for commit in commits:
                        try:
                            c = repo.get_commit(sha=commit.sha)
                            total_additions += c.stats.additions
                            total_deletions += c.stats.deletions
                        except requests.exceptions.ReadTimeout:
                            print(f"Timeout occurred while fetching commit {commit.sha}, skipping...")
                            continue

                    if total_commits > 0:
                        first_commit_date = commits[0].commit.author.date
                        merge_date = pr.merged_at
                        time_to_integration = (pd.to_datetime(merge_date) - pd.to_datetime(first_commit_date)).total_seconds() / 86400.0

                        pr_data = [{
                            'Merge Date': merge_date.strftime('%Y-%m-%d %H:%M:%S'),
                            'Time to Integration (days)': time_to_integration,
                            'Number of Commits': total_commits,
                            'Total Additions': total_additions,
                            'Total Deletions': total_deletions,
                            'Total Lines Changed': total_additions + total_deletions
                        }]
                        write_data_to_csv(pr_data, csv_file_path, write_header=write_header)
                        write_header = False  # Ensure headers are not written again after the first write

                    set_last_processed_pr(pr.id)
            break  # Exit loop if successful
        except (GithubException, requests.exceptions.RequestException) as e:
            print(f"An error occurred: {e}. Retrying in 1 hour...")
            time.sleep(3600)  # Wait for 1 hour before retrying
