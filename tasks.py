from celery.decorators import task

from app import Mission


@task
def github_hook(repo, **kw):
    log = github_hook.get_logger(**kw)
    log.info('Running task with repo %s!' % repo)
    Mission.go('ls')
