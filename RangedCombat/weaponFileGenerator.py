import json
from collections import OrderedDict

print("Name of file")
fileName = eval(input( ">" )) 
with open( "\\Weapons\\"+fileName + ".json" ,'w' ) as fp:
    jsonDict = OrderedDict()

    print("\nEnter TL")
    jsonDict['TL'] = eval(input('>'))

    print("\nEnter Gun Name")
    jsonDict['Name'] = eval(input('>'))

    print("\n**Damage subsection**")
    jsonDict['Damage'] = OrderedDict()

    print("\nEnter base Damage")
    jsonDict['Damage']['Base'] = eval(input('>'))

    print("\nEnter armor divisor")
    jsonDict['Damage']['Divisor'] = eval(input('>'))

    print("\nEnter damage type")
    jsonDict['Damage']['Type'] = eval(input('>'))

    print("\nEnter Acc")
    jsonDict['Acc'] = eval(input('>'))

    print("\n**Range subsection**")
    jsonDict['Range'] = OrderedDict()

    print("\nEnter minimum range")
    jsonDict['Range']['Min'] = eval(input('>'))

    print("\nEnter maximum range")
    jsonDict['Range']['Max'] = eval(input('>'))

    print("\n**Weight subsection**")
    jsonDict['Weight'] = OrderedDict()

    print("\nEnter base weight")
    jsonDict['Weight']['Base'] = eval(input('>'))

    print("\nEnter maximum range")
    jsonDict['Weight']['Misc'] = eval(input('>'))

    print("\nEnter rate of fire")
    jsonDict['RoF'] = eval(input('>'))

    print("\n**Shots subsection**")
    jsonDict['Shots'] = OrderedDict()

    print("\nEnter base shots")
    jsonDict['Shots']['Base'] = eval(input('>'))

    print("\nEnter reload number")
    jsonDict['Shots']['Reload'] = eval(input('>'))

    print("\nEnter ST")
    jsonDict['ST'] = eval(input('>'))

    print("\nEnter Bulk")
    jsonDict['Bulk'] = eval(input('>'))

    print("\nEnter Recoil")
    jsonDict['Rcl'] = eval(input('>'))

    print("\nEnter Cost")
    jsonDict['Cost'] = eval(input('>'))

    print("\nEnter LC")
    jsonDict['LC'] = eval(input('>'))

    print("\nEnter Notes")
    jsonDict['Notes'] = eval(input('>'))






    json.dump( jsonDict, fp, indent=3 )

