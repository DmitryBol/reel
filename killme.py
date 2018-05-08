import json
import sys
sys.path.insert(0, 'Front-end/')
import structure as Q
print("pomiluy gospodi")

j = """{"kill": "me"}"""

sas = json.loads(j)
print("kill" in sas)
lala = Q.Game(sas)

if ("kill" in sas):
    print(sas["kill"])