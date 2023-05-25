# DT django homework

## Introduction
Hi! This is my new telegram bot. It was made as a homework for django course.
With it, you can send "money" and postcards to friends.

Don't forget to check out the [course](https://www.youtube.com/playlist?list=PLQ09TvuOLytTca-0iXr09Ncohrs7qz5ju)!

## Quick start
Clone the project
``` bash 
git clone https://gitlab.com/yura34054/DT-django-homework.git
cd DT-django-homework
```

Create .env file, don't forget to change the data
``` bash
cp .env.example .env
```

Because server will be local you need to use ngrok or other tool to route the connection, add your DOMAIN to .env file 
``` bash
ngrok http 8000
```

Finally, you can build the image and run in container with one command
``` bash
make
```

## Possible problems
* This bot works only in webhook mode.
* Some code assumes that telegram blocks all messaging before the first /start command, 
this can lead to problems if you are removing data from database.

## Getting help
If you have a problem setting up or a question you can contact me:

telegram: https://t.me/Yurii_Mironov

email: ur34054@gmail.com
