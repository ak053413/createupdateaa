from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .forms import SignUpForm, LoginForm, UpdateForm2, UpdateUser
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

def home(request):
    return render(request, 'blog/home.html')

# dashboard
def dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        full_name = user.get_full_name()
        if Profile.objects.filter(user_id=user.pk):
            profile = Profile.objects.get(user_id=user.pk)
        else:    
            profile = None    
        return render(request, 'blog/dashboard.html', {'user':user, 'full_name':full_name, 'profile':profile})
    else:
        return HttpResponseRedirect('/login/')

# logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# signup
def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Congratulation!!')
            return HttpResponseRedirect('/login/')          
    else:        
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form':form})

# login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request,data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in Successfully !!')
                if not Profile.objects.filter(user_id=request.user.id):
                    request.session['u'] = 0
                    return HttpResponseRedirect('/updatepage2/{}/'.format(request.user.id))
                else:
                    return HttpResponseRedirect('/dashboard/')
        else:        
            form = LoginForm()
        return render(request, 'blog/login.html', {'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')       
    
# Update User
def update_user(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = User.objects.get(pk=id)
            form = UpdateUser(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                request.session['u'] = 1
                return HttpResponseRedirect('/updatepage2/{}/'.format(request.user.id))
        else:
            pi = User.objects.get(pk=id)
            form = UpdateUser(instance=pi)
        return render(request, 'blog/updatepost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')     
        
def update_page2(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Profile.objects.get(user_id=id)
            form = UpdateForm2(request.POST, request.FILES, instance=pi)
            if form.is_valid():
                form.save()
                if request.session['u'] == 0:
                    messages.success(request, 'Final Submit is Successfully !!')
                elif request.session['u'] == 1:
                    messages.success(request, 'Updation is Successful !!')   
                return HttpResponseRedirect('/dashboard/')
        else:
            if not Profile.objects.filter(user_id=id):
                Profile.objects.create(user_id=request.user.id)
            pi = Profile.objects.get(user_id=id)
            form = UpdateForm2(instance=pi)
        return render(request, 'blog/updatepost2.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')          