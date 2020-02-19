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

# Customization
The states of conversations are codified by the classes in Bot.Questions; every class is a State and contains a make method (that handles what happens when a question is made) a process method (that handles what happens when a question is processed) and a filter attribute, that establishes if the Bot must re-ask the question or must pass to the process method.
The ordered list of questions (question_list), the method to handle the end (with success) of a request (end_conversation) and the method to handle the cancellation of the request (cancel) are in Bot.Questions.

The singles filters, make, process, end_conversation and cancel methods are completely customizable.

To sum up collected info, there is a method (info_summary) in Bot.utils that creates a formatted list of inserted info.

For each class of Bot.Questions there is a field in the Member model, named exactly like the attribute "key_name" and there is an attribute "key_verbose_name " that specifies the words used to list each record.
The info_summary method lists all the info inserted in the conversation applying str() to the fields of Member specified by "key_name", excluding the ones in the to_exclude list (a kw argument of the method).
You can easily change key_verbose_name to adapt it to your language.

The home page of the site is completely customizable by the "home" view method and the "home.html" and "base.html" templates. It contains buttons to reset, restart, and to download members and team summary.

Even the admin base template is customizable, in "templates/admin/base_site.html".

The captains can be modified in captains.txt or even from the admin interface.
To add a captain you need his telegram chat_id (you can find it by the get_id command).

The bot token is specified in Bot/bot_config.py, together with the chat_id of the admin (that gets all error messages on telegram).

Given that Heroku mostly uses Postgres as DB (Postgres add-on), even in local development I suggest using the same.
 
The project was originally developed to handle
the assembling of the teams for a treasure hunt 
(called Operation Moby Dick) in Rome.
(www.cacciacapitale.it)
