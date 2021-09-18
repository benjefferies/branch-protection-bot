# Branch Protection Bot
A bot tool to temporarily disable and re-enable `Include administrators` option in branch protection

Github doesn't have a way to give a Bot access to override the branch protection, specifically if you [include administrators](https://github.com/isaacs/github/issues/1390).
The only possible solution is to disable the `include administrators` option. This increases risk of accidental pushes to master from administrators (I've done it a few times).
This tool doesn't completely solve the problem of accidents happening but reduces the chances by closing the window.

The intended use of this tool is to is in a CI/CD pipeline where you require temporary access to allow a administrator Bot push to a branch.

## How it works
1. Your automated pipeline is kicked off
1. Before you push to github you run this tool to disable `Include administrators`
1. Push to the repository
1. After you push to github you run this tool to enable `Include administrators`

## Example usage
### Docker
```
docker run -e ACCESS_TOKEN=abc123 -e BRANCH=master -e REPO=branch-protection-bot -e OWNER=benjefferies benjjefferies/branch-protection-bot
```

### Github Actions

```
- name: Temporarily disable "include administrators" branch protection
  uses: benjefferies/branch-protection-bot@master
  if: always()
  with:
    access_token: ${{ secrets.ACCESS_TOKEN }}
    branch: ${{ github.event.repository.default_branch }}
    
- name: Deploy
  run: |
    mvn release:prepare -B
    mvn release:perform -B
   
- name: Enable "include administrators" branch protection
  uses: benjefferies/branch-protection-bot@master
  if: always()  # Force to always run this step to ensure "include administrators" is always turned back on
  with:
    access_token: ${{ secrets.ACCESS_TOKEN }}
    owner: benjefferies
    repo: branch-protection-bot
    branch: ${{ github.event.repository.default_branch }}
```

#### Inputs

##### `access_token`

**Required** Github access token. https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line. Requires full repository access scope

##### `owner`

For example benjefferies for https://github.com/benjefferies/branch-protection-bot. If not set with repo GITHUB_REPOSITORY variable will be used

##### `repo`

For example branch-protection-bot for https://github.com/benjefferies/branch-protection-bot. If not set with repo GITHUB_REPOSITORY variable will be used

##### `branch`

Branch name. Default `"master"`

##### `retries`

Number of times to retry before exiting. Default `5`.

##### `enforce_admins`

If you want to pin the state of `Include administrators` for a step in the workflow.

#### Outputs

##### `initial_status`

Output the current branch protection status of `Include administrators` prior to any change.
You can retrieve it from any next step in your job using: `${{ steps.disable_include_admins.outputs.initial_status }}`.
This would help you to restore the initial setting this way:

```yaml
steps:
    - name: "Temporarily disable 'include administrators' default branch protection"
    id: disable_include_admins
    uses: benjefferies/branch-protection-bot@master
    if: always()
    with:
        access_token: ${{ secrets.ACCESS_TOKEN }}
        branch: ${{ github.event.repository.default_branch }}
        enforce_admins: false
    
    - ...

    - name: "Restore 'include administrators' default branch protection"
    uses: benjefferies/branch-protection-bot@master
    if: always() # Force to always run this step to ensure "include administrators" is always turned back on
    with:
        access_token: ${{ secrets.ACCESS_TOKEN }}
        branch: ${{ github.event.repository.default_branch }}
        enforce_admins: ${{ steps.disable_include_admins.outputs.initial_status }}
```

## Github repository settings
The Bot account must be an administrator.
