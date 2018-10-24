from __future__ import print_function
import os
import time
from flask import Flask, render_template_string, request, redirect, url_for
app = Flask(__name__)
TSTAMP_FILE = os.getenv("TSTAMP_FILE", "/tmp/tstamp.log")
INDEX = """
{% block content %}
<form action="" method="post">
  <input type="submit" name="timestamp" value="Timestamp!"/>
  <input type="submit" name="clear" value="Clear!"/>
</form>
{% for t in tstamps %}
<p>
{{ t }}
</p>
{% endfor %}
{% endblock %}
"""


def get_tstamp():
    # open with 'a+' to create (empty) file on fresh start
    with open(TSTAMP_FILE, "a+") as f:
        return f.readlines()


def new_tstamp():
    with open(TSTAMP_FILE, "a+") as f:
        f.write("%s\n" % (time.asctime(),))


def clear_tstamp():
    with open(TSTAMP_FILE, "w+") as _:
        pass


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if "clear" in request.form:
            clear_tstamp()
        if "timestamp" in request.form:
            new_tstamp()
        redirect(url_for('index'))

    tstamps = get_tstamp()
    if not tstamps:
        tstamps.append("No timestamps")
    return render_template_string(INDEX, tstamps=reversed(tstamps))
