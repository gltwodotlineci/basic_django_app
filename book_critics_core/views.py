from django.shortcuts import render, redirect
from .models import CustomUser, Ticket, Review, UserFollows
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignupForm, TicketForm, ReviewForm
from django.db.models import Q
from itertools import chain


def home(request):
    """
    Home page
    """
    if request.user.is_authenticated:
        return redirect('profile')

    login_form = LoginForm(request.POST or None)

    return render(request, 'base/home.html',
                  context={'form': login_form})


def login_user(request):
    """
    Login user. Check if the user is already authenticated
    and redirect to the profile page if so.
    If not, check if the form is valid
    """
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
    """
    Signup page. Check if the user is already authenticated
    and redirect to the profile page if so. If not, send the
    signup form to the template.
    """
    if request.user.is_authenticated:
        return redirect('profile')

    signup_form = SignupForm(request.POST or None)
    return render(request, 'acces/signup.html',
                  context={'signup_form': signup_form}
                  )


def inscription(request):
    if request.method == 'POST':
        """
        Check if the form is valid and create the user
        """
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
    """
    Logout user
    """
    logout(request)
    return redirect("home")


def refacto_followers(user: CustomUser) -> tuple:
    """
    Refactored function to get the list of followers
    """
    follower_users = user.following.all()
    following_lst = [u.followed_user for u in follower_users]
    followers = user.followed_user.all

    return follower_users, following_lst, followers


@login_required(login_url='http://localhost:8000')
def all_users(request):
    """
    Show users
    Send all the followed users to the template
    """
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
    """
    Show the profile of the user or of  the followed user
    """
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
    """
    Search user by initials
    Check if the user is already authenticated
    Check if the user serched exists and if the initials
    are at least 2 characters
    """
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


@login_required(login_url='http://localhost:8000')
def follow_user(request):
    """
    Follow a user
    Check if the user is already authenticated
    Check if the user you want to follow exists
    Create the user_follows object
    """
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
    """
    Unfollow a user
    Check if the user is already authenticated
    Check if the user you want to unfollow exists
    Delete the user_follows object
    """
    actual_user = request.user
    data = request.POST
    followed = data.get('user_id')
    try:
        followed_user = UserFollows.objects.filter(
            user=actual_user,
            followed_user=followed
        )
        followed_user.delete()
    except UserFollows.DoesNotExist:
        print("The user you want to unfollow does not exist")

    return redirect('all_users')


'''
Ticket part
'''


@login_required(login_url='http://localhost:8000')
def flux(request):
    """
    Show the flux of the user
    Get your tickets and your reviews, also them of hwo yo're following
    Create a list of tickets and reviews and send to the template
    """
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
    """
    Ticket page
    Check if the user is already authenticated
    Send the ticket form to the template
    """
    ticket_form = TicketForm(request.POST or None)
    return render(request, 'tickets/ticket.html',
                  context={'form': ticket_form}
                  )


@login_required(login_url='http://localhost:8000')
def create_ticket(request):
    """
    Create a ticket
    Check if the user is already authenticated
    Check if the form is valid
    Create the ticket
    """
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


def refactor_review_form(request) -> ReviewForm:
    """
    Factorizing review form
    """
    review_form = ReviewForm(request.POST or None)
    # review_form = ReviewForm(initial={'username': user.username})
    return review_form


@login_required(login_url='http://localhost:8000')
def my_tickets(request, user_id):
    """
    Show the tickets of the user
    Check if the user is already authenticated
    Send the tickets of the user to the template
    """
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


def ticket_and_review(request):
    """
    Ticket and review page
    Send the ticket and the review form to the template
    """
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
    """
    Creating a ticket and a review at the same time
    Check if the user is already authenticated
    Check if the forms are valid
    Create the ticket and the review
    """
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


def update_tck(request):
    """
    Check if the user is already authenticated and if the ticket exists
    Check if the ticket belongs to the user
    Update the ticket
    """
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


def update_review(request):
    """
    Check if the user is already authenticated and if the review exists
    Check if the review belongs to the user
    Update the review
    """
    user = request.user
    if request.method == "POST":
        data = request.POST
        review_id = data.get('review_id')
        ticket_id = data.get('ticket_id')
        try:
            review = Review.objects.get(uuid=review_id)
            ticket = Ticket.objects.get(uuid=ticket_id)
            if review.user != user and ticket.user != user:
                return redirect('flux')
            review.headline = data.get('headline')
            review.body = data.get('body')
            rating = data.get('rating')
            if rating is not None:
                review.rating = data.get('rating')
                review.rating = int(rating)
            review.save()
        except (Review.DoesNotExist, Ticket.DoesNotExist):
            error = "The review or ticket you updated does not exists"
            print(error)

    return redirect('flux')


def delete_ticket(request):
    """
    Check if it is user is the ticket's owner
    Delete the ticket
    """
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


def delete_review(request):
    """
    Check if it is user is the review's owner
    Delete the review
    """
    if request.method == 'POST':
        data = request.POST
        review_id = data.get('review_id')
        try:
            review = Review.objects.get(uuid=review_id)
            if request.user == review.user:
                review.delete()
                return redirect('flux')
        except Review.DoesNotExist:
            error = "The review you want to delete does not exists"
            print(error)

    return redirect('flux')


'''
Review part
'''


@login_required(login_url='http://localhost:8000')
def create_review(request):
    """
    Check if the user is already authenticated
    Check if the form is valid
    Create the review
    """
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

                return redirect('flux')

        except Ticket.DoesNotExist:
            error = 'The ticket does not exist'

        review_form = refactor_review_form(request)
        return render(request, 'tickets/all_tickets.html',
                      context={'error': error,
                               'form': review_form,
                               'tickets': tickets
                               })
