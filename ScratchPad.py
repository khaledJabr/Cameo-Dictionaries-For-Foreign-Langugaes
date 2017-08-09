from io import open
import json

cameoRulesList = json.load(open("CameoRule.json","r", encoding='UTF-8'))
count = 0
for x in cameoRulesList:
    if x["source"] != "CAMEO2":
        print x["ruleText"]
        count += 1

print count

testFileList = json.load(open("Word.json","r", encoding='UTF-8'))

for key in testFileList[0]:
    print key

