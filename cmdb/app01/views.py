from django.shortcuts import render,HttpResponse

# Create your views here.
def asset(request):
    if request.method == 'GET':
        return HttpResponse('姿势不对！')
    else:
        print(request.body)
        return HttpResponse('1002')

