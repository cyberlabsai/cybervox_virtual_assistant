import json 

file = open('actions.json', 'r')
local_actions = json.load(file)
local_actions = local_actions['data']