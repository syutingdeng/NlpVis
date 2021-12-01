import spacy
import pandas as pd
from tqdm import tqdm, tqdm_pandas

def pos_tagging(sentence):
    pos = [ ]
    nlp = spacy.load("en_core_web_sm")
    for i in nlp(str(sentence)):
        pos.append(i.pos_)
    return pos






def  pos_tagging_list(s):
    table = pd.DataFrame({"Setence":s})
    table['pos'] = table.apply(lambda x:pos_tagging(x['Setence']),axis=1)
    print(list(table['pos']))


#pos_tagging_list(["hi","how","are","you","hi","how","are","you","hi","how","are","you","hi","how","are","you","hi","how","are","you","hi","how","are","you","hi","how","are","you","hi","how","are","you"])