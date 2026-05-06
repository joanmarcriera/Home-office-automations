import json

with open('data/all_tools.json', 'r') as f:
    data = json.load(f)

tools = data['tools']
unique_tools = {}
for tool in tools:
    unique_tools[tool['id']] = tool

sorted_tools = sorted(unique_tools.values(), key=lambda x: x['id'])
data['tools'] = sorted_tools

with open('data/all_tools.json', 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')
