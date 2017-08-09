import json

cameoFile = open("Cameo_es_v0.0.1.txt","r")

cameoMap = {}

for line in cameoFile:
    cameoCode = line[line.index('[')+1: line.index(']')]
    print cameoCode
    words = line[line.index("#")+1:].split(",")

    if cameoCode not in cameoMap:
        cameoMap[cameoCode]= {"words": set(), "rules": set()}

    wordset = cameoMap[cameoCode]["words"]

    for word in words:
        if word.startswith("NTA"):
            continue
        wordset.add(word.strip())

    cameoMap[cameoCode]["rules"].add(line)

output_file = open("Cameo_es_v0.0.2.txt", "w+")

cameoConceptMap = {x["code"]:x ["concept"] for x in json.load(open("CameoEntry.json","r"))}

for cameoCode in cameoMap:
    if cameoCode not in cameoConceptMap:
        print "Concept not found : ", cameoCode
        continue
    concept = cameoConceptMap[cameoCode].upper().replace(" ","_")

    output_file.write("--- "+concept+" ["+cameoCode+"] ---\n")
    for word in cameoMap[cameoCode]["words"]:
        output_file.write(word.upper()+"\n")
    for rule in cameoMap[cameoCode]["rules"]:
        print type(rule)
        part1 = rule[:rule.index('[')]
        part2 = rule[rule.index('['):rule.index("#")]
        part3 = rule[rule.index('#'):]

        str = "%-50s %-10s %s" % (part1.upper(), part2, part3.upper())
        print str
        output_file.write(str)
    output_file.write("\n\n")

output_file.flush()
output_file.close()






