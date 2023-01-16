# -*- coding: utf-8 -*-
 
from django.http import HttpResponse
from django.db.models import Sum
from django.db import connection 
from TestModel.models import *
import sys
# 数据库操作
def getclass(table):
    aMod = sys.modules["TestModel.models"]
    aClass = getattr(aMod,str.capitalize(table))
    return aClass

def getattrkey(aClass,list):
    names = [i for i in dir(aClass) if i not in dir(Base)]
    dels = []
    for name in names:
        if len(list) == 0:
            if name[0] == '_' or name[-4:] == '_set':
                dels.append(name)
        elif name[0] == '_' or name not in list[0].__dict__.keys():
            dels.append(name)
    names = set(names) - set(dels)
    return names

def adddata(table,data):
    m_class = getclass(table)
    if len(data) == 4:
        if table == 'build':
            m_car = Car.objects.get(name=data[0])
            m_ind = Industry.objects.get(id=data[2])
            if update_industry(data[2],int(data[1]),table):
                return "build failed"
            with connection.cursor() as cur:
                cur.execute("select amount from build where industry = '"+data[2]+"' and car_name = '"+data[0]+"' and date = '"+data[3]+"'")
                obj = cur.fetchall()
            if len(obj) != 0:
                obj = Build.objects.get(industry=data[2],car_name=data[0],date=data[3])
                obj.amount += int(data[1])
                Build.objects.filter(industry=data[2],car_name=data[0],date=data[3]).update(amount=obj.amount)
                return "update success"
            else:
                m_class.objects.create(car_name = m_car,industry = m_ind,amount=int(data[1]),date=data[3])
                # obj = m_class(data[0],data[2],int(data[1]),data[3])
                return "update success"
        else:
            obj = m_class(data[0],int(data[1]),data[2],data[3])
    else:
        if table == 'buy':
            with connection.cursor() as cur:
                cur.execute("select amount from build where industry = '"+data[2]+"' and car_name = '"+data[0]+"'")
                obj = cur.fetchall()
            # obj = Build.objects.get(industry=data[2],name=data[0])
            if len(obj) == 0:
                return "lack of "+data[3]+ " car"
            tmp = int(data[3])
            while len(obj)!=0:
                with connection.cursor() as cur:
                    cur.execute("select amount,date from build where industry = '"+data[2]+"' and car_name = '"+data[0]+"'")
                    obj = cur.fetchall()
                if obj[0][0] == 0:
                    continue
                if obj[0][0] <= tmp:
                    tmp -= obj[0][0]
                    with connection.cursor() as cur: cur.execute("delete from build where industry = '"+data[2]+"' and car_name = '"+data[0]+"' and date = '"+str(obj[0][1])+"' and amount="+str(obj[0][0]))
                    # obj = Build.objects.filter(industry=data[2],name=data[0])
                    with connection.cursor() as cur: cur.execute("select amount,date from build where industry = '"+data[2]+"' and car_name = '"+data[0]+"'")
                    obj = cur.fetchall()
                    continue
                tmp2 = obj[0][0] - tmp
                with connection.cursor() as cur: cur.execute("update build set amount = "+str(tmp2)+" where industry = '"+data[2]+"' and car_name = '"+data[0]+"' and date = '"+str(obj[0][1])+"'")
                tmp = 0
                break
            if tmp > 0:
                return "lack of " + str(tmp) +" car"
            profit = Car.objects.get(name=data[0]).price * int(data[3])
            if update_industry(data[2],int(data[3]),table,profit):
                return "buy failed"
            with connection.cursor() as cur:
                cur.execute("select amount from buy where industry = '"+data[2]+"' and car_name = '"+data[0]+"' and date = '"+str(data[4])+"' and customer = '"+data[1]+"'")
                obj = cur.fetchall()
            if len(obj) == 0:
                m_class.objects.create(industry=Industry.objects.get(id=data[2]),car_name=Car.objects.get(name=data[0]),date=data[4],customer=Customer.objects.get(id=data[1]),amount=int(data[3]))
                obj = m_class(data[0],data[1],data[2],data[3],data[4])
                return "update success"
            else:
                obj = Buy.objects.get(industry_id=data[2],car_name=data[0],date=data[4],customer=data[1])
                obj.amount += int(data[3])
        else:
            obj = m_class(data[0],data[1],data[2],data[3],data[4])
    obj.save()
    return "update success"

def rank(table):
    attrs = []
    if table[:-1] == 'industry':
        aClass = getclass(table[:-1])
        if table[-1] == '1':
            list = aClass.objects.all().annotate(pro=Sum('profit')).order_by('-pro')
        if table[-1] == '2':
            list = aClass.objects.all().order_by('-car_in')
        if table[-1] == '3':
            list = aClass.objects.all().order_by('-car_out')
        if table[-1] == '4':
            list = aClass.objects.all().order_by('-car_remain')
        return printout(aClass,list)
    elif table[:-1] == 'car':
        aClass = getclass('buy')
        with connection.cursor() as cur:
            if table[-1] == '1':
                cur.execute("select car_name,sum(car.price*buy.amount) as profit from buy,car where car.name = buy.car_name group by(car_name) order by profit")
                attrs = ['car_name','profit']
            if table[-1] == '2':
                cur.execute("select brand,sum(car.price*buy.amount) as profit from buy,car where car.name = buy.car_name group by(brand) order by profit")
                attrs = ['brand','profit']
            if table[-1] == '3':
                cur.execute("select car_name,sum(amount) as ant from buy group by(car_name) order by ant")
                attrs = ['car_name','ant']
            if table[-1] == '4':
                cur.execute("select brand,sum(buy.amount) as ant from buy,car where car.name = buy.car_name group by(brand) order by ant")
                attrs = ['brand','ant']
            list = cur.fetchall()
            print(list)
        return printout(aClass,list,attrs)
    elif table[:-1] == 'customer':
        aClass = getclass('buy')
        with connection.cursor() as cur:
            if table[-1] == '1':
                cur.execute("select customer,sum(amount) as ant from buy group by(customer) order by ant")
                attrs = ['customer_id','ant']
            if table[-1] == '2':
                cur.execute("select customer,sum(car.price*buy.amount) as profit from buy,car where car.name = buy.car_name group by(customer) order by profit")
                attrs = ['customer_id','profit']
            list = cur.fetchall()
            print(list)
    else:
        aClass =getclass('buy')
        with connection.cursor() as cur:
            cur.execute("select car_name,sum(car.price*buy.amount) as profit from buy,car where car.name = buy.car_name group by(car_name) order by profit")
            list = cur.fetchall()
        return printout(aClass,list,['car_name','profit'])
    return printout(aClass,list,attrs)

def deldata(table,cond=None):
    aClass = getclass(table)
    if cond is not None:
        list = aClass.objects.filter(**cond)
        if list:
            tmp = printout(aClass,list)
            list.delete()
            return "del success" + tmp
        else:
            return "del failed"

def update_industry(industry_name,number,attr,profit=0):
    ind = Industry.objects.get(id=industry_name)
    if ind:
        if attr == 'build':
            ind.car_in += number
            ind.car_remain += number
        elif attr == 'buy':
            ind.car_out  += number
            ind.car_remain -= number
            ind.profit += profit
        ind.save()
        return False
    else:
        return True

def testdb(table,attr=None,cond=None):
    if table[-3:] == 'buy':
        if table[:8] == 'customer':
             cond['customer'] = Customer.objects.get(name=table[8:-3]).id
        table = table[-3:]
    aClass = getclass(table)
    list = aClass.objects.all()

    if cond is not None:
        list = aClass.objects.filter(**cond)
    return printout(aClass,list,attr)

def printout(aClass,list,attr=None):
    response = ""
    response1 = ""
    response1 += "<table border='1'><tr>"
    names2 = []
    if attr is not None:
        names = attr
    else:
        names = getattrkey(aClass,list)
    for name in names:
        if name[-3:] == '_id':
            tmp = name[:-3]
            if tmp in names:
                continue
        elif name[:3] == 'get':
            continue
        else:
            tmp = name
        response1 += '<td>' + tmp + '</td>'
        names2.append(name)
    response1 += "</tr>"
    if attr is None:
        for var in list:
            response1 += "<tr>"        
            for name in names2:
                response1 += '<td>' + str(var.__dict__[name]) + '</td>'
            response1 += "</tr>"
    else:
        for var in list:
            response1 += "<tr>"        
            for name in var:
                if attr is not None:
                    response1 += '<td>' + str(name) + '</td>'
            response1 += "</tr>"
    response = response1 + "</table>"
    return response
    # return HttpResponse("<p>" + response + "</p>")

def OLAP(classify,order,table,table2,action,attrs=None):
    aClass = getclass(table)
    sens = " "
    judge = False
    if len(attrs) != 0:
        for key,value in attrs.items():
            if judge:
                sens += " and "
            else:
                judge = True
            if key == 'day' or key == 'month' or key == 'year':
                sens += key + "(date)='"+ value + "'"
                continue
            sens += key + "='" + value +"'"
    with connection.cursor() as cur:
        if action == 'rank': 
            tmp = ''
            tmp2 = action + "ing"
        else:
            tmp = order
            tmp2 = action
        if table == table2:
            if len(attrs) != 0:
                cur.execute("with cte as (SELECT *, "+ action +"("+ tmp +") over (partition by `"+ classify +"` ORDER BY "+ order +") as "+ tmp2 +" FROM "+table+") select * from cte where"+sens)
            else:
                cur.execute("with cte as (SELECT *, "+ action +"("+ tmp +") over (partition by `"+ classify +"` ORDER BY "+ order +") as "+ tmp2 +" FROM "+table+") select * from cte")
        else:    
            if [table,table2] == ['build','car'] or [table2,table] == ['build','car']:
                sens2 = "car_name = car.name"
            elif [table,table2] == ['build','industry'] or [table2,table] == ['build','industry']:
                sens2 = "industry = ID"
            elif [table,table2] == ['buy','car'] or [table2,table] == ['buy','car']:
                sens2 = "car_name = car.name"
            elif [table,table2] == ['buy','industry'] or [table2,table] == ['buy','industry']:
                sens2 = "industry = ID"
            elif [table,table2] == ['buy','customer'] or [table2,table] == ['buy','customer']:
                sens2 = "buy.customer = ID"
            if len(attrs) != 0:
                cur.execute("with cte as (SELECT *, "+ action +"("+ tmp +") over (partition by `"+ classify +"` ORDER BY "+ order +") as "+ tmp2 +" FROM "+table+","+table2+" where "+sens2+") select * from cte where"+sens)
            else:
                cur.execute("with cte as (SELECT *, "+ action +"("+ tmp +") over (partition by `"+ classify +"` ORDER BY "+ order +") as "+ tmp2 +" FROM "+table+","+table2+" where "+sens2+") select * from cte")            
        list = cur.fetchall()
    # if table == 'car':
    #     attr = ["name","price","brand","size"]
    # elif table == 'buy':
    #     attr = ["car_name","customer","industry","amount","date"]
    # elif table == 'build':
    #     attr = ["car_name","industry","amount","date"]
    # elif table == 'industry':
    #     attr = ["id","profit","car_in","car_remain","car_out"]
    # elif table == 'customer':
    #     attr = ["id","name","sex","phone","salary"]
    # attr.append(action)
    title = [title[0] for title in cur.description]
    return printout(aClass,list,title)  

def sql(message):
    with connection.cursor() as cur:
        cur.execute(message)
    if 'select' in message:
        list = cur.fetchall()
        title = [title[0] for title in cur.description]
    # res = []
    # for item in list:
    #     res.append(dict(list(zip(title,item))))
        return printout(Base,list,title)
    else:
        return "execute success"

def cust(industry,name):
    with connection.cursor() as cur:
        cur.execute("select * from car where name='"+name+"'")
        if len(cur.fetchall()) != 0:
            cur.execute("select *from build where industry='"+industry+"' and car_name='"+name+"'")
        else:
            cur.execute("select * from car where brand='"+name+"'")
            if len(cur.fetchall()) != 0:
                cur.execute("select brand,car_name,amount,industry,date from build,car where industry='"+industry+"' and car_name = name and brand='"+name+"'")
            else:
                return "wrong name or brand"
    list = cur.fetchall()
    title = [title[0] for title in cur.description]
    return printout(Base,list,title)