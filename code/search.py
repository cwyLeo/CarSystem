from django.http import HttpResponse
from django.shortcuts import render
from . import testdb
from TestModel.models import * 
import json
# 表单
def search_form(request):
    username = request.GET['user']
    return render(request, 'search_form.html',{'user':username})

def del_form(request):
    username = request.GET['user']
    return render(request,"del.html",{'user':username})

def OLAP_form(request):
    username = request.GET['user']
    return render(request,"OLAP_form.html",{'user':username})

def sql_form(request):
    username = request.GET['user']
    return render(request,"sql_form.html",{'user':username})

def cust_form(request):
    ctx ={}
    carlist = Car.objects.all()
    indlist = Industry.objects.all()
    ctx['carlist'] = carlist
    ctx['indlist'] = indlist
    username = request.GET['user']
    ctx['user'] = username
    return render(request,"cust_form.html",ctx)

# 接收请求数据
def search(request):
    dicts = {}
    request.encoding='utf-8'
    user = request.GET['user']
    if 'class' in request.GET and request.GET['class']:
        i = -1
        while True:
            i += 1
            key = 'conds' + str(i)
            val = 'val' + str(i)
            if key in request.GET and val in request.GET and request.GET[key] and request.GET[val]:
                dicts[request.GET[key]] = request.GET[val]
            else:
                break     
        message = '你搜索的内容为: ' + request.GET['class'] + str(dicts) + testdb.testdb(request.GET['class'],cond=dicts) 
    else:
        message = '你提交了空表单'
    return render(request,'result.html',{'mes':message,'user':user})

def delete(request):
    dicts = {}
    request.encoding='utf-8'
    user = request.GET['user']
    if 'class' in request.GET and request.GET['class']:
        i = -1
        while True:
            i += 1
            key = 'conds' + str(i)
            val = 'val' + str(i)
            if key in request.GET and val in request.GET and request.GET[key] and request.GET[val]:
                dicts[request.GET[key]] = request.GET[val]
            else:
                break     
        message = testdb.deldata(request.GET['class'],cond=dicts)
    else:
        message = '你提交了空表单'
    return render(request,'result.html',{'mes':message,'user':user})
def rank(request):
    ctx = {}
    table = request.GET.get('table')
    user = request.GET.get('user')
    print(user)
    message = testdb.rank(table)
    ctx['mes'] = message
    # return HttpResponse(message)
    return render(request,'result.html',{'mes':message,'user':user})

def login(request):
    ctx = {}
    custlist = list(Customer.objects.values_list('name',flat=True))
    ctx['custlist'] = custlist
    print(custlist)
    username = ''
    pwd = ''
    if request.POST:
        username = request.POST['username']
        pwd = request.POST['pwd']
    if username == "admin" and pwd == "123456":
        return render(request,"post.html",{'user':username,'pwd':pwd})
    elif username in custlist and pwd == "000000":
        return render(request,"search_form.html",{'user':'customer'+username})
    elif username == "market" and pwd == "888888":
        return render(request,"search_form.html",{'user':username})
    else:
        return render(request,"login.html")

def OLAP(request):
    attrs = {}
    table = request.GET.get('table')
    table2 = request.GET.get('table2')
    user = request.GET['user']
    if 'classify' in request.GET and request.GET['classify']:
        classify = request.GET['classify']
        order = request.GET['order']
        action = request.GET['action']
        i = -1
        while True:
            i += 1
            key = 'conds' + str(i)
            val = 'val' + str(i)
            if key in request.GET and val in request.GET and request.GET[key] and request.GET[val]:
                attrs[request.GET[key]] = request.GET[val]
            else:
                break
    message = testdb.OLAP(classify=classify,table=table,table2=table2,order=order,action=action,attrs=attrs)
    return render(request,'result.html',{'mes':message,'user':user})

def sql(request):
    user = request.GET['user']
    if request.GET and request.GET['message']:
        message = request.GET['message'] + testdb.sql(request.GET['message'])
    return render(request,"result.html",{'mes':message,'user':user})

def cust(request):
    user = request.GET['user']
    if request.GET:
        message = testdb.cust(request.GET['industry'],request.GET['name'])
    return render(request,"result.html",{'mes':message,'user':user})