from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages

from internet_market_project import settings
from users.models import CustomUser


class RegisterView(TemplateView):
    template_name ='register.html'


class LoginView(TemplateView):
    template_name = 'login.html'


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
            email=email, password=password1,
            first_name=first_name, last_name=last_name
        )

        login(request, user)

        subject = user.first_name
        message = f'ПРИВЕТ {user.first_name}! Зачем решил зарегистрироваться? Ты че петух что ли?'

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Ошибка отправки почты: {e}")
            messages.warning(request,
                             "Вы зарегистрированы, но письмо не было отправлено.")
        return redirect('home-url')



class MakeLoginView(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password1')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home-url')
        else:
            messages.error(request, "Неверный email или пароль.")
            return redirect('login-url')



class MakeLogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('login-url')
