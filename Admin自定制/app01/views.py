from django.shortcuts import render,HttpResponse
from app01 import models

# Create your views here.
def test(request):
    user_group_list = models.Group.objects.all()

    return render(request,'test.html',{'res':user_group_list})

def test_add(request):
    if request.method == "GET":
        return render(request,'test_add.html')
    else:
        popid = request.GET.get('popup')
        if popid:
            #通过popup新创建了一个页面进来
            title = request.POST.get('title')
            obj = models.Group.objects.create(title=title)
            #response = {'id':obj.id,'title':obj.title}
            #1.关闭popup页面
            #2.当数据添加，找到原来发送popup的页面中的对应ID标签位置，添加数据并默认显示
            return render(request,'popup_response.html',{'id':obj.id,'title':obj.title,'popid':popid})
        else:
            #正常添加，重定向回列表页面
            title = request.POST.get('title')
            models.Group.objects.create(title=title)
            return HttpResponse('重定向到列表页面：所有用户组')




