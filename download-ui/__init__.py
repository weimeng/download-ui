import os
import subprocess

from flask import Flask, flash, redirect, render_template, request, url_for

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/downloads', methods=['POST'])
    def downloads_create():
        url = request.form['url']

        try:
            subprocess.check_output([
                'gallery-dl', url,
                '-d', './downloads/gallery-dl',
                '--filename', '{num:>03}.{extension}',
                '--cbz'
            ])
            flash('successfully downloaded {}'.format(url), category='success')
        except subprocess.CalledProcessError as e:
            flash("command '{}' return with error (code {}): {}".format(' '.join(e.cmd), e.returncode, e.output), category='error')

        return redirect(url_for('index'))

    return app
