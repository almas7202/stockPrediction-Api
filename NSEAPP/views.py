# from django.shortcuts import render
import json
import pandas as pd
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
# from nsetools import Nse
from nsepython import *
from django.http import HttpResponse
from sklearn.linear_model import LinearRegression
import random
from django.http import JsonResponse
# from myapp.models import *
from .form import *
from .models import *
import os
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


def symbol_get(request):
    symbol=list(fnolist())
    for data in symbol:
        ans=Stock(symbol=data)
        ans.save()
    return redirect('/marketview/')

def generate_csv(symbol):
    # symbol = Stock.objects.filter(symbol=symbol)[1]
    # start_date = "01-01-2023"
    # end_date = "10-04-2023"
    # series = "EQ"
    # data = nsefetch("https://www.nseindia.com/api/historical/cm/equity?symbol="+symbol+"&series=[%22"+series+"%22]&from="+start_date+"&to="+end_date+"")
    # data.to_csv(f"{symbol}.csv", index=False)
    start_date = "01-01-2023"
    end_date = "10-04-2023"
    series = "EQ"
    data_dict = nsefetch("https://www.nseindia.com/api/historical/cm/equity?symbol="+symbol+"&series=[%22"+series+"%22]&from="+start_date+"&to="+end_date+"")
    data = pd.DataFrame(data_dict['data'])
    data.to_csv(f"{symbol}.csv", index=False)


def add_to_watchlist(request):
    # symbol=request.POST['symbol']
    # stock = Stock.objects.filter(symbol=symbol)
    # ans = stock.first()
    # Watchlist(user=request.user,stock=ans).save()
    # generate_csv(stock)
    # return redirect('/watchlist/')
    symbol=request.POST['symbol']
    stock = Stock.objects.filter(symbol=symbol)[:1]
    if stock:
        ans = stock[0]
        generate_csv(ans.symbol)
        prediction = predict_price(symbol)
        Watchlist(user=request.user,stock=ans,predicted_price=prediction).save()
        print(prediction)
        return redirect('/watchlist/')
    else:
        return HttpResponse("Stock not found")
        


def Watchlistview(request):
    watch=[]
    get_stock=Watchlist.objects.filter(user=request.user)
    print(get_stock)
    for i in get_stock:
        quote_data =nsetools_get_quote(i.stock.symbol)
        prediction_data =i.predicted_price
        row_data = {
            'symbol': quote_data['symbol'],
            # 'companyName': quote_data['companyName'],
            'open': quote_data['open'],
            'dayHigh': quote_data['dayHigh'],
            'dayLow': quote_data['dayLow'],
            'lastPrice': quote_data['lastPrice'],
            'pChange': quote_data['pChange'],
            'change': quote_data['change'],
            'previousClose': quote_data['previousClose'],
            'totalTradedVolume': quote_data['totalTradedVolume'],
            'prediction': prediction_data
        }
        watch.append(row_data)
        print(watch)
    context={'watch':watch}
    return render(request, 'watchlist.html',context)

def Removestock(request,symbol):
    stock = Stock.objects.filter(symbol=symbol)
    stock_symbol = stock.first()
    get_symbol=Watchlist.objects.filter(user=request.user,stock=stock_symbol)
    get_symbol.delete()
    # messages.success(request, f"{symbol} removed from your watchlist.")
    return redirect('/watchlist/')


def predict_price(symbol):
    data = pd.read_csv(f"{symbol}.csv")
    X = data[['CH_OPENING_PRICE', 'CH_LAST_TRADED_PRICE','CH_TOTAL_TRADES']]
    y = data['CH_CLOSING_PRICE']
    model = LinearRegression()
    model.fit(X, y)
    last_row = data.tail(1)
    prediction = model.predict(last_row[['CH_OPENING_PRICE', 'CH_LAST_TRADED_PRICE','CH_TOTAL_TRADES']])
    return prediction[0]

