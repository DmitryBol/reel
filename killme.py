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

if "substitute" in interim["symbol"][i]["base"]["wild"]:
     for j in range(len(interim["symbol"][i]["base"]["wild"]["substitute"])):
        for k in range(len(interim["symbol"])):
            if interim["symbol"][i]["base"]["wild"]["substitute"][j] == interim["symbol"][k]["name"]:
                self.symbol[i].base.wild.substitute.append(k)
else:
    for j in range(len(self.symbol)):
        if not self.symbol[j].base.scatter:
            self.symbol[i].base.wild.substitute.append(j)

def transsubst (arr, type, interim, vav):
    if "substitute" in interim["symbol"][i][type]["wild"]:
        for j in range(len(interim["symbol"][i][type]["wild"]["substitute"])):
            for k in range(len(interim["symbol"])):
                if interim["symbol"][i][type]["wild"]["substitute"][j] == interim["symbol"][k]["name"]:
                    arr.append(k)
    else:
        for j in range(len(self.symbol)):
            if not vav[j].base.scatter:
                arr.append(j)