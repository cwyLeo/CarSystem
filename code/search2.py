# -*- coding: utf-8 -*-
 
from django.shortcuts import render
from django.views.decorators import csrf
from . import testdb
from TestModel.models import * 
# 接收POST请求数据
def search_post(request):
    ctx ={}
    carlist = Car.objects.all()
    indlist = Industry.objects.all()
    sizelist = Sizes.objects.all()
    customerlist = Customer.objects.all()
    ctx['carlist'] = carlist
    ctx['indlist'] = indlist
    ctx['sizelist'] = sizelist
    ctx['customerlist'] = customerlist
    if request.GET:
        table = request.GET['table']
        user = request.GET['user']
        ctx['user'] = user
    if request.POST:
        data = []
        table = request.POST['table']
        user = request.POST['user']
        ctx['user'] = user
        data.append(request.POST['n'])
        data.append(request.POST['o'])
        data.append(request.POST['p'])
        if 'q' in request.POST and request.POST['q']:
            data.append(request.POST['q'])
        if 'r' in request.POST and request.POST['r']:
            data.append(request.POST['r'])
        message = testdb.adddata(table,data)
        return render(request,'result.html',{'mes':message,'user':user})
    if user[8:] in list(Customer.objects.values_list('name',flat=True)):
        ctx['customerlist'] = [Customer.objects.get(name=user[8:])]
    if table == 'car':
        return render(request, "post.html", ctx)
    if table == 'customer':
        return render(request, "post2.html", ctx)
    if table == 'industry':
        return render(request, "post3.html", ctx)
    if table == 'buy':
        return render(request, "post4.html", ctx)
    if table == 'build':
        return render(request, "post5.html", ctx)