import json
print("pomiluy gospodi")

j = """{"kill": "me"}"""

sas = json.loads(j)

if ("kill" in sas):
    print(sas["kill"])