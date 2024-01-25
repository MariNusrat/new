from django.shortcuts import render, redirect
from django.contrib.auth import logout

from django.http import HttpResponseRedirect
from django.urls import reverse

from myfinal.models import MyRegistrations


from datetime import datetime  
import random
import array


def index(request):
    return render(request, 'index.html')

def UserRegister(request):
    if request.method == 'POST':
        name        = request.POST.get('name')
        email       = request.POST.get('email')
        password    = request.POST.get('password')
        password1   = request.POST.get('password1')
        phone       = request.POST.get('phone')
        city        = request.POST.get('city')
        checkEmail  = MyRegistrations.objects.filter(email=email).count()
        if checkEmail == 0:
            if password == password1:
                account     = MyRegistrations(name=name, email=email, password=password, phone=phone, city=city, role='user')
                account.save()
                message = 'Your Account Has Been Created.'
            else:
                 message = 'Your password did not matched.'
        else:
            message = 'Email is Already Taken.'
        return render(request, 'register.html', {'message': message})
    else:
        return render(request, 'register.html')



def AdminRegister(request):
    if request.method == 'POST':
        name        = request.POST.get('name')
        email       = request.POST.get('email')
        password    = request.POST.get('password')
        password1   = request.POST.get('password1')
        phone       = request.POST.get('phone')
        city        = request.POST.get('city')
        checkEmail  = MyRegistrations.objects.filter(email=email).count()
        if checkEmail == 0:
            if password == password1:
                account     = MyRegistrations(name=name, email=email, password=password, phone=phone, city=city, role='admin')
                account.save()
                message = 'Admin Account Has Been Created.'
            else:
                 message = 'Admin password did not matched.'
        else:
            message = 'Email is Already Taken.'
        return render(request, 'adminregister.html', {'message': message})
    else:
        return render(request, 'adminregister.html')


def UserLogin(request):
    if request.method == 'POST':
        email       = request.POST.get('email')
        password    = request.POST.get('password')
        checkUser   = MyRegistrations.objects.only().filter(email=email, password=password).count()
        if email == 0:
            message = 'Email or Password is Not Found.'
        else:
            query    = MyRegistrations.objects.only().filter(email=email, password=password).values_list('role', 'id')
            user_role     = query[0][0]
            user_id       = query[0][1]
            request.session['user_id']   = user_id
            request.session['user_role'] = user_role
            return redirect('Account')
        return render(request, 'login.html', {'message': message})
    else:
        return render(request, 'login.html')



def Account(request):
    if 'user_id' in request.session:
        user_id     = request.session['user_id'] 
        user_role   = request.session['user_role']
        query       = MyRegistrations.objects.only().filter(id=user_id)
        return render(request, 'account.html', {'id': user_id, 'role': user_role, 'profile': query})
    else:
        return redirect('Logout')


def AddMember(request):
    if 'user_id' in request.session and request.session['user_role'] == 'admin':
        user_id     = request.session['user_id'] 
        user_role   = request.session['user_role']
        if request.method == 'POST':
            name        = request.POST.get('name')
            email       = request.POST.get('email')
            password    = request.POST.get('password')
            phone       = request.POST.get('phone')
            city        = request.POST.get('city')
            role        = request.POST.get('role')
            checkEmail  = MyRegistrations.objects.filter(email=email).count()
            if checkEmail == 0:
                account     = MyRegistrations(name=name, email=email, password=password, phone=phone, city=city, role=role)
                account.save()
                message = 'Account Has Been Created.'
            else:
                message = 'Email is Already Taken.'
            return render(request, 'AddMember.html', {'id': user_id, 'role': user_role, 'message': message})
        return render(request, 'AddMember.html', {'id': user_id, 'role': user_role})
    else:
        return redirect('Logout')


def AllMembers(request):
    if 'user_id' in request.session and request.session['user_role'] == 'admin':
        user_id     = request.session['user_id'] 
        user_role   = request.session['user_role']
        members     = MyRegistrations.objects.all().exclude(role='admin')
        return render(request, 'AllMembers.html', {'id': user_id, 'role': user_role, 'members': members})
    else:
        return redirect('Logout')
        

def MemberEdit(request):
    if 'user_id' in request.session and request.session['user_role'] == 'admin':
        user_id     = request.session['user_id'] 
        user_role   = request.session['user_role']
        if request.POST.get('edit'):
            edit_id     = request.POST.get('edit_id')
            query       = MyRegistrations.objects.only().filter(id=edit_id)
            return render(request, 'MemberEdit.html', {'id': user_id, 'role': user_role, 'profile': query})
        if request.POST.get('submit'):
            member_id   = request.POST.get('member_id')
            name        = request.POST.get('name')
            email       = request.POST.get('email')
            password    = request.POST.get('password')
            phone       = request.POST.get('phone')
            city        = request.POST.get('city')
            role        = request.POST.get('role')
            query       = MyRegistrations.objects.only().get(id=member_id)
            query.name      = name 
            query.email     = email 
            query.password  = password 
            query.phone     = phone 
            query.city      = city 
            query.role      = role 
            query.save()
        return redirect('AllMembers')
    else:
        return redirect('Logout')


def MemberDelete(request):
    if 'user_id' in request.session and request.session['user_role'] == 'admin':
        user_id     = request.session['user_id'] 
        user_role   = request.session['user_role']
        if request.POST.get('delete'):
            delete_id = request.POST.get('delete_id')
            query       = MyRegistrations.objects.only().filter(id=delete_id)
            query.delete()
        return redirect('AllMembers')
    else:
        return redirect('Logout')




def Logout(request):
    if 'user_id' in request.session:
        # del request.session['user_id']
        # del request.session['user_role']
        # request.session.delete()

        logout(request)
        return redirect('UserLogin')
    else:
        return redirect('UserLogin')


    