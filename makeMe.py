import json

parentTarget = ""
previousTarget = ""
childrenNames = []
debug = False
indent = 0
""" figure out how to get the file location that the python script is being run from, oh and alos by chance, include options to specify alternate
    config location """
try:
    with open("./config.json", 'r') as jFile:
        jData = json.load(jFile)
        parentTarget = jData['parentTarget']
        previousTarget = jData['previousTarget']
        for child in jData['childrenNames']:
            childrenNames.append(child)
        debug = jData['debug']
        indent = jData['indent']
    success = True
except IOError as e:
    print(e)
finally:
    if (debug == True) and (success == True):
        print("JSON LOADED")
    else:
        print("JSON LOAD ERROR")
print(parentTarget)
print(previousTarget)
print(childrenNames)
print(debug)
print(indent)