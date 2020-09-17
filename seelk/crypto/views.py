from django.shortcuts import render
import requests
from django import forms
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from rest_framework import status
#import time


def index(request):    
    data = {}
    data["crypto_data"] = get_crypto_data(request)
    """starttime=time.time()
    while True:
        data = {}
        data["crypto_data"] = get_crypto_data("BTC", "USD")
        time.sleep(60 - ((time.time() - starttime) % 60.0)) # update every two hours
    """
    return render(request, "crypto/index.html", data)

# return the data received from api as json object
@csrf_protect
def get_crypto_data(request):
    base = request.POST['crypto_money'].upper()
    quote = request.POST['real_money'].upper()
    print(base, ' ', quote)
    api_url = "https://rest.coinapi.io/v1/exchangerate/"+ base + "/" + quote
    headers = {'X-CoinAPI-Key' : 'DA11C51B-A493-4347-A877-D7607A6C9D09'}

    try:
        data = requests.get(api_url, headers=headers).json()
    except Exception as e:
        print(e)
        data = dict()

    rate = data.get("rate")
    if rate == None:
        return JsonResponse({'message': 'This exchange doesn\'t exist!'}, status=status.HTTP_400_BAD_REQUEST)
    
    if (rate < float(request.POST['rate'])):
        send_mail(
            'Alert',
            'The rate of ' + base + ' falls under ' + request.POST['rate'],
            'valentine.meric@epita.fr',
            [request.user.email],
            fail_silently=False,
        )
    return data