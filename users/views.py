from django.shortcuts import render , redirect

# To Use Class of Django which give Default django User creation Form
from django.contrib.auth.forms import UserCreationForm

#imoort flash message from django like debug , info ,suceess , warning , error
from django.contrib import messages


#to render template only if User is login 
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm

#to update user information and Pic
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


# Create your views here.

def register(request):

    if request.method == 'POST':

        #To use Default Form
        #form = UserCreationForm(request.POST)


        #To use Modeified Form
        form = UserRegisterForm(request.POST)

        if form.is_valid():

            form.save()  #To save the  Users
            username = form.cleaned_data.get('username')

            messages.success(request , 'Account created Now Login !')

            return redirect('login')
    else:
        #To use Default Form
       # form = UserCreationForm()

       #To use Modeified Form
       form = UserRegisterForm()

    return render(request , 'users/register.html' , {'form':form})


@login_required
def profile(request):

    #to render template only if User is login
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
