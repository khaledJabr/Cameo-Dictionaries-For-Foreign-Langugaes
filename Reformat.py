import re
dict_file = open("CAMEO.es.0.0.5.txt","r")

out_file = open("CAMEO.es.0.0.6.txt", "w+")


default_code_map = {}

for line in dict_file:
    if line.startswith("#") or len(line.strip()) == 0:
        out_file.write(line+"")
        continue
    if line.startswith("---"):
        line = line.replace("-"," ").strip()
        try:
            start = line.index("[") + 1
            code = line[start: line.index("]")]
            verb = line[:start-1].strip()

            if verb in default_code_map:
                code2 = default_code_map[verb]
                if code2 != code:
                    code = code2
            else:
                default_code_map[verb] = code
            out_file.write("--- " + verb + " [" + code + "] ---\n")
            print "--- " + verb + " [" + code + "] ---"

        except:
            out_file.write("--- "+line+" ---\n")

            print "--- "+line+" ---\n"


    elif line.startswith("+"):
        out_file.write(line+"")
        print line
        continue

    elif line.startswith("-"):
        out_file.write(line+"")
        verbs = line[line.index("#")+1:].strip().split(",")
        code = line[line.index("[")+1:line.index("]")]
        for verb in verbs:
            if verb in default_code_map:
                continue
            else:
                default_code_map[verb] = code
        print line

    else:
        words = re.split(" +", line)
        if len(words) != 4:
            out_file.write(line + "")
            verb = words[0].strip()
            if verb in default_code_map:
                line = line.replace(verb, verb+"  ["+default_code_map[verb]+"]")
            print line
            continue

        code = words[1].replace("[","").replace("]","")
        verb = words[0]
        if verb in default_code_map:
            code2 = default_code_map[verb]
            if code2 != code:
                line = line.replace(code, code2)
                code = code2
        else:
            default_code_map[verb] = code
        out_file.write(line + "")
        print line



out_file.close()
dict_file.close()
