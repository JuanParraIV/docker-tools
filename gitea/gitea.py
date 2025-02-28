from github import Github
import os
import json
import requests

# Github
GH_ACCESS_TOKEN = os.environ['GH_ACCESS_TOKEN']
# Gitea
GITEA_ACCESS_TOKEN = os.environ['GITEA_ACCESS_TOKEN']
GITEA_USERNAME = os.environ['GITEA_USERNAME']
GITEA_PASSWORD = os.environ['GITEA_PASSWORD']
TARGET_HOST = "http://192.168.50.143:3001/"
MIGRATE_URI = "/api/v1/repos/migrate"
ENDPOINT = "%s%s" % (TARGET_HOST, MIGRATE_URI)

g = Github(GH_ACCESS_TOKEN)

EXCLUDE = []

def getRepos(g):
	repos = []
	for repo in g.get_user().get_repos():
			r = {}
			r['name'] = str(repo.name)
			r['url'] = str(repo.url)
			r['description'] = str(repo.description)
			r['private'] = str(repo.private)
			repos.append(r)
	return repos

def createRepo(source_url,name,description,private):
	headers = { "accept": "application/json", "content-type": "application/json" }
	headers["Authorization"] = "token %s" % (GITEA_ACCESS_TOKEN)

	migrate_data = { "mirror": False, "uid": 1 }
	migrate_data["auth_password"] = "%s" % (GITEA_PASSWORD)
	migrate_data["auth_username"] = "%s" % (GITEA_USERNAME)
	migrate_data["description"] = "%s" % (description)
	migrate_data["repo_name"] = "%s" % (name)
	migrate_data["private"] = bool("%s" % (private))
	migrate_data["clone_addr"] = "%s.git" % (source_url.replace("api.","").replace("github.com/repos", "github.com"))
	migrate_data["repo_owner"] = GITEA_USERNAME

	print(migrate_data)

	try:
		r = requests.post(url=ENDPOINT, data=json.dumps(migrate_data), headers=headers)
		print(r.text)
		if r.status_code != 200:
			return "Non-OK Response: %s" % (r.status_code)
		else:
			return "Done: %s" % (source_url)
	except Exception as e:
		return e
	finally:
		pass

def runMigration(r,x):
	exclude_repos = x
	for repo in r:
		if repo['name'] in exclude_repos:
			print("Excluding %s" % (repo['name']))
		else:
			print("Working on %s" % (repo['name']))
			print(createRepo(repo['url'],repo['name'],repo['description'],repo['private']))

	return "Done"

if __name__ == '__main__':
	repos = getRepos(g)
	print(runMigration(repos,EXCLUDE))
