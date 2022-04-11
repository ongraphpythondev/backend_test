import json
import requests
import jwt

from datetime import timezone, datetime, timedelta
from uuid import uuid4

from django.contrib import auth
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from ratelimit.decorators import ratelimit
from django.conf import settings
from .models import Bond
from .tokens import auth_only

User = get_user_model()


# Create your views here.

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8') 	
            body = json.loads(body_unicode) 	
            email = body['email']
            password = body['password']
        except:
            return JsonResponse({'message':'invalid json body or parameter missing'}, status=400)
        user = auth.authenticate(username = email,password=password)
        if user is not None:
            auth.login(request,user)
            payload = {
                'email':email,
                'password':password,
                'uuid':str(uuid4()),
                "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=3600)
            }
            token = jwt.encode(payload,settings.SECRET_KEY,algorithm='HS256')
            return JsonResponse({'message':'logged in', "token":token})
        else:
            return JsonResponse({'message':'invalid credentials'},status = 401)
    else:
        return JsonResponse({'message':'invalid request method'},status = 400)


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8') 	
            body = json.loads(body_unicode) 	
            email = body['email']
            password = body['password']
        except:
            return JsonResponse({'message':'invalid json body or parameter missing'}, status=400)
    
        if User.objects.filter(username = email).exists():
            return JsonResponse({'message':'email already exists'})
        else:
            user = User.objects.create_user(username = email,password=password)
            user.save()
            return JsonResponse({'message':'user created'})
    else:
        return JsonResponse({'message':'invalid request method'},status = 400)


def logout(request):
    auth.logout(request)
    return JsonResponse({'message':'logged out'})



@ratelimit(key='ip', rate='1000/m',block=True)
@csrf_exempt
@auth_only
def publish_bond(request):
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8') 	
            body = json.loads(body_unicode) 	
            bond_name = body['name']
            prince = body['price']
            number_of_bond = body['number_of_bond']
        except:
            return JsonResponse({'message':'invalid json body or parameter missing'}, status=400)

        data = jwt.decode(request.headers.get('token'), settings.SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(username = data['email'])
        
        try:
            bond = Bond.objects.create(name = bond_name,price=prince,number_of_bond=number_of_bond,seller=user)
            bond.save()
            uuid = bond.id
            return JsonResponse({'message':'bond published', 'uuid':uuid})
        except Exception as e:
            return JsonResponse({'error':e.__getattribute__('message_dict')},status = 400)
    else:
        return JsonResponse({'message':'invalid request method'},status = 400)


@auth_only
@ratelimit(key='ip', rate='1000/m',block=True)
def bond_list(request):
    if request.method == 'GET':
        data = jwt.decode(request.headers.get('token'), settings.SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(username = data['email'])
        bonds = Bond.objects.all().exclude(seller=user)
        return JsonResponse({'bonds':list(bonds.values())})
    else:
        return JsonResponse({'message':'invalid request method'},status = 400)


@csrf_exempt
@auth_only
@ratelimit(key='ip', rate='1000/m',block=True)
def buy_bond(request):
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8') 	
            body = json.loads(body_unicode)
            uuid = body['id']
        except:
            return JsonResponse({'message':'invalid json body or parameter missing'}, status=400)

        data = jwt.decode(request.headers.get('token'), settings.SECRET_KEY, algorithms=['HS256'])
        email = data['email']
        user = User.objects.get(username = email) 	
        
        bond = Bond.objects.get(id=uuid)
        
        if bond.buyer == None and bond.seller != user:
            bond.buyer = user
            bond.save()
            return JsonResponse({'message':'bond bought successfully'})
        else:
            return JsonResponse({'error':'invalid operation! This bond has been already bought'},status = 400)
    else:
        return JsonResponse({'message':'invalid request method'}, status = 400)


@auth_only
@ratelimit(key='ip', rate='1000/m',block=True)
def bond_list_usdollar(request):
    if request.method == 'GET':
        reqUrl = "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno"
        headersList = {
            "Accept": "application/json",
            "Bmx-Token": "44b9d473d63ba334ab881ad081d741cb5d605918c5c679ab381d2a11cc360cd8" 
        }
        payload = ""
        response = requests.request("GET", reqUrl, data=payload,  headers=headersList)
        
        #exchange bond price to us dollar according to latest dato from banxico
        data = json.loads(response.text)
        usd_price = data['bmx']['series'][0]['datos'][0]['dato']
        exchange_rate = float(usd_price)
       
        data = jwt.decode(request.headers.get('token'), settings.SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(username = data['email'])
        bonds = Bond.objects.all().exclude(seller=user)
        bond_list =  list(bonds.values())
    
        # divide the price by exchange rate to get the price in us dollar
        for bond in bond_list:
            bond['price'] = float(bond['price'])/exchange_rate
            #round the price to 4 decimal places
            bond['price'] = round(bond['price'],4)
    
        return JsonResponse({'bonds':bond_list})
    else:
        return JsonResponse({'message':'invalid request method'},status = 400)



