import json
import os

import requests
from dotenv import load_dotenv

load_dotenv("./.env")


user_name = os.getenv("USER_NAME", None)
token = os.getenv("token", 0)


def get_repos(user):
    r = requests.get(
        f'https://api.github.com/users/{user_name}/repos', auth=(user_name, token)
    )

    if r.status_code !=200:
        print(f"User {user_name} was not found")

    repos = []
    for i in r.json():
        repo = dict()
        try:
            repo["id"] = i["id"]
            repo["full_name"] = i["full_name"]
            repo["svn_url"] = i["svn_url"]
        except KeyError as err:
            print(f"Undefined key: {err}")
        finally:
            repos.append(repo)
    return repos


def repos_to_json(repos):
    repos_json = json.dumps(repos)
    return repos_json


def save_json(json_info, filename="github_json"):
    with open(filename, "w") as f:
        json.dump(json_info, f, indent=2)


def main():
    repos = get_repos(user_name)
    if not repos:
        return None
    repos_json = repos_to_json(repos)
    save_json(repos_json)


if __name__ == "__main__":
    main()
