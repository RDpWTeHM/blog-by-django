from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/RDpWTeHM/blog-by-django.git'


# if not env.SITENAME:
#     raise SystemExit("Please setup SITENAME at env")


def deploy():
    site_folder = "/home/%s/sites/%s" % (env.user, env.host)

    checkout_source_folder = site_folder + '/checkout-source'
    source_folder = site_folder + '/source'

    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(checkout_source_folder, source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    require_server_folders = (
        'database',
        'static_cdn', 'media_cdn',
        'source', 'checkout-source',
        'virtualenv', )
    for subfolder in require_server_folders:
        run('mkdir -p %s/%s' % (site_folder, subfolder))


def _get_latest_source(checkout_source_folder, source_folder):
    if exists(checkout_source_folder + '/.git'):
        run('cd %s && git fetch' % (checkout_source_folder, ))
    else:
        run('git clone %s %s' % (REPO_URL, checkout_source_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd %s && git reset --hard %s' % (checkout_source_folder, current_commit))

    run("cp -fr %s/blog/src/* %s" % (checkout_source_folder, source_folder))


def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/blog/settings.py'
    # DEBUG flag  #######################################
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    # ALLOWED_HOSTS  ###################################
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["{}"]'.format(site_name),
        )

    # secret_key   ####################################
    secret_key_file = source_folder + '/blog/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key, ))

    sed(settings_path,
        'SECRET_KEY =.+$',
        "from .secret_key import SECRET_KEY"
        )


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + "/../virtualenv"
    if not exists(virtualenv_folder + '/bin/pip'):
        run("virtualenv --python=python3 %s" % (virtualenv_folder, ))
    run('%s/bin/pip install -r %s/requirements.txt' % (
        virtualenv_folder, source_folder
    ))


def _update_static_files(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' % (
        source_folder,
    ))


def _update_database(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py migrate' % (
        source_folder,
    ))
