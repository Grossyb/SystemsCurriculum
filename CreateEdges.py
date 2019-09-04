from difflib import SequenceMatcher
from CanvasData import grab_canvas_data


#data structure initialization
data = {}
grades = {}
gradesList = []
modulesList = []
gradeScores = []
edges = []


def create_edges():
    #read in JSON file
    data, data2 = grab_canvas_data()
    #print(data)
    #print(data2)

    #parse data into formatted dictionary
    for d in data:
        grades[d['assignment']] = {}
        if d['score'] == None:
            d['score'] = 0
        score = 22
        grades[d['assignment']]['grade'] = score
        grades[d['assignment']]['module'] = d['module']

    #parse dictionary into separate lists
    for k, v in grades.items():
        gradesList.append(k)
        gradeScores.append(v['grade'])
        modulesList.append(v['module'])


    '''add edges
    for i in range(len(gradesList)):
        if i + 1 < len(gradesList):
            for j in range(i+1, len(gradesList)):
                if modulesList[i] == modulesList[j]:
                    edges.append((gradesList[i],gradesList[j]))
                elif similar(gradesList[i], gradesList[j]) > 0.5:
                    edges.append((gradesList[i],gradesList[j]))'''

    #add edges
    for d in data:
        for d2 in data2:
            if d['user_id'] == d2:
                if float(d["score"]) / float(d["total"]) * 100 > 90.0:
                    edges.append((d['assignment'], d2))


    return edges
