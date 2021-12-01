from operator import mod

import tokenizers
from model import TransformersModel
from transformers import BertTokenizer
import json
import umap
from tagging import pos_tagging,pos_tagging_list



if __name__ == '__main__':
    layer = 13
    model0 = TransformersModel(
        "nlptown/bert-base-multilingual-uncased-sentiment")
    model0.setModel(layer)
    model0.getModelOutput()
    hidden_by_layer = []
    hidden = []
    word_ids = []
    reducer = umap.UMAP(random_state=42)
    color_dic = {"NOUN":"#F8766D"}
    
    pos_dic = []
    word_dic = []

    

    for data_num in range(model0.numOfdata):
        word_ids = word_ids + model0.model_inputs[data_num]['input_ids'][0].tolist()

    for index in word_ids:
        word_dic.append(str(model0.tokenizer.decode(index)).replace(" ",""))
    
    #for i in word_dic"
    
    #print(model0.embedding_by_word_json(9))
   
    
    for i in range(word_ids):
        #print(model0.tokenizer.decode(word_ids[index]))
        word = str(model0.tokenizer.decode(word_ids[i])).replace(" ","")
        print(index/len(word_ids))
        pos = pos_tagging(word)
        hidden_by_layer.append({"word":word,
                                "pos":pos,
                                "color":color_dic.setdefault(pos[0],"#00BA38"),
                                "hidden0":"NULL"})





    with open('hidden.json','w')as f :
       json.dump(hidden_by_layer,f)
