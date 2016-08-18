# This module scraps the korean sentences from terms.naver.com
# Saves the result into vae/sentence

import tensor
from bs4 import BeautifulSoup
from urllib.request import urlopen

def scrap(docId):

    # It scraps the sentence of terms.naver.com/docId=docId
    if docId < 1 or 3430668 < docId :
        print("Invalid docId : " + str(docId))
        return
    try:
        base_url = "http://terms.naver.com/entry.nhn?docId="
        soup = BeautifulSoup(urlopen(base_url + str(docId)).read(),"html.parser")

        title = tensor.preprocess(soup.find('h2').text)[:-1]
        sentences = []
        for content in soup.findAll("p", { "class" : "txt"} ):
            for line in tensor.splitSentence(content.text):
                sentences.append(tensor.preprocess(line))

        return title, sentences

    except:
        print("Oops, I guess there is no such page for docId=" + str(docId))

