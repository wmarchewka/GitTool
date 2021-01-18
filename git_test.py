import git
import os

rw_dir = '~/Desktop/'

import git

#
# origin = empty_repo.create_remote('origin', repo.remotes.origin.url)

# repo = git.Repo('test_repo')
repo = git.Repo.init(os.path.join(rw_dir, 'testrepo'))
# List remotes

# Create a new remote
try:
    remote = repo.create_remote('origin', url='git@github.com:siemensbte/testrepo')
except git.exc.GitCommandError as error:
    print(f'Error creating remote: {error}')

# Reference a remote by its name as part of the object
print(f'Remote name: {repo.remotes.origin.name}')
print(f'Remote URL: {repo.remotes.origin.url}')

# Push changes
print(repo.remotes.origin.push())
