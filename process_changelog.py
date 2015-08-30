import os
import sys

with open('CHANGELOG.md', 'r') as f:
	prev_lines = f.readlines()

os.system('github_changelog_generator -o temp.md')

with open('temp.md', 'r') as f:
	temp_lines = f.readlines()

headers = []
for i, line in enumerate(temp_lines):
	if line.startswith('## ['):
		headers.append(i)


with open('CHANGELOG.md', 'w') as f:
	f.writelines(temp_lines[:headers[1]-1])
	f.writelines(prev_lines[1:])