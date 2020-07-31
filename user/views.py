from django.contrib import auth, messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile
from django.views import View
from .forms import RegisterForm, LoginForm
from django import forms


# Create your views here.

# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             return HttpResponseRedirect(reverse('User:login'))
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'User/register.html', {'form': form})
#


class Register(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'user/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST.get('username')
            password = request.POST.get('password1')
            my_user = authenticate(username=username, password=password)
            login(request, my_user)
            messages.success(request, f'Tạo tài khoản thành công')
            return HttpResponseRedirect(request.path)
        return render(request, 'user/register.html', {'form': form})


# class Login(View):
#     def get(self, request):
#         form = LoginForm()
#         return render(request, 'user/login.html', {'form': form})
#
#     def post(self, request):
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             print(username)
#             my_user = authenticate(username=username, password=password)
#             if my_user is not None:
#                 login(request, my_user)
#                 a = request.POST.get('next')
#                 print(request.path)
#                 return HttpResponseRedirect(reverse('mv:home'))
#         else:
#             return render(request, 'user/login.html', {'form': form})
#         # username = form.cleaned_dat['username']
#         # password = form.cleaned_data['password']
#         # my_user = authenticate(username=username, password=password)
#         # if my_user is None:
#
#         #     return HttpResponseRedirect(reverse('mv:index'))
#         # else:
#         #     return render(request, 'user/login.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        u_form = UserUpdateForm()
        p_form = ProfileUpdateForm()
        lst_mv = request.user.modelmv_set.all()

        if request.user.last_name:
            name = request.user.last_name + ' ' + request.user.first_name
        else:
            name = request.user.username

        content = {
            'u_form': u_form,
            'p_form': p_form,
            'lst_mv': lst_mv,
            'name': name
        }
    return render(request, 'user/profile.html', content)


def mv_post_by_user(request, the_slug):
    profile = get_object_or_404(Profile, slug=the_slug)
    my_user = profile.user
    lst_mv = my_user.modelmv_set.all()
    context = {
        'profile': profile,
        'lst_mv': lst_mv
    }
    return render(request, 'user/mv_post_by_user.html', context)


def base(request):
    return render(request, 'user/base.html')
