# buy-the-dip
Tracker of all things stonky.

Live production version - https://buy-the-dip-czx4.onrender.com

Vision

Do you have stock FOMO?

Has this ever happened to you? 

'Ahhh gawsh dang it, if only I had seen this stock was cheeepp a few months ago I totally would have gone full send crypto moonshots on it.'

Well, with the latest in advanced tech and a bit of python you can say goodbye to those regrits.


PRE REQUISITS (You will need to have the following installed on your device.)

1. Docker
2. A postgres db instance.

SETUP

1. Run 'make install' to build the containers.
2. Add a .env file to the root directory with the postgres db credentials.
    POSTGRES_URL = ""
    POSTGRES_USER = ""
    POSTGRES_PW = ""
    POSTGRES_DB =  ""
2. Run 'make upgrade' to run migrations.
3. Run 'make run' to run the project. (You should be able to access the project on http://127.0.0.1:80)

![Screenshot 2024-03-07 at 11 19 18](https://github.com/JTerry96/buy-the-dip/assets/42044307/c6da96e4-2573-432c-b653-7dc00da42389)


