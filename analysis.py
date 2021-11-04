def acc(info,select_list,layer):
    
    id_resutlt = []
    result_result = []
    all_result = []
    
    for j in range(layer):
        id = [] 
        result = []
        for i in range(len(info[j]['ground'])):
            if i in select_list:
                c1 = info[j]['classify'][i]['label']
                c2 = info[j]['ground'][i]['label']
                if(c1 == "1 star" or c1 == "2 stars" or c1 =="3 stars"):
                    if(c2==0):
                        result.append(1)
                        id.append(i)
                    else:
                        result.append(0)
                if(c1=="4 stars" or c1=="5 stars"):
                    if(c2==1):
                        result.append(1)
                        id.append(i)
                    else:
                        result.append(0)

        total = 0
        for i in result:
            total +=i
        
        acc = total / len(result)
        acc = round(acc,2)
        result_result.append([acc,j])
        
        id_resutlt.append(id)
    
    all_result = [result_result,id_resutlt]
    all_result = {"accuracy":result_result,"true_selection":id_resutlt}
    print(all_result)


    return  all_result


def CountAvgScore(info,select_list,layer,key):
  
    result = []
    for j in range(layer):
        score = 0
        for i in select_list:
            score +=info[j][key][i]
        avg = score/len(select_list)
        result.append([avg,j])
    
    print(result)
    
    return result



def pos_count(data):
    result = {}
    for word in data :
        result.setdefault(word,0)
        result[word] = result[word]+1
    return result

def pos_count_select(select,data,layer):
    all_result = []
    
    for j in range(layer):
        result = {}
        d3_result=[]
        for index,item in enumerate(data):
            if index in select[j]:
               for key in item.keys():
                   result.setdefault(key,0)
                   result[key] = result[key]+item[key]
        for key in result.keys():
            d3_result.append({"pos":key,"amount":result[key]})
        
        all_result.append(d3_result)
        print(all_result)
    return all_result
        

    
            
            