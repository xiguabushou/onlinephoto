from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import Users,CustomUser
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse
from PIL import Image
import time,os

def index(request):
    return render(request,"myapp/index.html")

#分页浏览图库
def photoindex(request,pIndex):
    kw = request.GET.get("keyword",None)
    mywhere = ""
    if kw is not None:
        ilist = Users.objects.filter(title__contains=kw)
        mywhere = "?keyword=%s"%(kw)
    else:
        ilist = Users.objects.all()
    p = Paginator(ilist,6)
    if pIndex < 1:
        pIndex = 1
    if pIndex > p.num_pages:
        pIndex = p.num_pages
    plist = p.page(pIndex)
    context = {"userslist":plist,"pIndex":pIndex,"rlist":p.page_range,"mywhere":mywhere,"kw":kw,"all":p.num_pages}
    return render(request,"myapp/photoindex.html",context)

#上传
def upload(request):
    return render(request,"myapp/upload.html")

#执行上传
def doupload(request):
    myfile = request.FILES.get("pic",None)
    if not myfile:
        context = {"info":"上传失败"}
        return render(request,"myapp/info.html",context)
    filename = str(time.time())+"."+myfile.name.split('.').pop()
    destination = open("./static/pic/"+filename,"wb+")
    for chunk in myfile.chunks():      # 分块写入文件  
        destination.write(chunk)  
    destination.close()

    # 执行图片缩放
    im = Image.open("./static/pic/"+filename)
    # 缩放到75*75(缩放后的宽高比例不变):
    im.thumbnail((150, 150))
    # 把缩放后的图像用jpeg格式保存: 
    im.save("./static/pic/S_"+filename,None)

    ob = Users()
    ob.title = request.POST['title']
    ob.photoname = filename
    ob.save()
    return redirect(reverse('photoindex', kwargs={'pIndex': 1}))

#删除图片
def delphoto(request,uid=0):
    try:
        ob = Users.objects.get(id=uid)
        if os.path.exists("./static/pic/"+ob.photoname):
            os.remove("./static/pic/"+ob.photoname)
        if os.path.exists("./static/pic/S_"+ob.photoname):
            os.remove("./static/pic/S_"+ob.photoname)
        ob.delete()
        return redirect(reverse('photoindex', kwargs={'pIndex': 1}))
    except:
        context = {"info":"删除失败"}
        return render(request,"myapp/info.html",context)
    
#加载编辑页面
def editpage(request,uid=0):
    ob = Users.objects.get(id=uid)
    context = {"user":ob}
    return render(request,"myapp/editpage.html",context)

#执行修改
def doedit(request,uid=0):
    try:
        ob = Users.objects.get(id=uid)
        ob.title = request.POST['title']

        #获取图片
        myfile = request.FILES.get("mypic",None)
        #检测是否上传了图片
        if myfile:
            #删除原图片
            if os.path.exists("./static/pic/"+ob.photoname):
                os.remove("./static/pic/"+ob.photoname)
            if os.path.exists("./static/pic/S_"+ob.photoname):
                os.remove("./static/pic/S_"+ob.photoname)
            filename = str(time.time())+"."+myfile.name.split('.').pop()
            ob.photoname = filename
            # 分块写入文件  
            destination = open("./static/pic/"+filename,"wb+")
            for chunk in myfile.chunks():
                destination.write(chunk) 
            destination.close()

            # 执行图片缩放
            im = Image.open("./static/pic/"+filename)
            # 缩放到75*75(缩放后的宽高比例不变):
            im.thumbnail((150, 150))
            # 把缩放后的图像用jpeg格式保存: 
            im.save("./static/pic/S_"+filename,None)

        ob.save()
        return redirect(reverse('photoindex', kwargs={'pIndex': 1}))
    except:
        context = {"info":"操作失败"}
        return render(request,"myapp/info.html",context)
    
def login(request):
    return render(request,"myapp/login.html")

def dologin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = CustomUser.objects.get(username=username, password=password)
            # 这里应该使用密码哈希进行比较，而不是明文密码
            request.session['user_id'] = user.id
            request.session.set_expiry(600)
            return redirect(reverse('photoindex', kwargs={'pIndex': 1}))
        except:
            return HttpResponse('<script>alert("账号或密码错误");location.href="/login/";</script>')
