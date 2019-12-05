"""
---------------------------------------------------------------------------------
This file extracts relevant information 'userid,username,score,total,assignment,
assignmentid,module' of each assignment and store them in the dictionary
'Assignments' and the list 'users'. Run this file to generate a text file of
raw input 'received.txt', and two simplified text files 'modAssignment.txt'
and 'modUsers.txt' to get a better understanding of the data structure.
---------------------------------------------------------------------------------
Contact anyone of us if you need furthur explanation:
Hao Yang hyang46@asu.edu
Chun Yang cyang114@asu.edu
Logan Cousins lcousins@asu.edu
Brandon Grossnickle bgrossni@asu.edu
--------------------------------------------------------------------------------
"""

import json
import requests
import html2text
import json

def grab_canvas_data():
    # curl standard format
    # curl -H "Authorization: Bearer <ACCESS-TOKEN>" "https://canvas.instructure.com/api/v1/courses"

<<<<<<< HEAD
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
=======
    # course url
    url = "https://asu.instructure.com/api/v1/courses/18732/assignments?per_page=200"
    headers = {"Authorization": "Bearer " + "7236~vh5XQQveDqwkvzPvhzsK9IivIdSmUDKY3FarvXAiY0xUpeCGhFmXkjKzMu67yYcc"}
    response = requests.get(url, headers = headers)
    # dictionary
    data = json.loads(response.text)

    # for grades only
    url2 = "https://asu.instructure.com/api/v1/courses/18732/gradebook_history/feed?per_page=200"
    response2 = requests.get(url2, headers = headers)
    data2 = json.loads(response2.text)
>>>>>>> edges_update

    # original raw data stored locally for inspection
    receivedText = open("received.txt","w")
    receivedText.write(response2.text)
    receivedText.close()


    assignments = []
    users = []

    for dictionary in data:
        for dictionary2 in data2:
            ## assignment, assignment id, score, total, module
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
                        newEntry["user_name"] = dictionary2["user_name"]

            if dictionary["points_possible"]:
                newEntry['total'] = dictionary["points_possible"]

            if dictionary["position"]:
                newEntry["module"] = dictionary["position"]

            if newEntry["total"] != 0 and newEntry["score"] != None and newEntry["user_id"] != None:
                assignments.append(newEntry)

    # stored locally for inspection and improvement
    # one dictionary output format {"user_id": 4249, "score": "250", "total": 250.0,
    # "assignment": "Systems Analysis Paper", "assignment_id": 372387, "module": 1}
    with open('modAssignment.txt','w') as filehandle:
        json.dump(assignments,filehandle)

    # all students' user id [4249, 266746, 333854]
    with open('modUsers.txt','w') as filehandle:
        json.dump(users,filehandle)

    return (assignments, users)




grab_canvas_data()
