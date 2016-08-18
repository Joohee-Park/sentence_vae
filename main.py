import sys
import naver

def main(argv):
    if len(argv) != 2 :
        print("You must specify start docId and end docId")
        return

    startDocId = argv[0] if argv[0] < argv[1] else argv[1]
    endDocId = argv[1] if argv[0] < argv[1] else argv[0]

    docId = startDocId
    fileNumber = str(int(int(docId)/100000))
    f1 = open("sentence/sentence"+fileNumber+".txt", "w", encoding="utf-8")
    f2 = open("sentence/title-sentence"+fileNumber+".txt", "w", encoding="utf-8")
    f3 = open("sentence/title"+fileNumber+".txt", "w", encoding="utf-8")

    for docId in range(int(startDocId), int(endDocId)+1):

        newFileNumber = str(int(int(docId)/100000))
        if fileNumber != newFileNumber:
            fileNumber = newFileNumber
            f1.close()
            f2.close()
            f3.close()
            f1 = open("sentence/sentence"+fileNumber+".txt", "w", encoding="utf-8")
            f2 = open("sentence/title-sentence"+fileNumber+".txt", "w", encoding="utf-8")
            f3 = open("sentence/title"+fileNumber+".txt", "w", encoding="utf-8")
        try :
            title, sentences = naver.scrap(docId)

            f1.write(title+"\n")
            f3.write(title+"\n")
            for sentence in sentences:
                f1.write(sentence+"\n")
                f2.write(title+"\t"+sentence+"\n")
        except :
            pass


if __name__ == "__main__":
    main(sys.argv[1:])