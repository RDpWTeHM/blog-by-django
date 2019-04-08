# Blog Site



## Demonstration

[:link: My personal blog](http://rdpwtehm.ddns.net:8080/posts/) site powered by this project for example.



## First Deploy

check `deploy_tools/provisioning_notes.md` for setting up 'nginx, systemd, etc...'



## Automatic Deploy

```
$ cd deploy_tools/
$ pip install Fabric3
#### or $ pip install --user Fabric3
#### or (virtualenv) $ pip install Fabric3
#### Fabric3 does not need at real service
$ fab deploy:host=<your-username-in-real-site-server>@<your-domain-name>
#### for ex:
#### $ fab deploy:host=user1@rdpwtehm.top
...output...
...done
```

