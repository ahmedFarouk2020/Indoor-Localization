from flask import Flask, request
import pandas as pd
import pickle

from sklearn.utils import estimator_html_repr
#from flask_cors import CORS




#------- GLOBAL VARIABLE -----R---
estimation = '0'  # output of the ML model
counter = 1       # counter for the ith record


# 	El-lab	El-modarag	Redmi	youssef	Farouk	target

input_to_model = pd.DataFrame({"WE_41B884":[0],"youssef":[0],"El-modarag":[0],"El-lab":[0],"Mo_Hamza":[0],"Farouk":[0],"RehabLab":[0],"redmi":[0]}, dtype=int)


model = pickle.load(open('saved_models/RandomForest87.sav', 'rb'))


app = Flask(__name__)


@app.route('/')
def home():
    return "<h2> Welcome </h2>"

# /api/send-data?ap1=1&ap2=2&ap3=3&ap4=4&ap5=5&ap6=6

s1 = 0
s2 = 0
s3 = 0
s4 = 0
s5 = 0
s6 = 0
s7 = 0
s8 = 0

@app.route('/api/send-data')
def receive():
    global estimation, input_to_model, counter, aggragate, s1, s2, s3, s4, s5, s6, s7, s8
    
    if counter == 3:
        # get the average of each data element
        input_to_model.iloc[0] = [s1/counter,s2/counter,s3/counter,s4/counter,s5/counter,s6/counter, s7/counter, s8/counter]
        estimation = model.predict(input_to_model)[0]

        counter = 0 # reset the counter
        
        # init all data elements
        s1 = 0
        s2 = 0
        s3 = 0
        s4 = 0
        s5 = 0
        s6 = 0
        s7 = 0
        s8 = 0
        
        return "<h2> Model estimation was updated </h2>"
        
    s1 += int(request.args.get('ap1'))
    print("s1= ", s1)
    s2 += int(request.args.get('ap2'))
    print("s2= ", s2)
    s3 += int(request.args.get('ap3'))
    print("s3= ", s3)
    s4 += int(request.args.get('ap4'))
    print("s4= ", s4)
    s5 += int(request.args.get('ap5'))
    print("s5= ", s5)
    s6 += int(request.args.get('ap6'))
    print("s6= ", s6)
    s7 += int(request.args.get('ap7'))
    print("s7= ", s7)
    s8 += int(request.args.get('ap8'))
    print("s8= ", s8)
    
    counter +=1
        
    return "<h2> Data is stored </h2>"


@app.route('/api/get_estimation')
def get_estimation():
    global estimation
    return str(estimation)
    
@app.route('/api/set_estimation')
def set_estimation():
    global estimation
    estimation = request.args.get('estimation')
    return estimation
    

# 192.168.43.145 ==> My IP Address
app.run(debug=True,port='5000',host="0.0.0.0")