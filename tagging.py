import spacy

def pos_tagging(snetence):
    pos = [ ]
    nlp = spacy.load("en_core_web_sm")
    for i in nlp(snetence):
        pos.append(i.pos_)
    return pos



