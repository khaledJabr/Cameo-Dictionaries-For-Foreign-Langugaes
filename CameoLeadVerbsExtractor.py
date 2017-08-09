import re
import json
from pprint import pprint


def get_verb_and_code(line):
    matcher = regex.search(line)
    if matcher != None:
        verb = matcher.group(0).strip().split(" ")[0]

        code = matcher.group(1)
        if code != None:
            code = code.replace("[", "").replace("]", "")

        return verb.strip(), code
    return None, None




cameo_file = open("CAMEO.2.0.txt","r")
verbs_map = {}
current_lead_verb = ""
regex = re.compile("[a-zA-Z ]+(\[[-|[0-9]*\])?")
for line in cameo_file:
    if line.strip() == "":
        continue

    if line.strip().startswith("---"):
        verb, code = get_verb_and_code(line)
        current_lead_verb = verb
        verbs_map[current_lead_verb]={"code": code, "related_verbs": {}}


    elif line.startswith("-") and current_lead_verb != "":

        current_lead_verb  = ""
    elif current_lead_verb != "":
        verb, code = get_verb_and_code(line)
        if verb != None:
            verbs_map[current_lead_verb]["related_verbs"][verb] = {'code': code}
        else:
            print "NOT Inserting"



print len(verbs_map)

verbs_db = [x for x in json.load(open("Word.json","r"))]

print len(verbs_db)

v_map = {}

for v in verbs_db:
    if 'text' in v:
        v_map[v['text']] = v['id']

print v_map['develop']
count = 0;
for verb in verbs_map:
    if verb.lower() in v_map:
        verbs_map[verb]["id"] = v_map[verb.lower()]
    else:
        print verb
        count += 1
    for rverb in verbs_map[verb]['related_verbs']:

        if rverb.lower() in v_map:
            #print rverb
            #print verbs_map[verb]['related_verbs'][rverb]
            verbs_map[verb]['related_verbs'][rverb]["id"] = v_map[rverb.lower()]
        else:
            print "+", rverb
            count += 1
print count
pprint(verbs_map)

























