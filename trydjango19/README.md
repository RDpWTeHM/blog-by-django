# READ ME



Reference:

https://www.youtube.com/playlist?list=PLEsfXFp6DpzQFqfCur9CJ4QnKQTVXUsRy


command history:
$ virtualenv .
$ source bin/activate
$ ## install django==1.9
$ ## create django project
$ ## trydjango19(django project) to src/
$
$ cd src
$ python manage.py migrate
$ python manage.py createsuperuser
...

src$ python manage.py startapp posts
#### install application in settings.py
#### create Post models
src$ python manage.py makemigrations
src$ python manage.py migrate

#### bring the database(models) to administration
#### create PostModelAdmin for more Granularity customization admin

## learning "what is CRUD?"

src$ touch posts/urls.py
#### create basic posts-index 'posts_home' function in posts/views.py
## learning url pattern of django

## learning render HTML basic

#### render HTML by queryset Post model

#### posts list -to-> post detail, use django reverse (resolve URL)

#### create post page by use django forms.
#### POST method success, redirect to home page


## update post
#### update URL and view - no real content
#### reuse create HTML to 'update'


## User Action Message
#### django.contrib.messages


## use template inherit
#### use template 'include' to include message


## Static files
#### change settings file for could use collectstatic

src$ mkdir static
src$ mkdir ../static_cdn
src$ python manage.py collectstatic

#### load static files - base.css for example


## Pagination
#### reference: https://docs.djangoproject.com/en/1.9/topics/pagination/


