### Welcome to this basic MVC Djaango app.
### In This application we can share Tickets and Reviews about books or articles with other users that we follow.

#### To start the construction of this application we will need to follow the previews instructions.

##### First, we start by creating the virtual environment.
```bash
sudo apt update
sudo apt install python3-venv
# Starting the virtual environment
python3 -m venv env
source ./env/bin/activate
```

Now that we have the virtual environment we can start by adding the application in local.

We can start with downloading the github repository first. Once we have our repository in local. We can add all the dependences by launch the requirements.txt document. document.
```bash
# Download repository
git clone https://github.com/gltwodotlineci/basic_django_app.git
# Or if we have the SSH key in the github account:
gti clone git@github.com:gltwodotlineci/basic_django_app.git

# Now we can add the dependences:
# First, let's enter to the root of the app.
cd basic_django_app
python -m pip install -r requirements.txt
# Or
python3 -m pip install -r requirements.txt
```

##### Checking if the app respects PEP8 practice.
Before we launch the application we will use Flake8  in order to check if the PEP8 practice is respected.
```bash
# In the root of the app we can lunch the next commands:
flake8 book_critics/urls.py
flake8 book_critics_core/urls.py
flake8 book_critics_core/views.py
flake8 book_critics_core/forms.py
flake8 book_critics_core/models.py
# Or
flake8 book_critics/urls.py book_critics_core/urls.py book_critics_core/views.py book_critics_core/forms.py book_critics_core/models.py
```
#### If no mistake is shown, that means that the criteria Pep8 are respected.

Now we can launch our application by using the next command.
```bash
./manage.py runserver
```
______________________
### Testing with the existing datas
#### If you want to test you have this data
**Users:**
glen0
glen1
glen2
anna
andrea
brayan
bledi
The password is the same for all of them:
testtest
