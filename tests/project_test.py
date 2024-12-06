import json


filepath = "/home/barak/Desktop/web2pdf-etl_output's/logs/"

for file in filepath:
    with open(file,'r') as f:
        data = json.load(f)
        print(data)