"""
------------------------------------------------------------------------------
This file connects users with their assignment information and store them in
the lists edges. Edges only contains tuples in the format of
(assignment name,userid,score,user name). Run this file to generate edges.json and edges2.json to see
more details.
------------------------------------------------------------------------------
"""



from difflib import SequenceMatcher
from CanvasData import grab_canvas_data
import os.path
from os import path
import json

#data structure initialization
data = {}
grades = {}
gradesList = []
modulesList = []
gradeScores = []
edges = []

def create_edges(repull):
    edges = []

    # if (repull == False) and (path.exists("edges.json") == True):
    #     with open('edges.json') as json_file:
    #         edges = json.load(json_file)
    #     return edges


    # read in JSON file
    data, data2 = grab_canvas_data()
    # print(data)
    # print(data2)

    # # parse data into formatted dictionary
    # for d in data:
    #     grades[d['assignment']] = {}
    #     if d['score'] == None:
    #         d['score'] = 0
    #     score = 22 # what is this?
    #     grades[d['assignment']]['grade'] = score
    #     grades[d['assignment']]['module'] = d['module']
    #
    # #parse dictionary into separate lists
    # for k, v in grades.items():
    #     gradesList.append(k)
    #     gradeScores.append(v['grade'])
    #     modulesList.append(v['module'])

    # add edges
    for d in data:
        for d2 in data2:
            if d['user_id'] == d2:
                score_calc = float(d["score"]) / float(d["total"]) * 100
                edges.append((d['assignment'], d2, score_calc, d["user_name"]))

                # user_name

    f = open("edges.json", "w")
    f.write(json.dumps(edges))
    f.close()

    # print(edges)
    return edges
