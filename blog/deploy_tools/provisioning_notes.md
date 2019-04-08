部署
======


## 需要安装的包（全局）：

* Git

* nginx

* python 3

* python3-pip

* virtualenv

Ubuntu ex:

```shell
$ sudo apt-get install git nginx python3 python3-pip
$ sudo pip3 install virtualenv
```

## （django 无关的）配置文件

### Nginx

```shell
$ SITENAME="my-domain.com"
$ cp nginx.SITENAME $SITENAME
$ {{ SITENAME }} --to--> $SITENAME
$ sudo cp $SITENAME /etc/nginx/sites-avaiable/
$ sudo ln -s /etc/nginx/sites-avaiable/$SITENAME \
             /etc/nginx/sites-enable/$SITENAME
```

### tempfiles

同上类似


### systemd

同上类似

`/etc/systemd/system/`


## 运行

```shell
$ sudo systemctl enable gunicorn-$SITENAME.socket
$ sudo systemctl start gunicorn-$SITENAME.socket
$ sudo service restart nginx
```

## Django 相关

### 目录

```shell
/home/deploy
 |
 +-- sites
       |
       +-- $SITENAME
             |
             +-- database/
             +-- source/
             +-- static_cdn/
             +-- media_cdn/
             |   # $ virtualenv ./virtualenv --python=python3
             +-- virtualenv/
```

### 数据库与静态文件收集

### 配置文件 - `ALLOWED_HOSTS`


