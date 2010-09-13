import hashlib

from flask import Flask, url_for, abort, render_template as render, request

import tasks


app = Flask(__name__)
app.config.from_object('settings_local')


def hook_secret():
    return hashlib.new('md5', 'hook:' + app.secret_key).hexdigest()


@app.route('/github/<secret>', methods=['POST'])
def github_hook(secret):
    if secret != hook_secret():
        abort(400)
    name = request.json['repository']['name']
    tasks.github_hook.delay(request.json['repository']['name'])
    return 'OK : %s' % name


# TODO: ldap auth
@app.route('/admin')
def admin():
    gh = url_for('github_hook', secret=hook_secret(), _external=True)
    return render('admin.html', github_url=gh)
