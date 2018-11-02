import getpass
import requests
import json
from datetime import datetime

try:
    input("Press any key to start...")
    username = "kjha7@asu.edu"
    password = "kirtijha1234"
    data = {"password": password,
            "type": "normal",
            "username": username,
            }
    url = "https://api.taiga.io/api/v1/"
    header = {"Content-type": "application/json"}
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
    sprints = json.loads(response.content)

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

    for sprint in sprint_data:
        print("\nTitle: ", sprint["Name"])
        print("created on: ", sprint["Created on"])
        print("start date: ", sprint["Start Date"])
        print("End date: ", sprint["End Date"])
        print("Total Points: ", sprint["Total Points"])
        print("Finished Points: ", sprint["Closed Points"])

except:
    print("Something went wrong")
    raise

while True:
    try:
        sprint_number = int(input("Select Sprint # : "))
        if sprint_number >= 1 and sprint_number <= len(sprint_data):
            break
        else:
            print("That's not a valid option!")
    except:
        print("That's not a valid option!")

try:
    sprint_number = len(sprint_data) - sprint_number

    sprint_id = sprints[sprint_number]
    id_s = sprint_id["id"]
    response = requests.get(url + "userstories", headers=header, params={"milestone": id_s})
    user_story = json.loads(response.content)

    print("\nUser Story name: ", sprint_id["name"])

    for story_data in user_story:
        status = story_data["status_extra_info"]
        if not status:
            finish = False
        else:
            finish = status["is_closed"]
        print("\nStory: ", story_data["subject"])
        print("Finished: ", finish)
        print("Created on: ", story_data["created_date"])

        id_ = str(story_data["id"])
        response = requests.get(url + "history/userstory/" + id_, headers=header)
        history = json.loads(response.content)
        for story in history:
            history = story["diff"]
            if "milestone" in history.keys():
                print("Moved to Sprint on: ", story["created_at"])

    response = requests.get(url + "tasks", headers=header, params={"milestone": id_s})
    tasks = json.loads(response.content)
    print("\nTasks of ", sprint_id["name"])

    name = {}
    count = {}

    for task_data in tasks:
        assigned_to = task_data["assigned_to_extra_info"]
        print("Task: ", task_data["subject"])
        if task_data["assigned_to"]:
            print("Assigned to: ",assigned_to["full_name_display"])
            count[task_data["assigned_to"]] = 0
            name[task_data["assigned_to"]] = assigned_to["full_name_display"]
            print()
        else:
            print("Assigned to: None\n")

    for task in tasks:
        if task["assigned_to"] in count.keys():
            count[task["assigned_to"]] += 1

    name = list(name.items())
    count = list(count.items())

    name = list(map(list, zip(*name)))[1]
    count = list(map(list, zip(*count)))[1]

    print(
        "\nNumber of tasks assigned to each team member in {} are:\n".format(
            sprint_id["name"]
        )
    )

    for i, j in zip(name, count):
        print(i, " : \t", j)

    input("\nPress Enter to EXIT.")

except:
    print("Something went wrong. Try again.")
    raise

