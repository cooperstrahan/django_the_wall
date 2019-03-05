from django.shortcuts import render, redirect
from apps.app_wall.models import *
import bcrypt
from django.contrib import messages

def index(request):
    return render(request, "index.html")

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    else :
        r_user = User.objects.create(first_name = request.POST['fname'], \
            last_name = request.POST['lname'], email = request.POST['email'], \
            password = bcrypt.hashpw(request.POST['pass'].encode(), bcrypt.gensalt()))
        
        request.session['name'] = r_user.first_name
        request.session['id'] = r_user.id
        request.session['registered'] = True
    return redirect('/wall')

def login(request):
    login_errors = User.objects.login_validator(request.POST)
    if len(login_errors) > 0:
        for tag, error in login_errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        l_user = User.objects.get(email=request.POST['email'])
        request.session['name'] = l_user.first_name
        request.session['id'] = l_user.id
        request.session['logged_in'] = True  
    return redirect('/wall')

def post_message(request):
    errors = Message.objects.msg_val(request.POST)
    if len(errors) > 0:
        for tag, error in  errors.items():
            messages.error(request, error, extra_tags=tag)
    else:
        Message.objects.create( \
            user_id=User.objects.get(id=request.session['id']), \
            message=request.POST['msg'])
    return redirect('/wall')

def post_comment(request):
    errors = Message.objects.cmt_val(request.POST)
    if len(errors) > 0:
        for tag, error in  errors.items():
            messages.error(request, error, extra_tags=tag)
    else:
        Comment.objects.create( \
            user_id=User.objects.get(id=request.session['id']), \
            message_id=Message.objects.get(id=request.POST['mes']), \
            comment=request.POST['cmt'])
    return redirect('/wall')

def wall(request):
    if 'id' in request.session:
        context = {
            "message_posts": Message.objects.all(),
            "comments": Comment.objects.all(),
        }
        
        for c in Comment.objects.all():
            print(c.user_id.first_name)
            print(c.message_id.message)
            print(c.comment)
        return render(request, "wall.html", context)
    else:
        return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')