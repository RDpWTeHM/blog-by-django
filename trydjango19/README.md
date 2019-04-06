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
#### create Post models
src$ python manage.py makemigrations
src$ python manage.py migrate

#### bring the database(models) to administration
#### create PostModelAdmin for more Granularity customization admin



