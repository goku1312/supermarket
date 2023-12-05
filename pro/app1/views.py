from django.shortcuts import render
from app1 import dbconnect
from django.http.response import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage

# Create your views here.
def home(request):
    return render(request,'home.html')
def userhome(request):
    return render(request,'userhome.html')
def staffhome(request):
    uid=request.session['user1']
    sql="select *from stafft where name='"+uid+"'"
    d=dbconnect.selectone(sql)
    sql1="select *from frnd where zid='"+uid+"'"
    da=dbconnect.selectone(sql1)
    # user=da[2]
    sql1e="select *from frnd where zid='"+uid+"'"
    daee=dbconnect.selectall(sql1e)
    sql12="select *from stafft "
    dat=dbconnect.selectall(sql12)
    return render(request,'staffhome.html',{"data":d,"data1":da,"data2":dat,"data3":daee})
def login(request):
    if request.POST.get("sub"):
        u=request.POST.get("uname")
        p=request.POST.get("upassword")
        sql="select *from tb4 where username='"+u+"' and password='"+p+"'"
        data=dbconnect.selectone(sql)
        if data and data[3]== 'admin':
            request.session['user']=u
            return render(request,'userhome.html',{})
        elif data and data[3]== 'staff':
            request.session['user1']=u
            uid=request.session['user1']
            sql="select * from stafft where name='"+uid+"'"
            data=dbconnect.selectone(sql)
            import time
            current = time.strftime('%I:%M %p')
            import datetime
            d=datetime.date.today()
            sq11="insert into staffdata(userid,date,timein) values('"+u+"','"+str(d)+"','"+current+"')"
            dbconnect.insert(sq11)
            sql2="update stafft set logs='1' where name='"+uid+"'"
            dbconnect.insert(sql2)
            return render(request,'staffhome.html',{"data":data})
    return render(request,"sign-in.html")
def logout(request):
    return HttpResponseRedirect('home')
def cate(request):
    return render(request,"terms-conditions.html")
def stflogout(request):
    uid=request.session['user1']
    import time
    current = time.strftime('%I:%M %p')
    sq11="update staffdata set timeout='"+current+"' where timeout=''"
    dbconnect.insert(sq11)
    sql2="update stafft set logs='0' where name='"+uid+"'"
    dbconnect.insert(sql2)
    return HttpResponseRedirect("login")
def item(request):
    if request.POST.get("sub"):
        a=request.POST.get("cname")
        sql="insert into mc (categoryname) values('"+a+"')"
        dbconnect.insert(sql)
        return HttpResponseRedirect("item")
    sql1="select * from mc"
    d=dbconnect.selectall(sql1)
    return render(request,"mcategory.html",{"data":d})

def subcatergory(request):
    sql="select *from mc"
    d=dbconnect.selectall(sql)
    sql2="select *from sc"  
    data=dbconnect.selectall(sql2) 
    if request.POST.get("sub"):
        b=request.POST.get("cid")
        a=request.POST.get("sname")
        sql="insert into sc (cid,subcatergoryname) values('"+b+"','"+a+"')"
        dbconnect.insert(sql)
        return HttpResponseRedirect("subcatergory")
    return render(request,"subcatergory.html",{'data':d,'data1':data})
def delete(request):
    uid=request.GET['x']
    sql="delete from sc where sid='"+uid+"'"
    dbconnect.delete(sql)
    return HttpResponseRedirect("subcatergory")


def staff(request):
    if request.POST.get("sub"):
        n=request.POST.get("uname")
        id=request.POST.get("sid")
        e=request.POST.get("uemail")
        p=request.POST.get("upass")
        s=request.POST.get("usalary")
        d=request.POST.get("udob")
        ph=request.FILES["uimage"]
        fs=FileSystemStorage()
        fs.save("app1/static/uploads/"+ph.name,ph)
        sql="insert into stafft(name,staffid,email,password,salary,dob,image) values('"+n+"','"+id+"','"+e+"','"+p+"','"+s+"','"+d+"','"+ph.name+"')"
        d=dbconnect.insert(sql)
        sql1="insert into tb4 (username,password,utype) values('"+n+"','"+p+"','"'staff'"')"
        dbconnect.insert(sql1)
        return HttpResponseRedirect("staff")
    sq="select * from stafft"
    dat=dbconnect.selectall(sq)
    return render(request,'staff.html',{'data':dat})

def makeactivate(request):
    id=request.GET['uid']
    sql="update stafft set status='1' where id='"+id+"'"
    dbconnect.insert(sql)
    return HttpResponseRedirect('staff')
def makedeactivate(request):
    id=request.GET['uid']
    sql="update stafft set status='0' where id='"+id+"'"
    dbconnect.insert(sql)
    return HttpResponseRedirect('staff')


def reset(request):
    id=request.GET['uid']
    import random
    captcha=list('abcdefghijklmnopkrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    c=random.sample(captcha,k=5)
    c1=''
    for i in c:
        c1+=i
    sql="update stafft set password='"+c1+"' where name='"+id+"'"
    dbconnect.update(sql)
    sql1="update tb4 set password='"+c1+"' where username='"+id+"'"
    dbconnect.update(sql1)
    return HttpResponseRedirect("staff")

def leave(request):
    uid=request.session['user1']
    sql="select *from stafft where name='"+uid+"'"
    de=dbconnect.selectone(sql)
    if request.POST.get("sub"):
        n=request.POST.get("title")
        r=request.POST.get("reason")
        sd=request.POST.get("sdate")
        ed=request.POST.get("edate")
        sql="insert into ltable (name,title,reason,startdate,enddate) values('"+uid+"','"+n+"','"+r+"','"+sd+"','"+ed+"')"
        dbconnect.insert(sql)
        return HttpResponseRedirect('leave')
    sql1="select * from ltable where name='"+uid+"'"
    data=dbconnect.selectall(sql1)
    return render(request,'leave.html',{'data':data,'data1':de})



def status(request):
    
    if request.POST.get("sub"):
        n=request.POST.get("name")
        d=request.POST.get("date")

        sql="select * from staffdata where userid='"+n+"' and date='"+d+"'"
        data=dbconnect.selectall(sql)
        return render(request,"status.html",{"data":data,})
    sql1="select * from stafft"
    d=dbconnect.selectall(sql1)
    return render(request,"status.html",{"d":d})

def leavests(request):
    sql="select * from ltable where status='0'"
    d=dbconnect.selectall(sql)
    sql1="select * from ltable"
    da=dbconnect.selectall(sql1)
    return render(request,"leaveadmin.html",{"data":d,"data1":da})


def approved(request):
    x=request.GET['uid']
    sql="update ltable set status='1' where id='"+x+"'"
    dbconnect.insert(sql)
    return HttpResponseRedirect('leavests')


def denied(request):
    x=request.GET['uid']
    sql="update ltable set status='2' where id='"+x+"'"
    dbconnect.insert(sql)
    return HttpResponseRedirect('leavests')

def profile(request):
    uid=request.session['user1']
    sql="select *from stafft where name='"+uid+"'"
    d=dbconnect.selectone(sql)
    return render(request,'profile.html',{'data':d})


def imgupdate(request):
    uid=request.session['user1']
    if request.POST.get("sub"):
        ph=request.FILES["uimage"]
        fs=FileSystemStorage()
        fs.save("app1/static/uploads/"+ph.name,ph)
        sql="update stafft set image='"+ph.name+"' where name='"+uid+"'"
        dbconnect.insert(sql)
        return HttpResponseRedirect("imgupdate")
    sql2="select *from stafft where name='"+uid+"'"
    d=dbconnect.selectone(sql2)
    return render(request,"imgupdate.html",{"data":d})


def passupdate(request):
    uid=request.session['user1']
    if request.POST.get("sub"):
        p=request.POST.get("upass")
        pn=request.POST.get("unpass")
        pc=request.POST.get("ucpass")
        sql="select * from stafft where name='"+uid+"'"
        d=dbconnect.selectone(sql)
        if d[4]!=p:
            ms="you have entered wrong password"
            return render(request,"passupdate.html",{'data':ms})
        elif pn!=pc:
            mse="password doesn't match"
            return render(request,"passupdate.html",{'data1':mse})
        else:
            sql1="update stafft set password='"+pc+"' where name='"+uid+"'"
            dbconnect.insert(sql1)
            sql2="update tb4 set password='"+pc+"' where username='"+uid+"'"
            dbconnect.insert(sql2)
            mse="password succesfully changed"
            return render(request,'passupdate.html',{"data2":mse})
    return render(request,'passupdate.html')


def update(request):
    uid=request.session['user1']
    if request.POST.get("sub"):
        e=request.POST.get("uemail")
        d=request.POST.get("udob")
        sql="update stafft set email='"+e+"',dob='"+d+"' where name='"+uid+"'"
        dbconnect.insert(sql)
        return HttpResponseRedirect("update")
    sql="select *from stafft where name='"+uid+"'"
    d=dbconnect.selectone(sql)
    return render(request,'update.html',{'data':d})

def zone(request):
    uid=request.session['user1']
    sql="select *from stafft where name='"+uid+"'"
    de=dbconnect.selectone(sql)
    dyt=de[7]
    sq="select * from stafft where name not in('"+uid+"') "
    dat=dbconnect.selectall(sq)
    sql4="select * from zone "
    me=dbconnect.selectall(sql4) 
    cnt=0
    if request.POST.get("pic"):
        cnt=1
    elif request.POST.get('text'):
        cnt=0
    if request.POST.get("subt"):
        import time
        current = time.strftime('%I:%M %p')
        import datetime
        d=datetime.date.today()
        k=request.POST.get("title")
        ph=request.FILES["pic"]
        fs=FileSystemStorage()
        fs.save("app1/static/uploads/"+ph.name,ph) 
        sql7="insert into zone (name,date,time,title,pic,n,image) values('"+uid+"','"+str(d)+"','"+current+"','"+k+"','"+ph.name+"','1','"+dyt+"') "
        dbconnect.insert(sql7)
        sql0="select * from zone"
        data8=dbconnect.selectall(sql0)
        lmsgid=data8[-1][0]
        for i in dat:
            sql6="insert into dummy(msgid,name,title,status) values('"+str(lmsgid)+"','"+i[1]+"','"+k+"','0')"
            dbconnect.insert(sql6)
        return HttpResponseRedirect("zone")
    if request.POST.get("sub"):
        m=request.POST.get("msg")
        import time
        current = time.strftime('%I:%M %p')
        import datetime
        d=datetime.date.today()
        sql3="insert into zone (name,msg,date,time,count,image,n) values ('"+uid+"','"+m+"','"+str(d)+"','"+current+"','0','"+dyt+"','0')"
        dbconnect.insert(sql3)
        sql5="select * from zone"
        data5=dbconnect.selectall(sql5)
        lmsgid=data5[-1][0]
        for i in dat:
            sql6="insert into dummy(msgid,name,msg,status) values('"+str(lmsgid)+"','"+i[1]+"','"+m+"','0')"
            dbconnect.insert(sql6)
        return HttpResponseRedirect("zone")
    return render(request,'myzone.html',{'data':de,"data1":dat,"data2":me,'cnt':cnt})

def like(request):
    zid=request.GET['id']
    uid=request.session['user1']   
    sql="select *from dummy where msgid='"+zid+"' and name='"+uid+"'"
    data=dbconnect.selectone(sql)
    msgstatus=data[4]
    if int(msgstatus)==0:
        sql1="update dummy set status='1' where msgid='"+zid+"' and name='"+uid+"'"
        dbconnect.insert(sql1)
        sql2="update zone set count=count+1 where id='"+zid+"' "
        dbconnect.insert(sql2)
    return HttpResponseRedirect("zone")


def cmt(request):
    zid=request.GET['id']
    uid=request.session['user1']
    sql="select *from stafft where name='"+uid+"'"
    de=dbconnect.selectone(sql)
    dyt=de[7]
    sq="select * from stafft where name not in('"+uid+"') "
    dat=dbconnect.selectall(sq)
    sq="select * from zone where  id='"+zid+"'"
    d=dbconnect.selectone(sq)
    if request.POST.get("sub"):
        m=request.POST.get("msg")
        import time
        current = time.strftime('%I:%M %p')
        import datetime
        dd=datetime.date.today()
        sql="insert into cmt(msgid,name,comment,time,date,image) values('"+zid+"','"+uid+"','"+m+"','"+current+"','"+str(dd)+"','"+dyt+"')"
        dbconnect.insert(sql)
        return HttpResponseRedirect("cmt?id="+zid)
    sq1="select * from cmt"
    do=dbconnect.selectall(sq1)
    return render(request,'cmt.html',{'data':de,"data1":dat,"data3":d,"data4":do})


def allmsg(request):
    zid=request.GET['id']
    uid=request.session['user1']
    sql="select *from stafft where name='"+uid+"'"
    de=dbconnect.selectone(sql)
    
    sq="select * from stafft where name not in('"+uid+"') "
    dat=dbconnect.selectall(sq)
    sq11="select * from stafft where  name='"+zid+"'"
    d=dbconnect.selectone(sq11)
    if request.POST.get("frd"):
        sql="insert into frnd (zid,uid,a) values('"+zid+"','"+uid+"','1')"
        dbconnect.insert(sql)
        return HttpResponseRedirect("allmsg?id="+zid)

    return render(request,'allmsg.html',{'data':de,"data1":dat,"data7":d})

def friendmsg(request):
    zid=request.GET['id']
    uid=request.session['user1']
    sql="select *from stafft where name='"+uid+"'"
    de=dbconnect.selectone(sql)
    dyt=de[7]
    sql1="select *from stafft where name='"+zid+"'"
    dee=dbconnect.selectone(sql1)
    if request.POST.get("sub"):
        m=request.POST.get("msg")
        import time
        current = time.strftime('%I:%M %p')
        import datetime
        dd=datetime.date.today()
        sql="insert into fmsg(msgid,name,msg,time,date,image) values('"+zid+"','"+uid+"','"+m+"','"+current+"','"+str(dd)+"','"+dyt+"')"
        dbconnect.insert(sql)
        return HttpResponseRedirect("friendmsg?id="+zid)
    sq1="select * from fmsg"
    do=dbconnect.selectall(sq1)
   
    
    return render(request,'friendmsg.html',{"data":de,"data1":dee,"data4":do})




def blank(request): 
    return render(request,"blank.html")










   