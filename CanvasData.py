import json
import requests
import html2text
import json

def grab_canvas_data():

    assignURL = "https://asu.instructure.com/api/v1/courses/18732/assignments?per_page=100"

    headers = {"Authorization": "Bearer " + "7236~vh5XQQveDqwkvzPvhzsK9IivIdSmUDKY3FarvXAiY0xUpeCGhFmXkjKzMu67yYcc"}
    assignResponse = requests.get(assignURL, headers = headers)
    data = json.loads(assignResponse.text)

    # pagination
    while True:
    	if 'next' in assignResponse.links:
    		# print(assignResponse.links['next']['url'])
    		assignURL = assignResponse.links['next']['url']

    		assignResponse = requests.get(assignURL, headers = headers)
    		data = data + json.loads(assignResponse.text)
    	else:
    		break

    f = open("assignments.json", "w")
    f.write(json.dumps(data))
    f.close()

    #for grades only
    gradesURL = "https://asu.instructure.com/api/v1/courses/18732/gradebook_history/feed?per_page=100"
    gradesResponse = requests.get(gradesURL, headers = headers)
    data2 = json.loads(gradesResponse.text)

    f = open("grades.json", "w")
    f.write(json.dumps(data2))
    f.close()

    while True:
    	if 'next' in gradesResponse.links:
    		# print(gradesResponse.links['next']['url'])
    		gradesURL = gradesResponse.links['next']['url']

    		gradesResponse = requests.get(gradesURL, headers = headers)
    		data2 = data2 + json.loads(gradesResponse.text)
    	else:
    		break

    assignments = []
    users = []

    for dictionary in data:
        for dictionary2 in data2:
            ## assignment, score, total, module
            newEntry = {}
            newEntry["user_id"] = None
            newEntry["score"] = None
            newEntry["total"] = 0

            if dictionary["name"]:
                newEntry["assignment"] = dictionary["name"]

            if dictionary["id"]:
                newEntry["assignment_id"] = dictionary["id"]
                if dictionary2["assignment_id"] == dictionary["id"]:
                    newEntry["score"] = dictionary2["current_grade"]

                    if dictionary2["user_id"]:
                        if dictionary2["user_id"] not in users:
                            users.append(dictionary2["user_id"])
                        newEntry["user_id"] = dictionary2["user_id"]

            if dictionary["points_possible"]:
                newEntry['total'] = dictionary["points_possible"]

            if dictionary["position"]:
                newEntry["module"] = dictionary["position"]

            if newEntry["total"] != 0 and newEntry["score"] != None and newEntry["user_id"] != None:
                assignments.append(newEntry)

    return (assignments, users)
