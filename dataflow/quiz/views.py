from django.shortcuts import redirect,render, HttpResponseRedirect
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .models import issues_register
from django.core.mail import send_mail
from .models import Register
from django.conf import settings
import pandas as pd
import csv
from django.http import HttpResponse


# 1st method login and siginup
# django auth user concept login and signup method if you check this code pls uncommet and url verify then it's work proper

# def sign_up(request):
#  if request.method == "POST":
#   fm = SignUpForm(request.POST)
#   if fm.is_valid():
#    messages.success(request, 'Account Created Successfully !!') 
#    fm.save()
#  else: 
#   fm = SignUpForm()
#  return render(request, 'signup.html', {'form':fm})


# def user_login(request):
#   if not request.user.is_authenticated:
#     if request.method == "POST":
#       fm = AuthenticationForm(request=request, data=request.POST)
#       if fm.is_valid():
#         uname = fm.cleaned_data['username']
#         upass = fm.cleaned_data['password']
#         user = authenticate(username=uname, password=upass)
#         if user is not None:
#           login(request, user)
#           messages.success(request, 'Logged in successfully !!')
#           return HttpResponseRedirect('/dashboard/')
#     else: 
#       fm = AuthenticationForm()
#     return render(request, 'userlogin.html', {'form':fm})
#   else:
#     return HttpResponseRedirect('/dashboard/')


def dashboard(request):
    if 'email' in request.session:
        if request.method == "POST":
            Name = request.POST.get('Name')
            Issues = request.POST.get('Issues')
            Comments = request.POST.get('Comments')
            Image = request.FILES.get('Image')
            Gender = request.POST.get('Gender')
            email = Register.objects.get(email=request.session['email'])
            data = issues_register(
                name = Name,
                issues = Issues,
                comments = Comments,
                issues_image = Image,
                gender = Gender
            )
            data.save()
            return redirect('/sent_email/'+str(email)+'/')
        else:
            try:
                row = issues_register.objects.all()
            except:
                row=None
            return render(request, 'dashboard.html',{'row':row})
    else:
        return redirect('/custome_login/')
 

def user_logout(request):
	if request.method == 'GET':
		request.session.flush()
		return redirect('/custome_login/')


def issues_register_update(request,id):
    if request.method == "POST":
        Name = request.POST.get('Name')
        Issues = request.POST.get('Issues')
        Comments = request.POST.get('Comments')
        Image = request.FILES.get('Image')
        Gender = request.POST.get('Gender')
        data = issues_register.objects.get(id=id)
        data.name = Name
        data.issues = Issues
        data.comments = Comments
        data.issues_image = Image
        data.gender = Gender
        data.save()
        return redirect('/dashboard/')
    else:
        row = issues_register.objects.get(id=id)
        return render(request, 'update.html',{'row':row})

# after save recieve email
def sent_email(request,email):
		subject = 'welcome to dataflowgroup'
		message = f' welcome to dataflowgroup'
		email_from = settings.EMAIL_HOST_USER
		recipient_list = [email]
		send_mail( subject, message, email_from, recipient_list )
		return redirect('/dashboard/')
    
# all data extract in csv 
def download(request):
    data = issues_register.objects.all().values_list('name', 'issues', 'issues_image', 'comments','gender')
    issue_df = pd.DataFrame(list(data))
    issue_df.to_csv('file.csv', index=False)
    with open('file.csv') as myfile:
        response = HttpResponse(myfile, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=file.csv'
        return response
    
    
# 2nd method login and siginup
# custome user login and register
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        data = Register(
            name=name,
            email=email,
            gender=gender,
            password=password,
        )
        data.save()
        messages.success(request, 'account is Register Succesfully!!!!')
        return render(request, 'customelogin.html')
    else:
        return render(request, 'register.html')


def custome_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            data = Register.objects.get(email=email,password=password)
            request.session['email'] = email
            return redirect('/dashboard/',{'data':data})
        except:
            messages.success(request, 'Password or Username is incorrect!!!')
            return redirect('/custome_login/')
    else:
        return render(request, 'customelogin.html')