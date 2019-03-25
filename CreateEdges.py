import json
from difflib import SequenceMatcher


#data structure initialization
data = {}
grades = {}
gradesList = []
modulesList = []
gradeScores = []
edges = []
similarEdges = []
colorMap = []


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def create_edges():
    #read in JSON file
    with open('grades.json', 'r') as fp:
        data = json.load(fp)

    #parse data into formatted dictionary
    for d in data:
        grades[d['assignment']] = {}
        score = float(d['score']) / float(d['total']) * 100
        grades[d['assignment']]['grade'] = score
        grades[d['assignment']]['module'] = d['module']

    #parse dictionary into separate lists
    for k, v in grades.items():
        gradesList.append(k)
        gradeScores.append(v['grade'])
        modulesList.append(v['module'])

    #assign colors to each node
    for g in gradeScores:
        if g < 50.00:
            colorMap.append('indianred')
        elif g > 50.00 and g < 70.00:
            colorMap.append('royalblue')
        elif g > 80.00:
            colorMap.append('seagreen')

    #add edges
    for i in range(len(gradesList)):
        if i + 1 < len(gradesList):
            for j in range(i+1, len(gradesList)):
                if modulesList[i] == modulesList[j]:
                    edges.append((gradesList[i],gradesList[j]))
                elif similar(gradesList[i], gradesList[j]) > 0.5:
                    #similarEdges.append((gradesList[i],gradesList[j]))
                    edges.append((gradesList[i],gradesList[j]))

    return edges
