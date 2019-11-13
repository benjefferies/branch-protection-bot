#!/usr/bin/env python

from time import sleep

import configargparse
from github3 import login
from github3.exceptions import NotFoundError, GitHubException


def toggle_enforce_admin(access_token, owner, repo_name, branch_name, retries):
    # or using an access token
    gh = login(token=access_token)
    try:
        repo = gh.repository(owner, repo_name)
    except NotFoundError:
        print(f"Could not find repo https://github.com/{owner}/{repo_name}")
        raise
    branch = repo.branch(branch_name)
    protection = branch.protection()
    print(f"Enforce admins branch protection enabled? {protection.enforce_admins.enabled}")
    print(f"Setting enforce admins branch protection to {not protection.enforce_admins.enabled}")
    for i in range(retries):
        try:
            if protection.enforce_admins.enabled:
                protection.enforce_admins.disable()
                return
            else:
                protection.enforce_admins.enable()
                return
        except GitHubException:
            print(f"Failed to set enforce admins to {not protection.enforce_admins.enabled}. Retrying...")
            sleep(i ** 2)  # Exponential back-off

    print(f"Failed to set enforce admins to {not protection.enforce_admins.enabled}.")
    exit(1)


if __name__ == '__main__':
    p = configargparse.ArgParser()
    p.add_argument('-t', '--access-token', env_var='ACCESS_TOKEN', required=True, help='Github access token. https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line')
    p.add_argument('-o', '--owner', env_var='OWNER', required=True, help='Owner. For example benjefferies for https://github.com/benjefferies/branch-protection-bot')
    p.add_argument('-r', '--repo', env_var='REPO', required=True, help='Repo. For example branch-protection-bot for https://github.com/benjefferies/branch-protection-bot')
    p.add_argument('-b', '--branch', env_var='BRANCH', default='master', help='Branch name')
    p.add_argument('--retries', env_var='RETRIES', default=5, help='Number of times to retry before exiting')

    options = p.parse_args()
    toggle_enforce_admin(options.access_token, options.owner, options.repo, options.branch, options.retries)
