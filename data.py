import tensor

f = open("sentence/sentence0.txt", "r", encoding="utf-8")

for line in f.readlines():
    print(tensor.toSentence(tensor.toTensor(line)))