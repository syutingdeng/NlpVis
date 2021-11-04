from flask import Flask, jsonify, render_template, request
from model import TransformersModel
from analysis import CountAvgScore, acc, pos_count, pos_count_select
import json
app = Flask(__name__)


model0 = TransformersModel('nlptown/bert-base-multilingual-uncased-sentiment')
info = []
num_layer = 2
@app.route('/_get_embedding')
def get_embedding():
  
   
    for i in range(num_layer):
        model0.setModel(i)
        model0.getModelOutput(level=i)
        model0.getDataSetHiddenState(i)
        model0.getDataAttention(level=i,index=1,word_index=0)
        model0.ground_truth()
        model0.classify()
        model0.part_of_speech()
        info.append({"ground":model0.ground_truth_sentiment,
                    "classify":model0.sentiment,
                    "layer":i,
                    "score":model0.score,
                    "attention":model0.attention,
                    })
  
    return jsonify(result = model0.web_umap(mode="ground",condition1=0,condition2=1),
                   )
    
@app.route('/_return_select', methods=['POST'])
def return_embedding():
    a = request.form.get("ids")
    a_list = json.loads(a)
    int_list = list(map(int,a_list))
    result = acc(info,int_list,layer=num_layer)["accuracy"]
    score = CountAvgScore(info,int_list,layer=num_layer,key='score')
    attention = CountAvgScore(info,int_list,layer=num_layer,key='attention')
    pos = pos_count_select(select=acc(info,int_list,layer=num_layer)["true_selection"],data=model0.pos,layer= num_layer)


    #for i in range(13):
    #    acc = model0.sentiment_Accuracy(data=int_list)
    #    result.append([acc,i])

    
        
    return jsonify(result=result,score=score,attention=attention,pos=pos)
    
@app.route('/_all_hidden')
def all_projection():
    all_hiddenstate = []
    for i in range(num_layer):
        model0.setModel(i)
        model0.getModelOutput(level=i)
        model0.ground_truth()
        all_hiddenstate.append({
            "embedding":model0.getDataSetHiddenState(i),
            "layer":i})
    model0.set_all_word_embedding(embedding=all_hiddenstate)
    
    

    return jsonify(result=model0.web_umap_all())
              
        
        
        

@app.route('/')
def index():
    return render_template('index.html')
if __name__ =="__main__":
    app.run(debug=True)



