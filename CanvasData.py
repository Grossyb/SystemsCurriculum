import json
import requests
import html2text

#7~AK0UAwLvvCAf33guCF1VyQs7S88xcVxtfHEwmBKllHETEAYMHs8YSkaKnjb8EUOB
url = "https://canvas.instructure.com/api/v1/courses/72360000000012397/assignments"
#users/72360000000048494/
headers = {"Authorization": "Bearer " + "7236~vh5XQQveDqwkvzPvhzsK9IivIdSmUDKY3FarvXAiY0xUpeCGhFmXkjKzMu67yYcc"}
response = requests.get(url, headers = headers)

data = json.loads(response.text)

url2 = "https://canvas.instructure.com/api/v1/courses/72360000000012397/assignments"
#users/72360000000048494/
headers = {"Authorization": "Bearer " + "7236~vh5XQQveDqwkvzPvhzsK9IivIdSmUDKY3FarvXAiY0xUpeCGhFmXkjKzMu67yYcc"}
response2 = requests.get(url2, headers = headers)

data2 = json.loads(response2.text)

print(data2)

modules = {}

descriptions = {}

for d in data:
    text = html2text.html2text(d['description']).encode('utf-8').lower()
    text = text.replace('\n', '')
    text = text.replace('(', '')
    text = text.replace(')', '')
    text = text.replace(':', '')
    text =text.replace('.', '')
    text = text.replace('*', '')
    text = text.replace('\xe2\x80\x99ve', '')
    text = text.replace('\xc2\xa0', '')
    descriptions[d['id']] = text


stopwords = ['', 'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some',
             'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are',
             'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she',
             'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did',
             'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a',
             'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than' ]

for v in descriptions.values():
    print(v)
    xx = v.split(' ')
    z = {}
    for x in xx:
        if x not in stopwords:
            if x in z:
                z[x] += 1
            elif x not in z:
                z[x] = 1
    for k, v in z.items():
        if v >= 1:
            print(k)
    print('------------\n')
