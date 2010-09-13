from datetime import datetime
import hashlib
import subprocess as sub

from flask import Flask, url_for, abort, render_template as render, request
from flaskext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('settings_local')
db = SQLAlchemy(app)


class Mission(db.Model):
    __tablename__ = 'missions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))  # How we called the command.
    text = db.Column(db.Text)         # What the script looked like.
    started = db.Column(db.DateTime)
    finished = db.Column(db.DateTime)
    duration = db.Column(db.Float)
    stdout = db.Column(db.Text)
    stderr = db.Column(db.Text)
    exit_code = db.Column(db.Integer)

    @classmethod
    def go(cls, command):
        p = sub.Popen(['which', command.split()[0]], stdout=sub.PIPE)
        loc = p.communicate()[0].strip()
        p = sub.Popen('file -i %s' % loc, stdout=sub.PIPE, shell=True)
        file_type = p.communicate()[0]
        if 'text' in file_type:
            text = open(loc).read()
        else:
            text = file_type

        start = datetime.now()
        proc = sub.Popen(command, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
        out, err = proc.communicate()
        finish = datetime.now()
        t = finish - start
        duration = round(t.seconds + float(t.microseconds) / 10**6, 3)

        m = Mission(name=command, text=text, started=start, finished=finish,
                    duration=duration, stdout=out, stderr=err,
                    exit_code=proc.returncode)
        db.session.add(m)
        db.session.commit()
        return m


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


@app.route('/monitor')
def monitor():
    return tasks.how_you_doin.delay().wait(timeout=1)


# Hey circular imports!
import tasks
