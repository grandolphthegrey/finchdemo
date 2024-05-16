#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 16:21:18 2024

@author: George
"""

import requests
import pandas as pd
from flask import Flask,request, jsonify, render_template, session, redirect
from flatten_json import flatten

url = 'https://sandbox.tryfinch.com/api/'
products = ["company", "directory", "individual", "employment"]
employee_size = 10
header = {"content-type":"application/json", "Finch-API-Version":"2020-09-17"}

app = Flask('app')
app.secret_key = 'dljsa#lqk24e2199jn!Ew@@dsa5'

@app.route('/')
def home():
    #return 'Hello, World!'
    return render_template("home.html")

@app.route('/createSandbox',methods=['POST'])
def createSandbox():
    #get the user selected provider
    provider = request.form['provider']
    #update the payload
    payload = {'provider_id':provider,'products':products, 'employee_size':employee_size}
    #make the API request
    r = requests.post(url+'/sandbox/create',headers=header,json=payload)
    #save bearer token to session
    token = r.json()['access_token']    
    print(token)
    session['token'] = token
    #return success message
    return redirect('http://127.0.0.1:5000/company')
  
@app.route('/company', methods=['GET'])
def getCompany():
    #update header
    header.update(Authorization='Bearer '+session.get('token'))
    #make API call to company endpoint
    r = requests.get(url+'/employer/company',headers=header)
    if r.status_code != 200:
        return "Provider has not implemented the requested products. Go back and select a different provider"
    else:
        #convert output to HTML
        tbl = pd.DataFrame(flatten(r.json()),index=['info']).T.to_html()
        #display output
        return render_template('basic.html', table=tbl)

@app.route('/directory',methods=['GET'])
def getDirectory():
    #update header
    header.update(Authorization='Bearer '+session.get('token'))
    #mkae API call to directory endpoint
    r = requests.get(url+'/employer/directory',headers=header)
    #convert output to HTML
    tbl = pd.DataFrame(flatten(r.json()),index=['info']).T.to_html()
    #display output
    return render_template('basic.html', table=tbl)

@app.route('/individual',methods=['POST'])
def getIndividual():
    #update header
    header.update(Authorization='Bearer '+session.get('token'))
    #get info
    provider = request.form['individual']
    #update payload
    payload={'requests':[{'individual_id':provider}]}
    #make API call to individual endpoint
    r = requests.post(url+'/employer/individual',headers=header,json=payload)
    print(r.content)
    #convert output to HTML
    arr = flatten(r.json()['responses'][0])
    arr = {k:(None if isinstance(v, list) else v) for k,v in arr.items()}
    tbl = pd.DataFrame(arr,index=['info']).T.to_html()
    #display output
    return render_template('employee.html', table=tbl)

@app.route('/employment',methods=['POST'])
def getEmployment():
    #update header
    header.update(Authorization='Bearer '+session.get('token'))
    #get info
    provider = request.form['employment']
    #update payload
    payload={'requests':[{'individual_id':provider}]}
    #make API call to individual endpoint
    r = requests.post(url+'/employer/employment',headers=header,json=payload)
    print(r.content)
    #convert output to HTML
    arr = flatten(r.json()['responses'][0])
    arr = {k:(None if isinstance(v, list) else v) for k,v in arr.items()}
    tbl = pd.DataFrame(arr,index=['info']).T.to_html()
    #display output
    return render_template('employee.html', table=tbl)
  
app.run(host='http://127.0.0.1', port=5000)
