from transformers import BertTokenizer, BertForSequenceClassification,BertConfig
import torch
from transformers import pipeline
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import umap
from mpl_toolkits.mplot3d import Axes3D

class TransformersModel:
    
    def __init__(self,model_name,UserInput):
        self.model_name=model_name
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.UserInput = UserInput

    def setModel(self,layer):
        config = BertConfig(num_hidden_layers=layer,output_hidden_states=True)
        self.model = BertForSequenceClassification(config)
        print("-----------------MODEL--------------------")
        print("Model name"+self.model_name+"\n")
        print(self.model)

    def getHiddenState(self,level):
        inputs = self.tokenizer(self.UserInput, return_tensors="pt")
        labels = torch.tensor([1]).unsqueeze(0)  # Batch size 1
        outputs = self.model(**inputs, labels=labels)
        self.hidden_states = outputs.hidden_states[level][0]
        self.length = outputs.hidden_states[level][0].shape[0]
        self.level = level
        print("Hidden Stat layer"+str(level))
        return outputs.hidden_states[level][0]

    def classify(self):
        classifier = pipeline('sentiment-analysis', model=self.model, tokenizer=self.tokenizer)
        return classifier(self.UserInput)

        
    def umap(self):
        reducer = umap.UMAP(random_state=42)
        word_embedding = []
        for i in range(self.length):    
            word_embedding.append(self.hidden_states[i].detach().numpy())
        word_embedding = np.array(word_embedding)
        word_embedded_reduce = reducer.fit_transform(word_embedding)
        
        x=[]
        y=[]
        x_min, x_max =  word_embedded_reduce.min(0), word_embedded_reduce.max(0)
        a_norm = (word_embedded_reduce - x_min) / (x_max - x_min)
        for i in a_norm:
            x.append(i[0])
            y.append(i[1])
        print(x)
        print(y)
        plt.plot(x,y,'ro')
        plt.show()
    
    

    


model0 = TransformersModel('bert-base-uncased',"UMAP is a general purpose manifold learning and dimension reduction algorithm. It is designed to be compatible with scikit-learn, making use of the same API and able to be added to sklearn pipelines.")
model0.setModel(6)
model0.getHiddenState(3)
#model0.umap()

print(model0.classify())
