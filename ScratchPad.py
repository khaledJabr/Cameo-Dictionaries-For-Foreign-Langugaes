##encoding= utf-8

arabic_part = "عمل_Test ]عة"
full_sent = arabic_part + " TEST [010]"
print full_sent
words = full_sent.split(" ")
print words[0].decode('utf-8'), words[1].decode('utf-8')
print [x.decode("utf-8") for x in words]
# print arabic_part, "[010] " + "Test"
# print "m"+ arabic_part+ "[010] Test"+ arabic_part#, , arabic_part