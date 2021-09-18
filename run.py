#!/usr/bin/env python
from distutils.util import strtobool
from time import sleep

import configargparse
from github3 import login
from github3.exceptions import NotFoundError, GitHubException


def toggle_enforce_admin(options):
    access_token, owner, repo_name, branch_name, retries, github_repository = options.access_token, options.owner, options.repo, options.branch, int(options.retries), options.github_repository
    if not owner and not repo_name and github_repository and "/" in github_repository:
        owner = github_repository.split("/")[0]
        repo_name = github_repository.split("/")[1]

    if owner == '' or repo_name == '':
        print('Owner and repo or GITHUB_REPOSITORY not set')
        raise RuntimeError
    enforce_admins = bool(strtobool(options.enforce_admins)) if options.enforce_admins is not None and not options.enforce_admins == '' else None
    # or using an access token
    print(f"Getting branch protection settings for {owner}/{repo_name}")
    protection = get_protection(access_token, branch_name, owner, repo_name)
    print(f"Enforce admins branch protection enabled? {protection.enforce_admins.enabled}")
    # save the current status for use later on if desired
    print(f"::set-output name=initial_status::{protection.enforce_admins.enabled}")
    print(f"Setting enforce admins branch protection to {enforce_admins if enforce_admins is not None else not protection.enforce_admins.enabled}")
    for i in range(retries):
        try:
            if enforce_admins is False:
                disable(protection)
                return
            elif enforce_admins is True:
                enable(protection)
                return
            elif protection.enforce_admins.enabled:
                disable(protection)
                return
            elif not protection.enforce_admins.enabled:
                enable(protection)
                return
        except GitHubException:
            print(f"Failed to set enforce admins to {not protection.enforce_admins.enabled}. Retrying...")
            sleep(i ** 2)  # Exponential back-off

    print(f"Failed to set enforce admins to {not protection.enforce_admins.enabled}.")
    exit(1)


def get_protection(access_token, branch_name, owner, repo_name):
    gh = login(token=access_token)
    if gh is None:
        print(f"Could not login. Have you provided credentials?")
        raise exit(1)

    try:
        repo = gh.repository(owner, repo_name)
    except NotFoundError:
        print(f"Could not find repo https://github.com/{owner}/{repo_name}")
        raise
    branch = repo.branch(branch_name)
    protection = branch.protection()
    return protection


def enable(protection):
    protection.enforce_admins.enable()


def disable(protection):
    protection.enforce_admins.disable()


if __name__ == '__main__':
    p = configargparse.ArgParser()
    p.add_argument('-t', '--access-token', env_var='ACCESS_TOKEN', required=True, help='Github access token. https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line')
    p.add_argument('-o', '--owner', env_var='OWNER', required=False, default='', help='Owner. For example benjefferies for https://github.com/benjefferies/branch-protection-bot')
    p.add_argument('-r', '--repo', env_var='REPO', required=False, default='', help='Repo. For example branch-protection-bot for https://github.com/benjefferies/branch-protection-bot')
    p.add_argument('--github_repository', env_var='GITHUB_REPOSITORY', required=False, default='', help='Owner and repo. For example benjefferies/branch-protection-bot for https://github.com/benjefferies/branch-protection-bot')
    p.add_argument('-b', '--branch', env_var='BRANCH', default='master', help='Branch name')
    p.add_argument('--retries', env_var='RETRIES', default=5, help='Number of times to retry before exiting')
    p.add_argument('--enforce-admins', env_var='ENFORCE_ADMINS', default=None, help='Flag to explicitly enable or disable "Include administrators"')

    toggle_enforce_admin(p.parse_args())
