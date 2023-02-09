# DT django homework

## Introduction
Hi! This is my new telegram bot. It was made as a homework for django course and doesn't serve much purpose right now.

Don't forget to check out the [course](https://www.youtube.com/playlist?list=PLQ09TvuOLytTca-0iXr09Ncohrs7qz5ju)!

## Quick start
Install the package
``` bash 
git clone https://gitlab.com/yura34054/DT-django-homework.git
cd DT-django-homework
```

Create virtual environment (optional)
``` bash
python3 -m venv venv
source venv/bin/activate
```

Install all requirements
``` bash
make piplock
```

Run migrations to setup SQLite database
``` bash
make migrate
```

Create .env file, don't forget to change the data
``` bash
cp .env.example .env
```

Because server will be local you need to use ngrok or other tool to route the connection, add your URL to .env file, 
``` bash
ngrok http 8000
```

Finally you can run the server
``` bash
make dev
```


## Possible problems
* This bot works in webhook mode. If you want, you can run a parallel process getting updates and sending them to localhost.
* Some code assumes that telegram blocks all messaging before the first /start command, this can lead to problems if you are removing data from database.

## Known issues
* webhook initialization can run more than once producing "Too Many Requests" error message

## Getting help
If you have a problem setting up or a question you can contact me:

telegram: https://t.me/Yurii_Mironov

email: ur34054@gmail.com
