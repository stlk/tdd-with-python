from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/stlk/tdd-with-python.git'  #1
SITES_FOLDER = '/home/ubuntu/sites'

def deploy():
    _create_directory_structure_if_necessary(env.host)  #2
    source_folder = '%s/%s/source' % (SITES_FOLDER, env.host)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)

def _create_directory_structure_if_necessary(site_name):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p %s/%s/%s' % (SITES_FOLDER, site_name, subfolder))  #12

def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):  #1
        run('cd %s && git fetch' % (source_folder,))  #23
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))  #4
    current_commit = local("git log -n 1 --format=%H", capture=True)  #5
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))  #6

def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path, 'DOMAIN = "localhost"', 'DOMAIN = "%s"' % (site_name,))
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')  #45

def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'): #1
        run('virtualenv --python=python3.3 %s' % (virtualenv_folder,))
    run('%s/bin/pip install -r %s/requirements.txt' % ( #2
            virtualenv_folder, source_folder
    ))

def _update_static_files(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' % ( # 1
        source_folder,
    ))

def _update_database(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py syncdb --migrate --noinput' % (
    source_folder,
))