import json 
  
f = open('actions.json',) 
  
data = json.load(f) 

local_actions = [
    {
        "name": "",
        "url": "",
        "method": "",
        "response": ""
    }
]