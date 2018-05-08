import json
import structure as Q

file = open('input.txt', 'r')
j = file.read()

interim = json.loads(j)

obj = Q.Game(interim)

print(obj.symbol[8].base.wild.substitute)
print(obj.symbol[7].base.substituted_by)
print(obj.symbol[9].base.substituted_by)
