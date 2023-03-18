import json, os, uuid

parentTarget = ""
childrenNames = []
debug = False
indent = 0
parentName = ""

def getPtarget():
    valid_response = False
    cwd = os.path.dirname(os.getcwd())
    print(f'Enter a response in a similar form to > {cwd}\nEnter C to use the current directory path\nEnter ? then press enter to see this prompt again\n')
    while valid_response == False:
        user_response = str(input("Enter directory to create parent folder in: "))
        if user_response == '?':
            print(f'Enter a response in a similar form to > {cwd}\nEnter C to use the current directory path')
        elif user_response == 'c':
            pTarget = cwd
            valid_response = True
            continue
        else:
            if os.path.exists(user_response) == False:
                print("Invlid parent folder location")
                continue
            else:
                pTarget = user_response
                valid_response = True
    return pTarget

def confirmThis(location):
    ask_user = str(input(f'Is the following parent folder path correct? -> {location}\n(Y/N) ')).lower()
    if ask_user == 'y':
        return True
    elif ask_user == 'n':
        return False
    else:
        #returns -1 if the response given was invalid
        return -1

def conManager(confirmMe, debug):
    user_confirmed = confirmThis(confirmMe)
    while user_confirmed == False:
        confirmMe = getPtarget()
        user_confirmed = confirmThis(confirmMe)
        if debug == True:
            print(confirmMe)
    return confirmMe

def getParentName():
    parentName = str(input("Please enter a name for the parent folder Or enter G to generate name > "))
    parentNameCon = False
    while parentNameCon == False:
        if parentName.lower() == 'g':
            parentName = str(uuid.uuid4())
        else:
            user_prompt = str(input(f'Is the parent folder name correct? > {parentName}\n(Y/N) ')).lower()
            if user_prompt == 'n':
                parentName = str(input("Please enter a name for the parent folder > "))
                continue
            else:
                parentNameCon = True
    return parentName

def conSetChildNames(chicken):
    doWeChickenOut = False
    while doWeChickenOut == False:
        user_prompt = str(input(f'Are the child names correct?\n{chicken}\n(Y/N) ')).lower()
        if user_prompt == 'n':
            print("Enter 'Q' when finished adding child folder names")
            rentAchicken = []
            counter = 0
            changeTheChicken = True
            while changeTheChicken == True:
                chicken_name = str(input(f'Enter name for child folder {counter}, or enter "Q" to quit adding folder names > '))
                if chicken_name.lower() == 'q':
                    changeTheChicken = False
                    continue
                else:
                    rentAchicken.append(chicken_name)
                    counter += 1
                    continue
            chicken = rentAchicken.copy()
            continue
        elif user_prompt == 'y':
            return chicken
        else:
            print("Invalid response. Please insert chicken.")
            continue

#get config data
try:
    with open("./config.json", 'r') as jFile:
        jData = json.load(jFile)
        parentTarget = jData['parentTarget']
        for child in jData['childrenNames']:
            childrenNames.append(child)
        debug = jData['debug']
        indent = jData['indent']
except IOError as e:
    print(e)

if parentTarget == "":
    parentTarget = getPtarget()
    parentTarget = conManager(parentTarget, debug)
else:
    parentTarget = conManager(parentTarget, debug)

#get the parent folder name and confirm that the desired name is correct
parentName = getParentName()

#confirm child names are what is desired
childrenNames = conSetChildNames(childrenNames).copy()

#create folders
final_parent_path = str(f'{parentTarget}\{parentName}')
if not os.path.exists(final_parent_path):
    os.makedirs(final_parent_path)
for name in childrenNames:
    childPath = str(f'{final_parent_path}\{name}')
    if not os.path.exists(childPath):
        os.makedirs(childPath)

#create new json dictionary
newJSON = {}
newJSON['parentTarget'] = str(parentTarget)
newJSON['childrenNames'] = childrenNames
newJSON['indent'] = indent
newJSON['debug'] = debug

#check if the values actually changed
same = all((newJSON.get(k) == v for k, v in jData.items()))

#create temp json file
tempfile = os.path.join(os.path.dirname('config.json'), str(uuid.uuid4()))
print(f'\n{tempfile}\n')
#to write or not to write thy json
if same == False:
    with open(tempfile, 'w') as f:
        json.dump(newJSON, f, indent = indent)
    try:
        os.rename(tempfile, 'config.json')
    except WindowsError:
        os.remove('config.json')
        os.rename(tempfile, 'config.json')