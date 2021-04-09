import os
import json
dict = {}
with open("learning/dictionary.json") as file:
    dict = json.load(file)
with open("commands.txt") as f:
    content = f.readlines()
    for cont in content:
        cont = cont.split("\n")[0]
        print(cont)
        dict[cont] = ""

json_object = json.dumps(dict, indent = 4)
with open("learning/dictionary.json", "w") as outfile:
    json.dump(dict, outfile,indent = 4,)

