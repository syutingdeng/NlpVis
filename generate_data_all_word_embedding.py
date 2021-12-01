from operator import le
from model import TransformersModel
from analysis import CountAvgScore, acc, pos_count, pos_count_select
import json

if __name__ == "__main__":
    model0 = TransformersModel('nlptown/bert-base-multilingual-uncased-sentiment')
  
    num_layer = 2
    all_word_hidden = {}
    clas = []
    hidden = []
    
    
    for i in range(num_layer):
        model0.setModel(i)
        model0.getModelOutput()
        model0.classify()
        model0.part_of_speech()
        #model0.getDataSetHiddenState(i)
        #hidden.setdefault("hidden"+str(i),model0.embedding_by_word_json(i)) #reduce dimension embedding by word
        hidden.append(model0.getClsEmbedding(i))
        clas.append(model0.sentiment)    

    
    #print(hidden[0]['hidden0'])
    #print(model0.web_umap(mode="ground",condition1=0,condition2=1))
    
    seq_all = []
    for index,item in enumerate (model0.data[0]):
        sentence = {"id":index,"sentence":item,"groundtruth":model0.data[1][index],"pos":model0.pos[index]}
        for i in range(num_layer):
            sentence.setdefault("layer"+str(i),{"hidden":hidden[i][index],"classify":clas[i][index]})
       
        #print(sentence)    

        seq_all.append(sentence)
    #info = {"sequence":seq_all,"all_word_hidden": all_word_hidden}
   
    
    """

    for i in range(num_layer):
        model0.setModel(i) ###Setting model and model layer
        model0.getModelOutput()### Get model output
        #model0.getDataSetHiddenState(i)#get specify layer hidden state
        #model0.getDataAttention(level=i,index=1,word_index=0)
        model0.embedding_by_word_json(i)
        model0.ground_truth()
        model0.classify()
        #model0.part_of_speech()
    """
        
        
        
    with open('all_dataset.json','w')as f :
       json.dump(seq_all,f)