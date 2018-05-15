import json
import structure as Q
import structure_alpha as A

file = open('DiStORteD.txt', 'r')
j = file.read()
file2 = open('Shining Crown.txt', 'r')
h = file2.read()

interim = json.loads(j)
interim2 = json.loads(h)

joj = A.Game(interim)
obj = Q.Game(interim2)

try:
    print("window = ", obj.window, '\t\t|\t\t', joj.window)
    print("____________________________________________________________________________________________________")
    for i in range(len(obj.symbol)):
        print("\tnumber : ", i, '\t\t|\t\t', i)
        print("\tname : ", obj.symbol[i].name, '\t\t|\t\t', joj.base.symbol[i].name)
        print("\tpayment : ", obj.symbol[i].payment, '\t\t|\t\t', joj.base.symbol[i].payment)
        print("\tbase")
        print("\t\tbase_direction : ", obj.symbol[i].base.direction, '\t\t|\t\t', joj.base.symbol[i].direction)
        print("\t\tbase_position : ", obj.symbol[i].base.position, '\t\t|\t\t', joj.base.symbol[i].position)
        print("\t\tbase_scatter : ", obj.symbol[i].base.scatter, '\t\t|\t\t', joj.base.symbol[i].scatter)
        if obj.symbol[i].base.wild:
            print("\t\t\tbase_wild_multiplier : ", obj.symbol[i].base.wild.multiplier, '\t\t|\t\t',
                  joj.base.symbol[i].wild.multiplier)
            print("\t\t\tbase_wild_expand : ", obj.symbol[i].base.wild.expand, '\t\t|\t\t',
                  joj.base.symbol[i].wild.expand)
            print("\t\t\tbase_wild_substitute : ", obj.symbol[i].base.wild.substitute, '\t\t|\t\t',
                  joj.base.symbol[i].wild.substitute)
        else:
            print("\t\tbase_wild : ", obj.symbol[i].base.wild, '\t\t|\t\t', joj.base.symbol[i].wild)
        print("\t\tbase_substituted_by : ", obj.symbol[i].base.substituted_by, '\t\t|\t\t',
              joj.base.symbol[i].substituted_by)
        print("\t\tbase_substituted_by_e : ", obj.symbol[i].base.substituted_by_e, '\t\t|\t\t',
              joj.base.symbol[i].substituted_by_e)
        print("\tfree")
        print("\t\tfree_direction : ", obj.symbol[i].free.direction, '\t\t|\t\t', joj.free.symbol[i].direction)
        print("\t\tfree_position : ", obj.symbol[i].free.position, '\t\t|\t\t', joj.free.symbol[i].position)
        print("\t\tfree_scatter : ", obj.symbol[i].free.scatter, '\t\t|\t\t', joj.free.symbol[i].scatter)
        if obj.symbol[i].free.wild:
            print("\t\t\tfree_wild_multiplier : ", obj.symbol[i].free.wild.multiplier, '\t\t|\t\t',
                  joj.free.symbol[i].wild.multiplier)
            print("\t\t\tfree_wild_expand : ", obj.symbol[i].free.wild.expand, '\t\t|\t\t',
                  joj.free.symbol[i].wild.expand)
            print("\t\t\tfree_wild_substitute : ", obj.symbol[i].free.wild.substitute, '\t\t|\t\t',
                  joj.free.symbol[i].wild.substitute)
        else:
            print("\t\tfree_wild : ", obj.symbol[i].free.wild, '\t\t|\t\t', joj.free.symbol[i].wild)
        print("\t\tfree_substituted_by : ", obj.symbol[i].free.substituted_by, '\t\t|\t\t',
              joj.free.symbol[i].substituted_by)
        print("\t\tfree_substituted_by_e : ", obj.symbol[i].free.substituted_by_e, '\t\t|\t\t',
              joj.free.symbol[i].substituted_by_e)
        print("____________________________________________________________________________________________________")

    for i in range(len(obj.line)):
        print("line ", i, " = ", obj.line[i], '\t\t|\t\t', joj.line[i])

    print("free multiplier = ", obj.free_multiplier, '\t\t|\t\t', joj.free_multiplier)
    print("distance = ", obj.distance, '\t\t|\t\t', joj.distance)
    print("RTP = ", obj.RTP, '\t\t|\t\t', joj.RTP)
    print("volatility = ", obj.volatility, '\t\t|\t\t', joj.volatility)
    print("hitrate = ", obj.hitrate, '\t\t|\t\t', joj.hitrate)
    print("baseRTP = ", obj.baseRTP, '\t\t|\t\t', joj.baseRTP)
    print("borders = ", obj.borders, '\t\t|\t\t', joj.borders)
    print("weights = ", obj.weights, '\t\t|\t\t', joj.weights)
    print("list of base wilds = ", obj.base_wildlist, '\t\t|\t\t', joj.base.wildlist)
    print("list of base expanding wilds = ", obj.base_ewildlist, '\t\t|\t\t', joj.base.ewildlist)
    print("list of free wilds = ", obj.free_wildlist, '\t\t|\t\t', joj.free.wildlist)
    print("list of free expanding wilds = ", obj.free_ewildlist, '\t\t|\t\t', joj.free.ewildlist)
    print("list of base scatters = ", obj.base_scatterlist, '\t\t|\t\t', joj.base.scatterlist)
    print("list of free scatters = ", obj.free_scatterlist, '\t\t|\t\t', joj.free.scatterlist)

except Exception as inst:
    print(inst)
