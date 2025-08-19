from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
from users.models import CustomUser


class RegisterView(TemplateView):
    template_name ='register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home-url')
        return super().dispatch(request, *args, **kwargs)



class LoginView(TemplateView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home-url')
        return super().dispatch(request, *args, **kwargs)



class MakeRegisterView(View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        password1 = data['password1']
        password2 = data['password2']

        if password1 != password2:
            messages.error(request, "Пароли не совпадают.")
            return redirect('register-url')

        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request,
                        "Пользователь с таким email уже существует."
                           )
            return redirect('register-url')

        user = CustomUser.objects.create_user(
            email=email, password1=password1,
            first_name=first_name, last_name=last_name
        )

        login(request, user)
        return redirect('home-url')



class MakeLoginView(View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        email = data.get('email')
        password1 = data.get('password1')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "Неверный email или пароль.")
            return redirect('login-url')

        if user.check_password(password1):
            login(request, user)
            return redirect('home-url')
        else:
            messages.error(request, "Неверный email или пароль.")
            return redirect('login-url')



class MakeLogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('login-url')
