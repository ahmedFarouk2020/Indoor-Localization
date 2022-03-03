from flask import Flask, request
import pandas as pd
import pickle

#------- GLOBAL VARIABLE -----R---
estimation = '0'  # output of the ML model
counter = 0       # counter for the ith record


aggragate = pd.DataFrame({"STUDBME1":0,"STUDBME2":[0],"CMP_LAB1":[0],"CMP_LAB2":[0],"CMP_LAB3":[0],"CMP_LAB4":[0]}, dtype=int)
input_to_model = pd.DataFrame({"STUDBME1":0,"STUDBME2":[0],"CMP_LAB1":[0],"CMP_LAB2":[0],"CMP_LAB3":[0],"CMP_LAB4":[0]}, dtype=int)


model = pickle.load(open('../saved_models/randomForest_84all.sav', 'rb'))


app = Flask(__name__)

@app.route('/')
def home():
    return "<h2> Welcome </h2>"

# /api/send-data?ap1=1&ap2=2&ap3=3&ap4=4&ap5=5&ap6=6
@app.route('/api/send-data')
def receive():
    global estimation, input_to_model, counter, aggragate
    s1 = request.args.get('ap1')
    print("s1= ", s1)
    s2 = str(request.args.get('ap2'))
    print("s2= ", s2)
    s3 = str(request.args.get('ap3'))
    print("s3= ", s3)
    s4 = str(request.args.get('ap4'))
    print("s4= ", s4)
    s5 = str(request.args.get('ap5'))
    print("s5= ", s5)
    s6 = str(request.args.get('ap6'))
    print("s6= ", s6)
    
    input_to_model.iloc[0] = [s1,s2,s3,s4,s5,s6]

    estimation = model.predict(input_to_model)[0]
        
    return "<h2> Data is stored </h2>"


    estimation = model.predict(input_to_model)[0]
# @app.route('/api/send-data')
# def receive():
    # global estimation, input_to_model, counter, aggragate
    # s1 = request.args.get('ap1')
    # print("s1= ", s1)
    # s2 = str(request.args.get('ap2'))
    # print("s2= ", s2)
    # s3 = str(request.args.get('ap3'))
    # print("s3= ", s3)
    # s4 = str(request.args.get('ap4'))
    # print("s4= ", s4)
    # s5 = str(request.args.get('ap5'))
    # print("s5= ", s5)
    # s6 = str(request.args.get('ap6'))
    # print("s6= ", s6)
    
    # input_to_model.iloc[0] = [s1,s2,s3,s4,s5,s6]

    # aggragate = aggragate.append(input_to_model.iloc[0])
    # print(aggragate)
    # counter += 1
    
    # if counter == 6:
        # estimate()
        # aggragate = aggragate[0:0]
        # counter = 0
        # return "<h2> Model has updated the data </h2>"
        
    # return "<h2> Data is stored </h2>"


# def estimate():
    # global input_to_model, aggragate, estimation
    # # get mean of 5 readings
    # print(aggragate.mean())
    # input_to_model.loc[0] = (aggragate.mean()+0.5).astype(int)
    # print(input_to_model)
    # estimation = model.predict(input_to_model)[0]


@app.route('/api/get_estimation')
def get_estimation():
    return str(estimation)
    
@app.route('/api/set_estimation')
def set_estimation():
    global estimation
    estimation = request.args.get('estimation')
    return estimation
    


app.run(debug=True,port='5000',host="0.0.0.0")