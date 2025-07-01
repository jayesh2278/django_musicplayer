# Create your views here.
from functools import cache
from urllib import response
from django.http import HttpResponse
from django.shortcuts import render,redirect
# imported our models
from django.core.paginator import Paginator
from .models import Song
from django.core.cache import cache
import redis
from django.conf import settings
import secrets


def index(request):
        paginator= Paginator(Song.objects.all(),1)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # context={"page_obj":page_obj}

        return render(request,"index.html",{'page_obj':page_obj,}) 

# def comlr(request,id):
#     son = Song.objects.get(pk=id) 
#     pko = Skipcount.objects.create(song=son)
#     songcount = Skipcount.objects.filter(song=id).count()
#     print(songcount)    
#     return render(request, "counter.html",{"songcount":songcount})

r = redis.Redis(host=settings.REDIS_HOST,
                   port=settings.REDIS_PORT,
                   db=settings.REDIS_DB)      

def coml(request,id):
    # for getting ip adress of user who click skip button
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # print "returning FORWARDED_FOR"
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        # print "returning REAL_IP"
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        # print "returning REMOTE_ADDR"
        ip = request.META.get('REMOTE_ADDR')
    print(ip)
    number = secrets.SystemRandom().randint(0,255)
    ip = f'192.168.0.{number}'
    # 
    # redis operations
    user_key = f"{ip}:{id}"
    skip_counter = f"skipper:{id}"
    response = r.get(user_key)
    if response is None:
        print("Updating counter")
        r.set(user_key, "SKIPPED", keepttl=True)
        r.expire(user_key, 600)
        r.incr(skip_counter,1)
        r.expire(skip_counter, 600*5)
    else:
        print("not updating same ip found!!")    
    total_skip =  r.get(skip_counter)
    print(total_skip)

    return HttpResponse("ok")
