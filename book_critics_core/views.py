from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomUser, Ticket, Review, UserFollows
from django.contrib.auth import login, logout


def home(request):
    if request.user.is_authenticated:
        return redirect('profile')
    return render(request, 'base/home.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('profile')

    return render(request, 'acces/signup.html')


def inscirption(request):
    data = request.POST
    username = data.get('username')
    password = data.get('password')
    password2 = data.get('confirm_password')
    email = data.get('email')
    
    # Verifying the password or the user existence
    try:
        if CustomUser.objects.get(username=username):
            return render(request, 'acces/signup.html', context={'error': 'Cet utilisateur existe déjà'})
    except CustomUser.DoesNotExist:
        if password != password2:
            return render(request, 'acces/signup.html', context={'error': 'Les mots de passe ne correspondent pas'})

    user = CustomUser.objects.create_user(username=username, password=password, email=email)

    context = {'user': user}
    return render(request, 'profile/show.html', context=context)


# sending followers list
def send_followers_list(followed_usr_lst: list, actual_usr)-> list:
    followed_usr_obj = UserFollows.objects.filter(
        user=actual_usr)
    for followed_user in followed_usr_obj:
        followed_usr_lst.append(followed_user.followed_user.username)

    return followed_usr_lst

def all_users(request):
    # Check if the user is signed in
    if request.user.is_anonymous:
        return redirect('signup')
    
    actual_user = request.user
    users = CustomUser.objects.all()

    followed_user_lst = []
    try:
        followed_user_lst = send_followers_list(followed_user_lst, actual_user)
    except UserFollows.DoesNotExist:
        followed_user = None


    return render(request, 'profile/all_users.html',
                  context={'users': users,
                           'actual_user': actual_user,
                           'followed_user': followed_user_lst
                           },
                  )


def show_profile(request):
    # Check if the user is signed in
    if request.user.is_anonymous:
        return redirect('signup')
    
    user = request.user

    return render(request, 'profile/show.html',
                  context={'user': user}
                  )


def follow_user(request):
    # Check if the user is signed in
    if request.user.is_anonymous:
        return redirect('signup')

    # Check if user you want to follow exists
    data = request.POST
    user_id = data.get('user_id')
    # Actual user
    actual_user = request.user
    users = CustomUser.objects.all()
    followed_user_lst = []
    try:
        user_follow = CustomUser.objects.get(uuid=user_id)
        UserFollows.objects.create(user=actual_user,
                                    followed_user=user_follow)
        
        followed_user_lst = send_followers_list(followed_user_lst, actual_user)
        
        return render(request, 'profile/all_users.html',
                    context={'users': users,
                             'actual_user': actual_user,
                             'followed_user': followed_user_lst
                            }
                        )
    
    except CustomUser.DoesNotExist:
        users = CustomUser.objects.all()
        return render(request, 'profile/all_users.html',
                    context={'error': 'Error: this user does not exist',
                            'users': users,
                            'followed_user': followed_user_lst
                            }
                        )

# unfollow an actual user
def unfollow_user(request):
    # Check if the user is signed in
    if request.user.is_anonymous:
        return redirect('signup')
    actual_user = request.user
    data = request.POST
    followed = data.get('user_id')

    followed_user = UserFollows.objects.filter(
        user=actual_user,
        followed_user=followed
    )
    followed_user.delete()
    users = CustomUser.objects.all()
    followed_user_lst = []
    try:
        followed_user_lst = send_followers_list(followed_user_lst, actual_user)
    except UserFollows.DoesNotExist:
        followed_user = None
    return render(request, 'profile/all_users.html',
                    context={'users': users,
                             'actual_user': actual_user,
                             'followed_user': followed_user_lst
                            }
                )


# Login user
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

def ticket(request):
    # Check if the user is signed in
    if request.user.is_anonymous:
        return redirect('signup')
    user = request.user
    return render(request, 'tickets/ticket.html',
                  context={'user': user}
                  )

def create_ticket(request):
    # Check if the user is signed in
    if request.user.is_anonymous:
        return redirect('signup')
    
    user = request.user
    data = request.POST
    title = data.get('title')

    # Creating the ticket
    Ticket.objects.create(user=user, title=title)
    tickets = Ticket.objects.all().order_by('-time_created')
    return render(request, 'tickets/all_tickets.html',
                  context={'tickets': tickets}
                  )

def all_tickets(request):
    # Check if the user is signed in
    if request.user.is_anonymous:
        return redirect('signup')
    
    tickets = Ticket.objects.all().order_by('-time_created')
    
    for ticket in tickets:
        print("Ticket --- ", ticket.review.all())

    return render(request, 'tickets/all_tickets.html',
                  context={'tickets': tickets}
                  )


def create_review(request, ticket_id):
    # Check if the user is signed in
    if request.user.is_anonymous:
        return redirect('signup')
    
    ticket = get_object_or_404(Ticket, uuid=ticket_id)
    
    data = request.POST
    # rating = data.get('rating')
    headline = data.get('headline')
    body = data.get('body')

    # Creating the review
    review = Review.objects.create(user=request.user,
                                   ticket=ticket,
                                   headline=headline,
                                   body=body
                                   )
    
    return render(request, 'tickets/review.html',
                  context={'ticket': ticket,'review': review}
                  )


def create_review(request):
    if request.user.is_anonymous:
        return redirect('signup')
    user = request.user
    data = request.POST
    ticket_id = data.get('ticket_id')
    headline_review = data.get('headline-review')
    body_review = data.get('content-review')
    rating = data.get('rating')
    try:
        ticket = Ticket.objects.get(uuid=ticket_id)
        review = Review.objects.create(user=user,
                                       ticket=ticket,
                                       headline=headline_review,
                                       body=body_review,
                                       rating=rating)
        return render(request, 'tickets/all_tickets.html',
                      context={'ticket': ticket,
                              'review': review,
                              }
                      )
    except Ticket.DoesNotExist:
        return render(request, 'tickets/all_tickets.html',
                      context={'error': 'Ce billet n\'existe pas'}
                      )
