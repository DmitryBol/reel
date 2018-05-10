import json
import structure as Q

file = open('input.txt', 'r')
j = file.read()

interim = json.loads(j)

obj = Q.Game(interim)

print("window = ", obj.window)
print("_____________________________________________________________")
for i in range(len(obj.symbol)):
    print("\tname : ", obj.symbol[i].name)
    print("\tpayment : ", obj.symbol[i].payment)
    print("\tbase")
    print("\t\tbase_direction : ", obj.symbol[i].base.direction)
    print("\t\tbase_position : ", obj.symbol[i].base.position)
    print("\t\tbase_scatter : ", obj.symbol[i].base.scatter)
    if (obj.symbol[i].base.wild):
        print("\t\t\tbase_wild_multiplier : ", obj.symbol[i].base.wild.multiplier)
        print("\t\t\tbase_wild_expand : ", obj.symbol[i].base.wild.expand)
        print("\t\t\tbase_wild_substitute : ", obj.symbol[i].base.wild.substitute)
    print("\t\tbase_substituted_by : ", obj.symbol[i].base.substituted_by)
    print("\t\tbase_substituted_by_e : ", obj.symbol[i].base.substituted_by_e)
    print("\tfree")
    print("\t\tfree_direction : ", obj.symbol[i].free.direction)
    print("\t\tfree_position : ", obj.symbol[i].free.position)
    print("\t\tfree_scatter : ", obj.symbol[i].free.scatter)
    if (obj.symbol[i].free.wild):
        print("\t\t\tfree_wild_multiplier : ", obj.symbol[i].free.wild.multiplier)
        print("\t\t\tfree_wild_expand : ", obj.symbol[i].free.wild.expand)
        print("\t\t\tfree_wild_substitute : ", obj.symbol[i].free.wild.substitute)
    print("\t\tfree_substituted_by : ", obj.symbol[i].free.substituted_by)
    print("\t\tfree_substituted_by_e : ", obj.symbol[i].free.substituted_by_e)
    print("_____________________________________________________________")

for i in range(len(obj.lines)):
    print("line ", i, " = ", obj.lines[i])

print("free_multiplier = ", obj.free_multiplier)
print("distance = ", obj.distance)
print("RTP = ", obj.RTP)
print("volatility = ", obj.volatility)
print("hitrate = ", obj.hitrate)
print("baseRTP = ", obj.baseRTP)
print("borders = ", obj.borders)
print("weights = ", obj.weights)
print("set of base wilds = ", obj.set_of_base_wilds)
print("set of base ewilds = ", obj.set_of_base_ewilds)
print("set of free wilds = ", obj.set_of_free_wilds)
print("set of free ewilds = ", obj.set_of_free_ewilds)
print("vsmisle")
print("cecedsfscvcvc")