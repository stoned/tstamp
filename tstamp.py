from __future__ import print_function
import os
import time
import socket
from flask import Flask, render_template_string, request, redirect, url_for


TSTAMP_FILE = os.getenv("TSTAMP_FILE", "/tmp/tstamp.log")
INDEX = """
{% block content %}
<form action="" method="post">
 <input type="submit" name="timestamp" value="Timestamp!"/>
 <input type="submit" name="clear" value="Clear!"/>
</form>
<hr/>
App {{ color }} on {{ hostname }} from {{ client }} with headers
<hr/>
<ul>
{% for h,v in headers.iteritems() %}
<li>{{ h }}={{ v }}</li>
{% endfor %}
</ul>
</p>
<ul>
{% for t in tstamps %}
<li>{{ t }}</li>
{% endfor %}
</ul>
{% endblock %}
"""


app = Flask(__name__)


def get_tstamp():
    # open with 'a+' to create (empty) file on fresh start
    with open(TSTAMP_FILE, "a+") as f:
        return f.readlines()


def new_tstamp(hostname):
    tstamp = time.asctime()
    ts = "%s %s" % (tstamp, hostname)
    with open(TSTAMP_FILE, "a+") as f:
        f.write("%s\n" % (ts,))


def clear_tstamp():
    with open(TSTAMP_FILE, "w+") as _:
        pass


@app.route("/", methods=['GET', 'POST'])
def index():
    hostname = socket.gethostname()
    color = os.getenv("COLOR", "'invisible'")
    if request.method == 'POST':
        if "clear" in request.form:
            clear_tstamp()
        if "timestamp" in request.form:
            new_tstamp(hostname)
        redirect(url_for('index'))

    tstamps = get_tstamp()
    if not tstamps:
        tstamps.append("No timestamps")
    return render_template_string(INDEX,
                                  tstamps=reversed(tstamps),
                                  hostname=hostname, client=request.remote_addr, headers=request.headers,
                                  color=color)


if __name__ == '__main__':
    host = os.getenv("HOST", "127.0.0.1")
    port = os.getenv("PORT", "5000")
    app.run(host=host, port=port)
