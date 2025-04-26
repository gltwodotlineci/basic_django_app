### Welcom to this basic MVC Djaango app.
### IN This app we can share Tickets and Reviews about books or articles with other users that we follow.

#### To start the construction of this app we will need to follow the previws instructions

##### First we start by creating the virtual envirenement
Let first check the package manager 'pip'
```bash
pip -V
# if there is no pip or we have an older version than 24.0
# we can install it.
python3 -m pip install 'requests==24.0'
# or upgrading it
python3 -m pip install --upgrade pip
```

```bash
sudo apt update
sudo apt install python3-venv
# Starting the virtual envirenement
python3 -m venv env
source ./env/bin/activate
```

##### Let start by installing Django in our virtual envirenement and than starting our project


```bash
python3 -m venv env
source ./env/bin/activate
pip install django==4.2

# Starting the project:
django-admin startproject book_critics
cd book_critics
python manage.py startapp book_critics_core
```

Once we created the project and the app, it is highly recomanded to create the User model.
We can create the user model with the AbstractUser. And we shall add the following lines in settings.py
```python
INSTALLED_APPS = [
    ...
    'book_critics_core',
]
AUTH_USER_MODEL = 'book_critics_core.CustomUser'
```
And latter we can launch the migrations
```bash
./manage.py makemigrations
./manage.py migrate
```

If we want to download the application from github. We can skip all the parts from the creation of django. We can just check the package manager and create the virtual envirenement utill the line 22 of the 'README.md document'

We can start with downloading the github repository and that we can launch the requirments document.
```bash
# Download repository
git clone https://github.com/gltwodotlineci/basic_django_app.git
# Or if we have the SSH key in the github account:
gti clone git@github.com:gltwodotlineci/basic_django_app.git

# Now we can add the dependences:
cd proj_books_critics
python -m pip install -r requirements.txt
# Or
python3 -m pip install -r requirements.txt
```

##### Checking if the app respect PEP8 practice.
We will with Flake8 if the PEP8 practice is respected
```bash
python -m pip install flake8
# In the root of the app we can lunch the next commands:
flake8 book_critics/urls.py
flake8 book_critics_core/urls.py
flake8 book_critics_core/views.py
flake8 book_critics_core/forms.py
flake8 book_critics_core/models.py
# Or
flake8 book_critics/urls.py book_critics_core/urls.py book_critics_core/views.py book_critics_core/forms.py book_critics_core/models.py
```
