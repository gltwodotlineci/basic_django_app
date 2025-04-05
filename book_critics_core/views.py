from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomUser, Ticket, Review, UserFollows
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


def home(request):
    if request.user.is_authenticated:
        return redirect('profile')
    return render(request, 'base/home.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('profile')

    return render(request, 'acces/signup.html')


def inscription(request):# inscription avec formulaire
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
def send_followers_list(actual_usr: CustomUser)-> list[str]:
    followers_obj = actual_usr.following.all()
    followed_usr_lst = CustomUser.objects.filter(pk__in=followers_obj.values_list(
        'followed_user', flat=True))

    return followed_usr_lst


@login_required(login_url='http://localhost:8000')
def all_users(request):
    actual_user = request.user
    users = CustomUser.objects.all()

    try:
        followed_user_lst = send_followers_list(actual_user)
    except UserFollows.DoesNotExist:
        followed_user_lst = []

    return render(request, 'profile/all_users.html',
                  context={'users': users,
                           'actual_user': actual_user,
                           'followed_user': followed_user_lst
                           },
                  )

@login_required(login_url='http://localhost:8000')
def show_profile(request):   
    user = request.user
    followed_users = UserFollows.objects.filter(user=user)
    followers = UserFollows.objects.filter(followed_user=user)
    followed_user_lst = []
    followers_lst = []
    # Get the list of followed users
    for followed_user in followed_users:
        followed_user_lst.append(followed_user.followed_user)

    # Get the list of followers
    for follower in followers:
        followers_lst.append(follower.user)

    return render(request, 'profile/show.html',
                  context={'user': user,
                           'followed_user': followed_user_lst,
                           "followers": followers_lst
                           }
                  )


# Show all spcecific user
@login_required(login_url='http://localhost:8000')
def other_profile(request, user_id):

    try:
        other_user = CustomUser.objects.get(uuid=user_id)
        actual_user = request.user
    except CustomUser.DoesNotExist:
        return render(request, 'base/home.html', context={'error': 'Cet utilisateur n\'existe pas'})    

    followed_users = UserFollows.objects.filter(user=other_user)
    followers = UserFollows.objects.filter(followed_user=other_user)
    followed_user_lst = []
    followers_lst = []
    # Get the list of followed users
    for followed_user in followed_users:
        followed_user_lst.append(followed_user.followed_user.username)

    # Get the list of followers
    for follower in followers:
        followers_lst.append(follower.user.username)

    return render(request, 'profile/show.html',
                  context={'user': other_user,
                           'followed_user': followed_user_lst,
                           "followers": followers_lst,
                           'actual_user': actual_user
                           })


@login_required(login_url='http://localhost:8000')
def follow_user(request):
    # Check if user you want to follow exists
    data = request.POST
    user_id = data.get('user_id')
    # Actual user
    actual_user = request.user
    users = CustomUser.objects.all()
    try:
        user_follow = CustomUser.objects.get(uuid=user_id)
        UserFollows.objects.create(user=actual_user,
                                    followed_user=user_follow)
        
        followed_user_lst = send_followers_list(actual_user)
        
        return render(request, 'profile/all_users.html',
                    context={'users': users,
                             'actual_user': actual_user,
                             'followed_user': followed_user_lst
                            }
                        )
    
    except CustomUser.DoesNotExist:
        followed_user_lst = []
        users = CustomUser.objects.all()
        return render(request, 'profile/all_users.html',
                    context={'error': 'Error: this user does not exist',
                            'users': users,
                            'followed_user': followed_user_lst
                            }
                        )


# unfollow an actual user
@login_required(login_url='http://localhost:8000')
def unfollow_user(request):
    actual_user = request.user
    data = request.POST
    followed = data.get('user_id')

    followed_user = UserFollows.objects.filter(
        user=actual_user,
        followed_user=followed
    )
    followed_user.delete()
    users = CustomUser.objects.all()
    try:
        followed_user_lst = send_followers_list(actual_user)
    except UserFollows.DoesNotExist:
        followed_user_lst = []
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


@login_required(login_url='http://localhost:8000')
def ticket(request):
    user = request.user
    return render(request, 'tickets/ticket.html',
                  context={'user': user}
                  )

@login_required(login_url='http://localhost:8000')
def create_ticket(request):
    user = request.user
    data = request.POST
    title = data.get('title')

    # Creating the ticket
    Ticket.objects.create(user=user, title=title)
    tickets = Ticket.objects.all().order_by('-time_created')
    return render(request, 'tickets/all_tickets.html',
                  context={'tickets': tickets}
                  )


@login_required(login_url='http://localhost:8000')
def all_tickets(request):
    tickets = Ticket.objects.all().order_by('-time_created')

    return render(request, 'tickets/all_tickets.html',
                  context={'tickets': tickets}
                  )


@login_required(login_url='http://localhost:8000')
def my_tickets(request):
    user = request.user
    tickets = Ticket.objects.filter(user=user).order_by('-time_created')

    return render(request, 'tickets/all_tickets.html',
                  context={'tickets': tickets}
                  )


@login_required(login_url='http://localhost:8000')
def create_review(request, ticket_id):
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


@login_required(login_url='http://localhost:8000')
def create_review(request):
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
