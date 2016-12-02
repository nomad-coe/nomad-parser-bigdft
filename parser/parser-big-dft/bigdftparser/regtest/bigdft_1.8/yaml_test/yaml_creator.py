import yaml

data = {}
listy = []
data["list"] = [1000000000000+x for x in range(2000000)]

with open('data.yml', 'w') as outfile:
    yaml.dump(data, outfile, default_flow_style=True)
