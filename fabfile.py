from fabric.contrib.files import exists
from fabric.api import (
    env, run, local, cd, task, prefix, shell_env, warn_only, quiet
)

env.repo_url = 'https://github.com/bhrutledge/jahhills.com.git'
env.project_pkg = 'hth'
env.project_apps = ['music', 'news', 'shows']


# TODO: Add dev environment
# TODO: Add staging environment


@task
def prod():
    env.hosts = ['debugged.org']
    env.user = 'rutt'
    env.user_dir = '/home/%(user)s' % env
    env.project_dir = '%(user_dir)s/webapps/jahhills' % env
    env.app_port = '13149'
    env.env_name = 'jahhills'
    env.settings = '%(project_pkg)s.settings.prod' % env
    env.requirements = 'requirements/dev.txt'
    env.workers = 4

    init_env()


@task
def dev():
    env.hosts = ['localhost']
    env.user = 'brian'
    env.user_dir = '/Users/%(user)s' % env
    env.project_dir = '%(user_dir)s/Code/jahhills.com' % env
    env.app_port = '8000'
    env.env_name = 'jahhills.com'
    env.settings = '%(project_pkg)s.settings.dev' % env
    env.requirements = 'requirements/dev.txt'

    init_env()


def init_env():
    # TODO: Merge these into one context manager
    env.django_env = dict(DJANGO_SETTINGS_MODULE=env.settings)
    env.workon = 'workon %(env_name)s' % env

    env.manage = 'cd %(project_pkg)s && ./manage.py' % env
    env.data = 'hth/jahhills.json'

    # TODO: Use a config file for gunicorn
    env.gunicorn = 'cd %(project_pkg)s && gunicorn' % env
    env.gunicorn_dir = '%(project_dir)s/.gunicorn' % env
    env.pid_path = '%(gunicorn_dir)s/pid' % env
    env.access_log_path = '%(gunicorn_dir)s/access_log' % env
    env.error_log_path = '%(gunicorn_dir)s/error_log' % env
    env.wsgi_app = '%(project_pkg)s.wsgi:application' % env


@task
def deploy():
    # Assume project apps and virtualenv are set up
    pull()
    requirements()
    migrate()
    loaddata()
    collectstatic()
    restart()


@task
def pull():
    with cd(env.project_dir):
        if exists('.git'):
            run('git pull')
        else:
            run('git clone %(repo_url)s .' % env)


@task
def requirements():
    with prefix(env.workon), shell_env(**env.django_env):
        run('pip-sync %(requirements)s' % env)


@task
def migrate():
    with prefix(env.workon), shell_env(**env.django_env):
        run('%(manage)s migrate --noinput' % env)


@task
def loaddata():
    with prefix(env.workon), shell_env(**env.django_env):
        run('%(manage)s loaddata %(data)s' % env)


@task
def dumpdata():
    # TODO: workon: command not found
    # with prefix(env.workon), shell_env(**env.django_env):
    # TODO: Set `run = local` for `dev` task.
    local('%(manage)s dumpdata --indent=4 music news shows > %(data)s' % env)


@task
def collectstatic():
    with prefix(env.workon), shell_env(**env.django_env):
        run('%(manage)s collectstatic --noinput' % env)


@task
def start():
    run('mkdir -p %(gunicorn_dir)s' % env)
    with prefix(env.workon), shell_env(**env.django_env):
        run('%(gunicorn)s --daemon '
            '--workers %(workers)s '
            '--bind 127.0.0.1:%(app_port)s '
            '--access-logfile %(access_log_path)s '
            '--error-logfile %(error_log_path)s '
            '--pid %(pid_path)s '
            '%(wsgi_app)s'
            % env)


@task
def stop():
    # TODO: Better orchestration with start()
    with warn_only():
        run('kill $(cat %(pid_path)s)' % env)

    with quiet():
        run('rm %(pid_path)s' % env)


@task
def restart():
    try:
        run('kill -HUP $(cat %(pid_path)s)' % env)
    except:
        start()
