from inspect import classify_class_attrs
from transformers import BertTokenizer, BertForSequenceClassification, BertConfig, AutoModelForSequenceClassification, AutoTokenizer
import torch
from transformers import pipeline
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


import umap
from analysis import pos_count
from prepare_data import loaddata


class TransformersModel:

    def __init__(self, model_name):
        self.model_name = model_name
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.data = loaddata()  # load from dataset

    def setModel(self, layer):
        #config = BertConfig(num_hidden_layers=layer,output_hidden_states=True)
        #self.model = BertForSequenceClassification(config)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name, output_hidden_states=True,
            num_hidden_layers=layer,
            output_attentions=True
        )
        print("-----------------MODEL--------------------")
        print("Model name"+self.model_name+"\n")
        print(self.model)
        self.layer = layer

    # get uesr input hiddenstate
    def getUserInputHiddenState(self, UserInput, level):
        self.UserInput = UserInput
        inputs = self.tokenizer(self.UserInput, return_tensors="pt")
        labels = torch.tensor([1]).unsqueeze(0)  # Batch size 1
        outputs = self.model(**inputs, labels=labels)
        self.hidden_states = outputs.hidden_states[level][0]
        self.length = outputs.hidden_states[level][0].shape[0]
        print("Hidden Stat layer"+str(level))
        return outputs.hidden_states[level][0]

    def getModelOutput(self,level):
        outputs = []
        for index, item in enumerate(self.data[0]):
            if(index %10 == 0):
                print("#", str(index))
                print(item)
            inputs = self.tokenizer(
                item, return_tensors="pt", padding='max_length', max_length=50)
            # labels = torch.tensor([1]).unsqueeze(0)  # Batch size 1
            outputs.append(self.model(**inputs)) 
        self.outputs = outputs
        self.level = level
        



    def getDataAttention(self, level,index,word_index):#哪個字對應哪個字的Attention
        cls_attention = []
        if level !=0 :
            for i in self.outputs:
               cls_attention.append(i.attentions[level-1][0][0][index][word_index].detach().numpy().tolist())
        else:
            for i in range(len(self.data[0])):
                cls_attention.append(0)
        self.attention = cls_attention
            
    def getDataSetHiddenState(self, level):  # get dataset "cls" hiddenstate
        cls_embedding = []
        
        for i in self.outputs:
            cls_embedding.append(
               i.hidden_states[level][0][0])
            print(len(i.hidden_states[level][0]))
            
        self.cls_embedding = cls_embedding
        self.cls_embedding_np = np.array(cls_embedding)
        self.dataset_length = len(cls_embedding)
        print("cls_embedding length", str(self.dataset_length))
        word_embedding = []
        for i in range(self.dataset_length):
            word_embedding.append(self.cls_embedding[i].detach().numpy())
        self.web_word_embedding = np.array(word_embedding)
        return np.array(word_embedding).tolist()


    def classify(self):
        #classifier = pipeline('sentiment-analysis')
        classifier = pipeline('sentiment-analysis',
                              model=self.model, tokenizer=self.tokenizer)
        classify = []
        score = []
        for i in self.data[0]:
            classify.append(classifier(i)[0])
            score.append(classifier(i)[0]['score'])
        self.sentiment = classify
        self.score = score

        # return classifier(self.UserInput)
    def ground_truth(self):
        self.ground_truth_sentiment = self.data[1]

    def UserInputClassify(self):
        classifier = pipeline('sentiment-analysis',
                              model=self.model, tokenizer=self.tokenizer)
        return classifier("I love you")[0]


    def umap(self, mode, condition1, condition2):
        reducer = umap.UMAP(random_state=42)
        word_embedding = []
        for i in range(self.dataset_length):
            word_embedding.append(self.cls_embedding[i].detach().numpy())
        # print(word_embedding)
        word_embedding = np.array(word_embedding)
        word_embedded_reduce = reducer.fit_transform(word_embedding)

        """for i in range(self.length):    
            word_embedding.append(self.hidden_states[i].detach().numpy())
        print(word_embedding)
        word_embedding = np.array(word_embedding)
        word_embedded_reduce = reducer.fit_transform(word_embedding)"""

        x = []
        y = []
        x_min, x_max = word_embedded_reduce.min(0), word_embedded_reduce.max(0)
        word_embedded_norm = (word_embedded_reduce - x_min) / (x_max - x_min)

        
        # for i in word_embedded_reduce:
        #    x.append(i[0])
        #    y.append(i[1])

        x0 = []
        y0 = []
        x1 = []
        y1 = []
        x2 = []
        y2 = []

        if(mode == "ground"):
            label = self.ground_truth_sentiment
        else:
            label = self.sentiment
        for index, item in enumerate(word_embedded_norm):
            if(label[index]['label'] == condition1):
                x0.append(item[0])
                y0.append(item[1])
            elif(label[index]['label'] == condition2):
                x1.append(item[0])
                y1.append(item[1])
            else:
                x2.append(item[0])
                y2.append(item[1])
        # print(word_embedded_reduce)
        print("=================")
        print(x0)
        print(y0)
        print(x1)
        print(y1)
        print(x2)
        print(y2)
        plt.scatter(x0, y0, c="red")
        plt.scatter(x1, y1, c="green")
        plt.show()
        # plt.plot(x,y,'ro')
        #

    def web_umap(self, mode, condition1, condition2):
        reducer = umap.UMAP(random_state=42)
        word_embedded_reduce = reducer.fit_transform(self.web_word_embedding)
        x_min, x_max = word_embedded_reduce.min(0), word_embedded_reduce.max(0)
        word_embedded_norm = (
            (word_embedded_reduce - x_min) / (x_max - x_min)).tolist()
        for index, item in enumerate(word_embedded_norm):
            if(mode == "ground"):
                label = self.ground_truth_sentiment
            else:
                label = self.sentiment
            if(label[index]['label'] == condition1):
                item.append("#F8766D")
            elif(label[index]['label'] == condition2):
                item.append("#00BA38")
            else:
                item.append("#619CFF")
            item.append(index)
            item.append(
                {"ground": self.ground_truth_sentiment[index]['label'], "sentiment": self.sentiment[index]['label'],"layer":self.level})

        return word_embedded_norm

    def set_all_word_embedding(self,embedding):
        self.all_word_embedding = embedding
    
    def web_umap_all(self):
       
        all_embedding_list = []
        for i in self.all_word_embedding:
            for n in i.get("embedding"):
                all_embedding_list.append(n)
        
        reducer = umap.UMAP(random_state=42)
        word_embedded_reduce = reducer.fit_transform(all_embedding_list)
        x_min, x_max = word_embedded_reduce.min(0), word_embedded_reduce.max(0)
        word_embedded_norm = (
            (word_embedded_reduce - x_min) / (x_max - x_min)).tolist()

        level_count = -1
        data_count = 0
        label = self.ground_truth_sentiment
        for index,item in enumerate(word_embedded_norm):
            data_count= index%len(self.data[0])
            print("selddata length")
            print(len(self.data[0]))
            if(label[data_count]['label'] == 0):
                item.append("#F8766D")
            elif(label[data_count]['label'] == 1):
                item.append("#00BA38")
            else:
                item.append("#619CFF")
            if index % len(self.data[0]) ==0:
                level_count =level_count+1
            item.append(data_count)     
            item.append({"layer":level_count})        
                    
        
        print(word_embedded_norm)
        return word_embedded_norm

    def embedding_umap(self):
        all_embedding_list = []
        for i in self.all_word_embedding:
            for n in i.get("embedding"):
                all_embedding_list.append(n)
        
        reducer = umap.UMAP(random_state=42)
        word_embedded_reduce = reducer.fit_transform(all_embedding_list)
        x_min, x_max = word_embedded_reduce.min(0), word_embedded_reduce.max(0)
        word_embedded_norm = (
            (word_embedded_reduce - x_min) / (x_max - x_min)).tolist()
        self.word_embedding_norm = word_embedded_norm

    def part_of_speech(self):
        pos_dic = []
        for i in self.data[2]:
            pos_dic.append(pos_count(i))
        self.pos = pos_dic    

    
    
    
        



if __name__ == "__main__":
    all_hidden = []
    model0 = TransformersModel(
        'nlptown/bert-base-multilingual-uncased-sentiment')
    model0.setModel(12)
    model0.getDataSetHiddenState(12)
    model0.classify()
    model0.ground_truth()
    print(model0.sentiment_Accuracy(data=[9, 11, 13, 14, 17]))

    # print(model0.confusionMatrix())
    # model0.umap(condition="NEGATIVE")

    # model0.umap(mode="normal",condition="LABEL_0")
