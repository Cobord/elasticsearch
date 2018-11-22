import requests
import random
import hashlib
import json

url="http://parisx:9200/universities/doc/" 

def assignClasses():
    classes=[]
    for x in range(random.randrange(1,6)):
      classes.append(genclass())
    return classes 
      
schools = ("Arizona State University", "University of South Carolina - Columbia", "University of North Carolina at Chapel Hill") 
firstNames = ("Walker", "Stephen", "Julie", "George")
lastNames = ("Rowe", "Shakespeare", "Mann", "Sarte")
courses= ("math", "physics", "French", "logic")

def genclass():
    classes={}
    classes["name"]=courses[random.randrange(0,3)]
    classes["grades"] = random.randrange(1,7)
    return classes

def genParent(id):
    child={}
    child['name'] = 'students'
    child['parent'] = id
    return child

def genSchool():
    school={}
    school["universities_students"] = {'name': 'universities'}
    school["school"]=schools[random.randrange(0,3)]
    m = hashlib.sha1()
    m.update(bytes(json.dumps(school), 'utf-8'))
    id = m.hexdigest()
    print(school)
    response = requests.post(url + id, json=school)
    print (response.json())
    return id

def genStudent():
    id = genSchool()
    students={}
    students["universities_students"] = genParent(id)
    students["school"]=schools[random.randrange(0,3)]
    students["firstName"] = firstNames[random.randrange(0,3)]
    students["lastName"] = lastNames[random.randrange(0,3)]
    students["classes"] = assignClasses()
    m = hashlib.sha1()
    m.update(bytes(json.dumps(students), 'utf-8'))
    sid = m.hexdigest()

    print(students)
    response = requests.post(url + sid + "?routing=1&refresh", json=students)
    print (response.json())

for r in range(1,2):
    genStudent()

