import json
import structure_alpha as Q

file = open('DiStORteD.txt', 'r')
j = file.read()

interim = json.loads(j)

obj = Q.Game(interim)

print("window = ", obj.window)
print("____________________________________________________________________________________________________")
for i in range(len(obj.base.symbol)):
    print("\tnumber : ", i)
    print("\tname : ", obj.base.symbol[i].name)
    print("\tpayment : ", obj.base.symbol[i].payment)
    print("\tbase")
    print("\t\tbase_direction : ", obj.base.symbol[i].direction)
    print("\t\tbase_position : ", obj.base.symbol[i].position)
    print("\t\tbase_scatter : ", obj.base.symbol[i].scatter)
    if obj.base.symbol[i].wild:
        print("\t\t\tbase_wild_multiplier : ", obj.base.symbol[i].wild.multiplier)
        print("\t\t\tbase_wild_expand : ", obj.base.symbol[i].wild.expand)
        print("\t\t\tbase_wild_substitute : ", obj.base.symbol[i].wild.substitute)
    else:
        print("\t\tbase_wild : ", obj.base.symbol[i].wild)
    print("\t\tbase_substituted_by : ", obj.base.symbol[i].substituted_by)
    print("\t\tbase_substituted_by_e : ", obj.base.symbol[i].substituted_by_e)
    print("\tfree")
    print("\t\tfree_direction : ", obj.free.symbol[i].direction)
    print("\t\tfree_position : ", obj.free.symbol[i].position)
    print("\t\tfree_scatter : ", obj.free.symbol[i].scatter)
    if obj.free.symbol[i].wild:
        print("\t\t\tfree_wild_multiplier : ", obj.free.symbol[i].wild.multiplier)
        print("\t\t\tfree_wild_expand : ", obj.free.symbol[i].wild.expand)
        print("\t\t\tfree_wild_substitute : ", obj.free.symbol[i].wild.substitute)
    else:
        print("\t\tfree_wild : ", obj.free.symbol[i].wild)
    print("\t\tfree_substituted_by : ", obj.free.symbol[i].substituted_by)
    print("\t\tfree_substituted_by_e : ", obj.free.symbol[i].substituted_by_e)
    print("____________________________________________________________________________________________________")

for i in range(len(obj.line)):
    print("line ", i, " = ", obj.line[i])

print("free multiplier = ", obj.free_multiplier)
print("distance = ", obj.distance)
print("RTP = ", obj.RTP)
print("volatility = ", obj.volatility)
print("hitrate = ", obj.hitrate)
print("baseRTP = ", obj.baseRTP)
print("borders = ", obj.borders)
print("weights = ", obj.weights)
print("list of base wilds = ", obj.base.wildlist)
print("list of base expanding wilds = ", obj.base.ewildlist)
print("list of base scatters = ", obj.base.scatterlist)
print("list of free wilds = ", obj.free.wildlist)
print("list of free expanding wilds = ", obj.free.ewildlist)
print("list of free scatters = ", obj.free.scatterlist)

