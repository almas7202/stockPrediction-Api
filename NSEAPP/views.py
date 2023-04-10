# from django.shortcuts import render
import json
import pandas as pd
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
# from nsetools import Nse
from nsepython import *

import random
from django.http import JsonResponse
# from myapp.models import *
from .form import *
# Create your views here.

def homeview(request):
    return render(request, 'home.html')

def baseview(request):
    return render(request, 'base.html')

def registerview(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form = UserCreateForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/home/') # redirect to the homepage
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = SignInForm()
    return render(request, 'login.html', {'form': form})

def userlogout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/home/')

def marketview(request):
    # nse = Nse()
    # stock_symbols = list(nse.get_stock_codes().keys())
    # print(stock_symbols)
    # random_symbols = random.sample(stock_symbols, 25)
    # stock_data = []
    # for symbol in random_symbols:
    #     try:
    #         data = nse.get_quote(symbol)
    #     except Exception as e:
    #         print(f"Error fetching live data for symbol {symbol}: {e}")
    #         continue    
    #     stock_data.append(data)
    #     print(stock_data)   
    # context = {'stock_data': stock_data}
    stocks=list(fnolist())
    random_symbols = random.sample(stocks, 15)
    stock_data = []
    for symbol in random_symbols:
        try:
            data = nsetools_get_quote(symbol)
        except Exception as e:
            print(f"Error fetching live data for symbol {symbol}: {e}")
            continue    
        stock_data.append(data)
    print(stock_data) 
    print("Top Gainers")
    responsedata = nse_get_top_gainers()
    # parsing the DataFrame in json format.
    json_records = responsedata.reset_index().to_json(orient ='records')
    topgainersData = json.loads(json_records)
    print("Top Lossers")
    toplosser = nse_get_top_losers()
    # parsing the DataFrame in json format.
    json_records = toplosser.reset_index().to_json(orient ='records')
    toplosserData = json.loads(json_records)
    context = {'stock_data': stock_data,'top_gainers_data': topgainersData,'top_losser_data':toplosserData}
    return render(request, 'exchange-live-price.html',context)


def marketlight(request):
    index=nse_index()
    json_records = index.reset_index().to_json(orient ='records')
    indexdata = json.loads(json_records)[:50]
    context={'indexdata':indexdata}
    return render(request, 'markets-light.html',context)




