import json
from io import open

language = "es"

synsetCameoToSubmission = json.load(open("SynsetCameoToSubmission.json","r"))

#print type(synsetCameoToSubmission)

# for key in synsetCameoToSubmission:
#     print type(synsetCameoToSubmission[key])


wordFeedbacks = json.load(open("FeedbackOnSynsetWord.json", "r"))

synsetWords = json.load(open("SynsetWord.json", encoding='UTF-8'),  "r")

synsetWords = [x for x in synsetWords if x["languageCode"] == "es"]

idToSynsetWordMap = {x["id"]: x for x in synsetWords}

count = 0

print len(wordFeedbacks)

filteredWordFeedbacks = []

for entry in wordFeedbacks:

    if entry['idWord'] in idToSynsetWordMap:
        entry["synset_id"] = idToSynsetWordMap[entry['idWord']]['idSynsetEntry']
        filteredWordFeedbacks.append(entry)
    else:
        count += 1


print len(filteredWordFeedbacks)



submissionToWordfeedbacks = {}

for entry in filteredWordFeedbacks:
    if entry['submissionId'] not in submissionToWordfeedbacks:
        submissionToWordfeedbacks[entry['submissionId']] = list()
    submissionToWordfeedbacks[entry['submissionId']].append(entry)


word_stat = {}

for synsetId in synsetCameoToSubmission:
    for cameoId in synsetCameoToSubmission[synsetId]:
        if cameoId not in word_stat:
            word_stat[cameoId]={}
        for submissionId in synsetCameoToSubmission[synsetId][cameoId]:
            if submissionId not in submissionToWordfeedbacks:
                continue

            for feedback in submissionToWordfeedbacks[submissionId]:
                if feedback['idWord'] not in word_stat[cameoId]:
                    word_stat[cameoId][feedback['idWord']] = {"correct": 0, "incorrect": 0, "ambiguous": 0}
                if feedback['verdict'] == "c":
                    word_stat[cameoId][feedback['idWord']]["correct"] += 1
                elif feedback['verdict'] == "ic":
                    word_stat[cameoId][feedback['idWord']]["incorrect"] += 1
                else:
                    word_stat[cameoId][feedback['idWord']]["ambiguous"] += 1

#print word_stat

synsetEntryList = json.load(open("SynsetEntry.json","r"))

synsetEntryToWordMap = {x["id"]: x["idWord"] for x in synsetEntryList}

wordList = json.load(open("Word.json", "r"))

#print wordList

print wordList[0]['text']
wordIdToText ={}
for i in range(0, len(wordList)):
#    print wordList[i]
    if 'text' in wordList[i]:
        wordIdToText[wordList[i]["id"]] = wordList[i]['text']
    else:
        print "ISSUE " +str(wordList[i])


cameo_word_translated = {}

for cameoId in word_stat:
    if cameoId not in cameo_word_translated:
        cameo_word_translated[cameoId] = {}
    for synsetWordId in word_stat[cameoId]:
        synsetWord = idToSynsetWordMap[synsetWordId]

        if word_stat[cameoId][synsetWordId]["correct"] >= word_stat[cameoId][synsetWordId]["incorrect"] + word_stat[cameoId][synsetWordId]["ambiguous"]:
            wordId = synsetEntryToWordMap[synsetWord["idSynsetEntry"]]
            wordEN = wordIdToText[wordId]
            if wordEN not in cameo_word_translated[cameoId]:
                cameo_word_translated[cameoId][wordEN] = set()
            cameo_word_translated[cameoId][wordEN].add(synsetWord['word'])

#print cameo_word_translated

cameoEntryList = json.load(open("CameoEntry.json", "r"))

codeToCameoId = {x['code']: x['id'] for x in cameoEntryList}

cameoRulesList = json.load(open("CameoRule.json","r", encoding='UTF-8'))
count = 0

listCameoIDs = []
for key in codeToCameoId:
     listCameoIDs.append(codeToCameoId[key])

#print sorted(listCameoIDs)
listCameoIDs = []
for key in cameo_word_translated:
    listCameoIDs.append(key)
#print sorted(listCameoIDs)

outputFile = open("Cameo_es_v0.0.1.txt", "w+", encoding="UTF-8")
for x in cameoRulesList:
    if x["source"] != "CAMEO2":
        cameoId = str(codeToCameoId[x['cameoCode']])
        if cameoId in cameo_word_translated:
            translatedWords = cameo_word_translated[cameoId]
            if x['word'] in translatedWords:
                outputFile.write('- ' +x['ruleText']+'['+x['cameoCode']+'] #'+ ', '.join(translatedWords[x["word"]])+'\n')
            else:
                outputFile.write('- ' + x['ruleText'] + '[' + x['cameoCode'] + '] #' + "NTA "+x['word']+"\n")
            count += 1
print count

outputFile.close()
























