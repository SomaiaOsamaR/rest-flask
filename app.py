#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Postman Installed on the system. Postman helps to test Rest API.


# In[2]:


#pip install Flask


# In[3]:


#pip install flask-restful


# In[4]:


#pip install pandas


# In[5]:


#jsonify -> jsonify is a function in Flask's flask. json module. 
#jsonify serializes data to JavaScript Object Notation (JSON) format, 
from flask import Flask, jsonify 
# Flask-RESTful is an extension for Flask that adds support for quickly building REST APIs.
from flask_restful import Resource, Api , reqparse
#import pandas as pd 


# In[6]:


# The main entry point for the application. Create an instance of the class.
app=Flask(__name__)
api=Api(app)


# In[7]:


data_arg=reqparse.RequestParser()
data_arg.add_argument("ID" , type=int ,help="Enter ID")
data_arg.add_argument("Title" , type=str ,help="Enter Title")
data_arg.add_argument("Author" , type=str ,help="Enter Author")
data_arg.add_argument("Country" , type=str ,help="Enter Country")


# In[8]:


# To Solve Arabic text in response body issue 
def inverse_repr(a_string):
    a_string = repr(a_string)
    a_string = a_string.replace('\\\\','\\')
    # encode/decode stuff
    return a_string.strip("'").encode().decode("unicode-escape")


# In[9]:


# In this class we define function get This means that any GET Request on the url endpoint hit this function 
# and delete function will hit by Delete request.
class read_Delete(Resource):
    def __init__(self):
        # read csv file
        self.data = pd.read_excel('result.xlsx')
   
    # GET request on the url will hit this function
    def get(self,ID):
        # find data from excel based on user input
        data_fount=self.data.loc[self.data['ID'] == ID].to_json(orient="records")
        # return data found in excel
        return jsonify({'message': inverse_repr(data_fount)})
    # Delete request on the url will hit this function
    
    def delete(self,ID):
        if ((self.data['ID'] == ID).any()):
            # Id it present delete data from csv
            self.data = self.data.drop(self.data["ID"].loc[self.data["ID"] == ID].index)
            self.data.to_excel("result.xlsx", index=False)
            return jsonify({"message": 'Deleted successfully'})
        else:
            return jsonify({"message": 'Not Present'})


# In[10]:


# In this class we define functions post, 
# and put means any POST PUT Request on the URL endpoint will be hitting their respective function.
class Create_Update(Resource):
    def __init__(self):
        # read data from csv
        self.data = pd.read_excel('result.xlsx')

    # POST request on the url will hit this function
    def post(self):
        # data parser to parse data from url
        args = data_arg.parse_args()
        # if ID is already present
        if((self.data['ID']==args.ID).any()):
            return jsonify({"message": 'ID already exist'})
        else:
            # Save data to csv
            self.data= self.data.append(args, ignore_index=True)
            self.data.to_excel("result.xlsx", index=False)
            return jsonify({"message": 'Done'})

    # PUT request on the url will hit this function
    def put(self):
        args = data_arg.parse_args()
        if ((self.data['ID'] == args.ID).any()):
            # if ID already present Update it
            self.data=self.data.drop(self.data["ID"].loc[self.data["ID"] == args.ID].index)
            self.data = self.data.append(args, ignore_index=True)
            self.data.to_excel("result.xlsx", index=False)
            return jsonify({"message": 'Updated successfully'})
        else:
            # If ID not present Save that data to csv
            self.data = self.data.append(args, ignore_index=True)
            self.data.to_excel("result.xlsx", index=False)
            return jsonify({"message": 'successfully Created'})


# In[11]:


# adding the defined resources along with their corresponding URLs
api.add_resource(read_Delete, '/<int:ID>')
api.add_resource(Create_Update,'/')


# In[12]:


#pip install GitPython


# In[13]:


#Gunicorn is a web server that is more powerful than the built-in server that flask gives you. 
#The built-in server in the flask can only handle one user at a time. But Gunicorn can deal with many users at once.


# In[14]:


#pip install gunicorn


# In[15]:


#pip freeze > requirements.txt


# In[16]:


#git init .


# In[17]:


#git add app.py Procfile requirements.txt
#git commit -m "first commit"


# In[18]:


# main function for calling the app
app.run(debug = True,use_reloader = False)
if __name__ == '__main__':
     app.run(debug=True)


# In[ ]:





# In[ ]:





# In[ ]:




