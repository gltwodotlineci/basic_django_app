from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from .models import CustomUser, Ticket, Review, UserFollows
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignupForm, TicketForm, ReviewForm
from django.db.models import Q
from itertools import chain


def home(request):
    if request.user.is_authenticated:
        return redirect('profile')

    login_form = LoginForm(request.POST or None)

    return render(request, 'base/home.html',
                  context={'form': login_form})


# Login user
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = CustomUser.objects.get(username=username)
            login(request, user)
            followed_user = user.following.all()
            followers = user.followed_user.all()

            return render(request, 'users/show.html',
                          context={'user': user,
                                   'followed_user': followed_user,
                                   "followers": followers})

    form = LoginForm(request.POST or None)
    return render(request, 'base/home.html',
                  context={'form': form,
                           'user': request.user
                           }
                  )


# Inscription page
def signup(request):
    if request.user.is_authenticated:
        return redirect('profile')

    signup_form = SignupForm(request.POST or None)
    return render(request, 'acces/signup.html',
                  context={'signup_form': signup_form}
                  )


def inscription(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = CustomUser.objects.create_user(username=username,
                                                  email=email,
                                                  password=password)

            login(request, user)
            context = {'user': user}
            return render(request, 'users/show.html', context=context)

    form = SignupForm(request.POST or None)
    return render(request, 'acces/signup.html',
                  context={'signup_form': form}
                  )


# Logout user
def logout_user(request):
    logout(request)
    return redirect("home")


# sending followers list
def send_followers_list(actual_usr: CustomUser) -> QuerySet:
    followers_obj = actual_usr.following.all()
    foll_usr_lst = CustomUser.objects.filter(pk__in=followers_obj.values_list(
        'followed_user', flat=True))

    return foll_usr_lst


def refacto_followers(user: CustomUser) -> tuple:
    follower_users = user.following.all()
    following_lst = [u.followed_user for u in follower_users]
    followers = user.followed_user.all

    return follower_users, following_lst, followers


@login_required(login_url='http://localhost:8000')
def all_users(request):
    actual_user = request.user
    followed_users, following_lst, followers = refacto_followers(actual_user)

    return render(request, 'users/all_users.html',
                  {
                    'follow_users': followed_users,
                    'followers': followers,
                    'following_lst': following_lst
                  }
                  )


@login_required(login_url='http://localhost:8000')
def show_profile(request):
    user = request.user
    # Followed and follower
    followed_user = user.following.all()
    followers = user.followed_user.all()

    return render(request, 'users/show.html',
                  context={'user': user,
                           'followed_user': followed_user,
                           "followers": followers
                           }
                  )


# Searching user by initials
@login_required(login_url='http://localhost:8000')
def search_user(request):
    actual_user = request.user
    followed_users, following_lst, followers = refacto_followers(actual_user)

    check_follow_lst = [us.followed_user for us in followed_users]
    find_msg = "The person(s) we found are"
    users = None
    if request.method == 'POST':
        name_initial = request.POST.get('init-username')
        if len(name_initial) < 2:
            find_msg = "Please enter an initial with at least 2 characters"
        else:
            usr = CustomUser.objects.all()
            users0 = usr.filter(username__istartswith=name_initial)
            users = users0.exclude(uuid=actual_user.pk)
            if not users0.exists():
                find_msg = f"No user found with the initial '{name_initial}'"

        return render(request, 'users/all_users.html',
                      context={'users': users,
                               'follow_users': followed_users,
                               'actual_user': actual_user,
                               'followers': followers,
                               'name_initial': name_initial,
                               'check_follow': check_follow_lst,
                               'following_lst': following_lst,
                               'find_msg': find_msg
                               })

    return redirect('all_users')


# Show all spcecific user
@login_required(login_url='http://localhost:8000')
def other_profile(request, user_id):

    try:
        other_user = CustomUser.objects.get(uuid=user_id)
        actual_user = request.user
    except CustomUser.DoesNotExist:
        error = 'Cet utilisateur n\'existe pas'
        return render(request, 'base/home.html', context={'error': error})

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

    return render(request, 'users/show.html',
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
    users = CustomUser.objects.exclude(uuid=actual_user.pk)

    try:
        user_follow = users.get(uuid=user_id)
        UserFollows.objects.create(user=actual_user,
                                   followed_user=user_follow)

    except CustomUser.DoesNotExist:
        pass

    return redirect('all_users')


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
    return redirect('all_users')


'''
Ticket part
'''


# Flux
@login_required(login_url='http://localhost:8000')
def flux(request):
    user = request.user
    # Getting the ticket of users follower
    followed = UserFollows.objects.filter(user=user)
    # all tickets, mine ticket than others
    all_tickets = Ticket.objects.filter(Q(user=user) |
                                        Q(user__in=followed.values_list(
                                              'followed_user',
                                              flat=True)))
    all_tickets.order_by('-time_created')

    # Geting the reviews
    following = user.following.all()
    following = [u.followed_user for u in following]
    following.append(user)

    reviews2_others = Review.objects.filter(user__in=following)
    reviews2_others.order_by('-time_created')

    # creating a list of reviews and tickets
    tickets_revies = list(chain(all_tickets, reviews2_others))
    ticks_revs_sorted = sorted(tickets_revies,
                               key=lambda obj: obj.time_created,
                               reverse=True
                               )

    tickets_reviews = []
    for tic_rev in ticks_revs_sorted:
        if hasattr(tic_rev, 'title'):
            tickets_reviews.append((tic_rev, 'T'))
        else:
            tickets_reviews.append((tic_rev, 'R'))

    # Sending the review form
    reviw_form = ReviewForm(request.POST or None)
    return render(request, 'tickets/flux.html',
                  {'tickets_reviews': tickets_reviews,
                   'form': reviw_form
                   }
                  )


@login_required(login_url='http://localhost:8000')
def ticket(request):
    ticket_form = TicketForm(request.POST or None)
    return render(request, 'tickets/ticket.html',
                  context={'form': ticket_form}
                  )


@login_required(login_url='http://localhost:8000')
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            image = form.cleaned_data['image']
            # Creating the ticket
            new_ticket = Ticket.objects.create(user=request.user,
                                               title=title,
                                               description=description,
                                               image=image
                                               )
            tickets = Ticket.objects.filter(user=new_ticket.user)
            tickets.order_by('-time_created')
            return render(request, 'tickets/all_tickets.html',
                          context={'tickets': tickets}
                          )

    return redirect('ticket')


# Factorizing review form
def refactor_review_form(request) -> ReviewForm:
    review_form = ReviewForm(request.POST or None)
    # review_form = ReviewForm(initial={'username': user.username})
    return review_form


@login_required(login_url='http://localhost:8000')
def my_tickets(request, user_id):
    user = request.user
    review_form = ReviewForm(request.POST)
    if user_id != user.uuid:
        followed = CustomUser.objects.get(uuid=user_id)
    else:
        followed = user

    tickets = Ticket.objects.filter(user=followed).order_by('-time_created')

    return render(request, 'tickets/all_tickets.html',
                  context={'tickets': tickets,
                           'user': followed,
                           'form': review_form,
                           }
                  )


# Page for ticket and review
def ticket_and_review(request):
    ticket_form = TicketForm(request.POST or None)
    review_form = ReviewForm(request.POST or None)

    return render(request, 'tickets/ticket_and_review.html',
                  context={
                        'ticket_form': ticket_form,
                        'review_form': review_form
                        }
                  )


# Creating ticket and review at the same time
@login_required(login_url='http://localhost:8000')
def create_tck_rvw(request):
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form is None or review_form is None:
            print('The ticket or review form is empty')
            return redirect('flux')

        if ticket_form.is_valid() and review_form.is_valid():
            title = ticket_form.cleaned_data['title']
            description = ticket_form.cleaned_data['description']
            image = ticket_form.cleaned_data['image']
            headline = review_form.cleaned_data['headline']
            body = review_form.cleaned_data['body']
            rating = review_form.cleaned_data['rating']

            # Creating the ticket
            ticket = Ticket.objects.create(user=request.user,
                                           title=title,
                                           description=description,
                                           image=image
                                           )

            # Creating the review
            Review.objects.create(user=request.user,
                                  ticket=ticket,
                                  headline=headline,
                                  body=body,
                                  rating=rating
                                  )
            tickets = Ticket.objects.filter(user=ticket.user)
            tickets.order_by('-time_created')
            return render(request, 'tickets/all_tickets.html',
                          context={'tickets': tickets}
                          )

    ticket_form = TicketForm(request.POST or None)
    user = request.user
    ticket_form = TicketForm(initial={'username': user.username})

    return render(request, 'tickets/ticket.html',
                  context={
                    'form': ticket_form,
                    }
                  )


# update ticket
def update_tck(request):
    user = request.user
    if request.method == "POST":
        data = request.POST
        ticket_id = data.get('ticket_id')
        try:
            ticket = Ticket.objects.get(uuid=ticket_id)
            # Checking if the ticket belongs to the user
            if ticket.user != user:
                return redirect('my_tickets')

            ticket.title = data.get('ticket_title')
            ticket.description = data.get('description')
            if 'image' in request.FILES:
                ticket.image = request.FILES['image']
            ticket.save()

            tickets = Ticket.objects.filter(user=ticket.user)
            form = ReviewForm(request.POST or None)
            return render(request, 'tickets/all_tickets.html',
                          context={
                                'tickets': tickets,
                                'form': form,
                                'user': user
                                })
        except Ticket.DoesNotExist:
            error = "The ticked you updated does not exists"
            return render(request, 'users/show.html',
                          context={'user': user.username,
                                   'error': error
                                   })


# delete ticket
def delete_ticket(request):
    data = request.POST
    ticket_id = data.get('ticket_id')
    ticket = Ticket.objects.get(uuid=ticket_id)
    tickets = Ticket.objects.filter(user=request.user)
    tickets.order_by('-time_created')
    form = ReviewForm(request.POST or None)

    if ticket.user == request.user:
        ticket.delete()
        return render(request, 'tickets/all_tickets.html',
                      context={
                        'tickets': tickets,
                        'form': form,
                        'user': request.user
                          }
                      )


'''
Review part
'''


@login_required(login_url='http://localhost:8000')
def create_review(request):
    user = request.user
    error = None
    if request.method == 'POST':
        try:
            ticket_id = request.POST.get('ticket_id')
            print("Beforeee... ")
            ticket = Ticket.objects.get(uuid=ticket_id)
            # Geting the ticket from the right user
            tickets = Ticket.objects.filter(user=ticket.user)
            tickets.order_by('-time_created')

            form = ReviewForm(request.POST)

            if form.is_valid():
                headline = form.cleaned_data['headline']
                body = form.cleaned_data['body']
                rating = form.cleaned_data['rating']
                # Creating the review
                Review.objects.create(user=user,
                                      ticket=ticket,
                                      headline=headline,
                                      body=body,
                                      rating=rating
                                      )
                # form2 = refactor_review_form(request)
                # return render(request, 'tickets/all_tickets.html',
                #               context={'ticket': ticket,
                #                        'tickets': tickets,
                #                        'form': form2
                #                        })
                return redirect('flux')

        except Ticket.DoesNotExist:
            error = 'The ticket does not exist'

        review_form = refactor_review_form(request)
        return render(request, 'tickets/all_tickets.html',
                      context={'error': error,
                               'form': review_form,
                               'tickets': tickets
                               })
