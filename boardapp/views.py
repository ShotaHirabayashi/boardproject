from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from .models import BoardModel
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.generic import CreateView
from django.urls import reverse_lazy
# Create your views here.



def signupfunc(request):
    if request.method == 'POST':
        #nameと一致
        username2 =  request.POST['username']
        password2 =  request.POST['password']
        try:
            User.objects.get(username = username2)
            return render(request, 'signup.html',{"error":"このユーザは存在します"})
        except:
            user = User.objects.create_user(username2,'',password2)
            return render(request , 'signup.html',{'some':100})
    return render(request , 'signup.html',{'some':100})


def loginfunc(request):
    if request.method == 'POST':
    #nameと一致
        username2 =  request.POST['username']
        password2 =  request.POST['password']
        user = authenticate(request, username=username2,password = password2)
        if user is not None:
            login(request,user)
            return redirect('list')
        else:
            return redirect('login')
    return render(request, 'login.html')

    #render
    # 返すhtmlは引数のもの
    # urlは再度リクエストしない
    #引数あるの注意

    # redirect
    # urlを再度読み込んでくれる

@login_required
def listfunc(request):
    object_list = BoardModel.objects.all()
    return render(request,'list.html',{'object_list':object_list})


def logoutfunc(request):
    logout(request)
    return redirect('login')
    # Redirect to a success page.


def detailfunc(request,pk):
    object = BoardModel.objects.get(pk=pk)
    return render(request,'detail.html',{'object':object})

def goodfunc(request,pk):
    post = BoardModel.objects.get(pk=pk)
    post.good = post.good + 1
    post.save()
    return redirect('list')


def readfunc(request,pk):
    post = BoardModel.objects.get(pk=pk)
    post2 = request.user.get_username()
    if post2 in post.readtext:
        return redirect('list')
    else:
        post.read +=1
        post.readtext = post.readtext + ' '+post2
        return redirect('list')


class BoardCreate(CreateView):
    model = BoardModel
    template_name = "create.html"
    fields = ("title","content","author","images")
    success_url = reverse_lazy('list')



