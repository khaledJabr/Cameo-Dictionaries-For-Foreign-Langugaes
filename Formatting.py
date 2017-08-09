
import io

synset_file = io.open("Synsets.txt","r", encoding="UTF-8")
synset_file_out = io.open("synsets_es.txt","w+", encoding="UTF-8")

for line in synset_file:
    if len(line.strip()) == 0:
        synset_file_out.write(line)
    elif line.startswith("&"):
        synset_file_out.write(line)
    elif line.startswith("+"):
        synset_file_out.write(line)
    else:
        synset_file_out.write("+"+line)

synset_file_out.close()
synset_file.close()
