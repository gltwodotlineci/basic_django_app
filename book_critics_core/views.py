from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomUser
from django.contrib.auth import login, logout

def home(request):
    return render(request, 'base/home.html')


def signup(request):
    return render(request, 'acces/signup.html')

def inscirption(request):
    data = request.POST
    username = data.get('username')
    password = data.get('password')
    pasword2 = data.get('confirm_password')
    
    # Verifying the password or the user existence
    try:
        user = CustomUser.objects.get(username=username)
        if user:
            return render(request, 'acces/signup.html', context={'error': 'Cet utilisateur existe déjà'})
    except CustomUser.DoesNotExist:
        if password != pasword2:
            return render(request, 'acces/signup.html', context={'error': 'Les mots de passe ne correspondent pas'})

    user = CustomUser.objects.create_user(username=username, password=password)

    context = {'user': user}
    return render(request, 'profile/show.html', context=context)


def show_profile(request, user_id):
    # Check if the user is signed in
    if request.user.is_anonymous:
        return redirect('signup')
    
    user = get_object_or_404(CustomUser, uuid=user_id)

    return render(request, 'profile/show.html',
                  context={'user': user}
                  )

def login_user(request):
    data = request.POST
    username = data.get('username')
    password = data.get('password')
    try:
        user = CustomUser.objects.get(username=username)
        if user.check_password(password):
            login(request, user)
            return render(request, 'profile/show.html',
                           context={'user': user})
        
        return render(request, 'base/home.html', context={'error': 'Mot de passe incorrect'})
    
    except CustomUser.DoesNotExist:
        return render(request, 'acces/login.html', context={'error': 'Cet utilisateur n\'existe pas'})
    
    return render(request, 'acces/login.html')


def logout_user(request):
    logout(request)
    return redirect("home")
