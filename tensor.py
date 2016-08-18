import re

# This function preprocesses the sentence
# 1. It removes the irregular space
# 2. If it does not end with ".", then append it
# 3. It removes the characters between parenthesis
# 4. If it contains out-of-scope characters, it removes it
def preprocess(sentence):

    if len(sentence) < 1:
        return sentence

    # [1] It removes the characters between parenthesis
    # ? in regex means "greedy"
    sentence = re.sub(r"\(.*?\)","", sentence)

    # [2] If it contains out-of-scope characters, remove it
    # Korean Syllable : \uAC00-\uD7AF
    # Korean Alphabet : \u1100-\u11FF
    # Alphanumeric and noted character : \u0021-\u007E
    sentence = re.sub('[^\uAC00-\uD7AF\u1100-\u11FF\u0021-\u007E ]+',"",sentence)
    # Replace various whitespace into normal space
    sentence = re.sub('[\s]+'," ",sentence)

    # If out-of-string-index error occurs, just ignore it
    try:
        # [3] It removes start-space
        if sentence[0] == ' ':
            sentence = sentence[1:]

        # [4] If it does not end with ".", then append it
        if sentence[-1] != '.':
            sentence += "."
    except:
        return sentence

    return sentence

# Split the sentence out of text corpus
# Returns the list of sentence
def splitSentence(text):
    result = []
    # Do not split the sentence for the case of "0.3"
    text = re.sub(r'([0-9])\.([0-9])',r'\1@\2',text)
    # Do not split the sentence for the case of "e.g", "cf.", "St.", "st.", "s.t"
    text = text.replace("e.g", "e@g").replace("cf.", "cf@").replace("St.", "St@").replace("st.", "st@").replace("s.t", "s@t")
    for line in text.split("."):
        line = line.replace("@",".")
        if len(line) > 0:
            result.append(line)
    return result