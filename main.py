from bs4 import BeautifulSoup
import requests
import json


class Organization:
    def __init__(self, name, employee_names) -> None:
        self.name = name
        self.employee_names = employee_names
        self.commit_count = 0
        self.add_count = 0
        self.delete_count = 0

    def __str__(self):
        return self.name + " has " + str(len(self.employee_names) + 1) + " Employees which made: " + format(self.commit_count, ',d').replace(',', '.') + " Commits, " + format(self.add_count, ',d').replace(',', '.') + " New Lines, " + format(self.delete_count, ',d').replace(',', '.') + " Deleted Lines"


def get_orgname_by_username(username):
    page = requests.get("https://github.com/" + username)
    soup = BeautifulSoup(page.text, "html.parser")

    org = soup.find_all(class_="p-org")
    if len(org) == 0:
        print(username + " has no organization")
        return None

    return org[0].findChild("div").text


f = open('contributors.json')
json_res = json.load(f)
f.close()

orgs = [Organization("None", [])]

for res in json_res:
    org_name = get_orgname_by_username(res["author"]["login"])
    if org_name == None:
        org_name = "None"

    list_org = next((org for org in orgs if org.name == org_name), None)
    if list_org == None:
        list_org = Organization(org_name, [])
        orgs.append(list_org)
    else:
        list_org.employee_names.append(res["author"]["login"])

    for week in res["weeks"]:
        list_org.commit_count += week["c"]
        list_org.add_count += week["a"]
        list_org.delete_count += week["d"]

for org in orgs:
    print(org.__str__())
