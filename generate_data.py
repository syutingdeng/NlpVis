from operator import mod

import tokenizers
from model import TransformersModel
from transformers import BertTokenizer
import json
import umap
if __name__ == '__main__':
    layer = 2
    model0 = TransformersModel(
        "nlptown/bert-base-multilingual-uncased-sentiment")
    model0.setModel(layer)
    model0.getModelOutput()
    hidden_by_layer = []
    hidden = []
    word_ids = []
    reducer = umap.UMAP(random_state=42)
        
    for data_num in range(model0.numOfdata):
        word_ids = word_ids + model0.model_inputs[data_num]['input_ids'][0].tolist()
    #print(len(word_ids))
       
    # encoded = model0.tokenizer(model0.data[0][0])['input_ids']
    # decoded = model0.tokenizer.decode(encoded[0])
    # print(model0.model_inputs[0]['input_ids'])
    #print(len(model0.embedding_by_word_json(level=layer)))
    for level in range(2):
        for index, word_emb in enumerate(model0.embedding_by_word_json(level=layer)):
            #print(model0.tokenizer.decode(word_ids[index]))
            hidden_by_layer.append({"word":model0.tokenizer.decode(word_ids[index]),
                                   "hidden":word_emb})





    with open('hidden.json','w')as f :
       json.dump(hidden_by_layer,f)
