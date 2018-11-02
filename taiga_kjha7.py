import getpass
import requests
import json
from datetime import datetime

try:
    username = input("username: ")
    password = input("Enter password: ")
    data = {"password": password,
            "type": "normal",
            "username": username,
            }
    url = "https://api.taiga.io/api/v1/"
    header = {"Content-type": "application/json"}
    print(json.dumps(data))
    response = requests.post(url + "auth", data=json.dumps(data), headers=header)
    # print(response.content)
    token = json.loads(response.content)
    print("token", token['auth_token'])

except:
    print("Invalid username or password!\n")
    raise

try:
    slug = input("Enter slug of the project: ")
    params = (
        ('slug', slug),
    )

    response = requests.get(url=url + "projects/by_slug", headers=header, params=params)
    # print(response.content)
    project_data = json.loads(response.content)
    name = project_data['name']
    print("Project name: ", name)
    id = project_data['id']

    print("Team members:\n")

    for member in project_data['members']:
        print("Full Name:", member["full_name_display"])
        print("Role:", member['role_name'])


except:
    print("Invalid slug.")
    raise

try:
    response = requests.get(url + "milestones", headers=header, params={"project": id})
    sprints = json.load(response.content)

    sprint_data = []

    for sprint in sprints:
        sprint_data.append(
            {
                "Name": sprint["name"],
                "Created on": sprint["created_date"],
                "Start Date": sprint["estimated_start"],
                "End Date": sprint["estimated_finish"],
                "Total Points": sprint["total_points"],
                "Closed Points": sprint["closed_points"],
            }
        )

except:
    print("Something went wrong")
    raise

for sprint in sprint_data:
    print("Title: ", sprint["Name"])
    created = datetime.strptime(sprint["Created on"], "%Y-%m-%dT%H:%M:%S.%fZ")
    created = datetime.strftime(created, "%b %d %Y")
    print("Created On", created)
    start = datetime.strptime(sprint["Start Date"], "%Y-%m-%d")
    start = datetime.strftime(start, "%b %d %Y")
    print("\tStart Date\t\t: \t{}".format(start))
    end = datetime.strptime(sprint["End Date"], "%Y-%m-%d")
    end = datetime.strftime(end, "%b %d %Y")
    print("\tEnd Date\t\t: \t{}".format(end))
    print("\tTotal Points\t\t: \t{}".format(sprint["Total Points"]))
    print("\tFinished Points\t\t: \t{}\n".format(sprint["Closed Points"]))
