# TeamBot
Telegram Bot powered with a Django site to handle assembling of teams

# General Info
There are a number of captains, chosen by the admin.
Users contacting the bot are asked for personal information,
and for the captain they want to play with; the bot then sends
a request with a summary to the selected captain.
The captain can accept or deny it; in case of denial,
the request goes to another captain (randomly chosen) until
someone has accepted or everyone has refused.
Then the user is noticed to be inserted in a team, or to be
refused by all.

The Bot works with a webhook to a Django site on heroku,
that is also used to manage and download information collected.

# Get started:
To install the project, clone the repo, create a proper virtualenv and 
run: pip install -r requirements.txt
Write your Python version (up to 3.6) in runtime.txt (check if Heroku supports is) and create
a postgres database, specifying user, password and dbname in localdb.env

To initialize the database run: python manage.py migrate

After every modifications to models: python manage.py makemigrations

If you need to intervene on the DB run: python manage.py shell

To start the local development server run:
python manage.py runserver --noreload
and go on localhost:8000/ to access the site

Given that Heroku mostly uses Postgres as DB (Postgres add-on), even
in local development I suggest using the same.

Given that in production the Bot works with a webhook,
I suggest to use a webhook even in local development.
