from __future__ import print_function
import os
from datetime import datetime
import socket
import random
import redis
from werkzeug.urls import url_encode, url_parse, url_unparse
from functools import partial
from flask import Flask, render_template_string, request, redirect, url_for


INDEX = """
{% block content %}
<form action="" method="post">
 <input type="submit" name="timestamp" value="Timestamp!"/>
 <input type="submit" name="clear" value="Clear!"/>
</form>
<hr/>
Timestamps app '{{ color }}' on {{ hostname }} from {{ request.remote_addr }}, using {{ storage_type }} storage
<ul>
<li>path: {{ request.path }}</li>
<li>script_root: {{ request.script_root }}</li>
<li>base_url: <a href="{{ request.base_url }}">{{ request.base_url }}</a></li>
<li>url: <a href="{{ request.url }}">{{ request.url }}</a></li>
<li>url_root: <a href="{{ request.url_root }}">{{ request.url_root }}</a></li>
</ul>
<hr/>
<ul>
{% for h,v in request.headers.items() %}
<li>{{ h }}={{ v }}</li>
{% endfor %}
</ul>
<hr/>
</p>
<ul>
{{ timestamps|length }} timestamp{{ 's' if timestamps|length > 1 else '' }}
</p>
{% for t in timestamps|reverse %}
<li>{{ t }}</li>
{% endfor %}
</ul>
{% endblock %}
"""

# names generator from
# github.com/docker/docker-ce/components/engine/pkg/namesgenerator
names_generator_left = [
    "admiring",
    "adoring",
    "affectionate",
    "agitated",
    "amazing",
    "angry",
    "awesome",
    "beautiful",
    "blissful",
    "bold",
    "boring",
    "brave",
    "busy",
    "charming",
    "clever",
    "cool",
    "compassionate",
    "competent",
    "condescending",
    "confident",
    "cranky",
    "crazy",
    "dazzling",
    "determined",
    "distracted",
    "dreamy",
    "eager",
    "ecstatic",
    "elastic",
    "elated",
    "elegant",
    "eloquent",
    "epic",
    "exciting",
    "fervent",
    "festive",
    "flamboyant",
    "focused",
    "friendly",
    "frosty",
    "funny",
    "gallant",
    "gifted",
    "goofy",
    "gracious",
    "great",
    "happy",
    "hardcore",
    "heuristic",
    "hopeful",
    "hungry",
    "infallible",
    "inspiring",
    "interesting",
    "intelligent",
    "jolly",
    "jovial",
    "keen",
    "kind",
    "laughing",
    "loving",
    "lucid",
    "magical",
    "mystifying",
    "modest",
    "musing",
    "naughty",
    "nervous",
    "nice",
    "nifty",
    "nostalgic",
    "objective",
    "optimistic",
    "peaceful",
    "pedantic",
    "pensive",
    "practical",
    "priceless",
    "quirky",
    "quizzical",
    "recursing",
    "relaxed",
    "reverent",
    "romantic",
    "sad",
    "serene",
    "sharp",
    "silly",
    "sleepy",
    "stoic",
    "strange",
    "stupefied",
    "suspicious",
    "sweet",
    "tender",
    "thirsty",
    "trusting",
    "unruffled",
    "upbeat",
    "vibrant",
    "vigilant",
    "vigorous",
    "wizardly",
    "wonderful",
    "xenodochial",
    "youthful",
    "zealous",
    "zen",
]
names_generator_right = [
    "albattani",
    "allen",
    "almeida",
    "antonelli",
    "agnesi",
    "archimedes",
    "ardinghelli",
    "aryabhata",
    "austin",
    "babbage",
    "banach",
    "banzai",
    "bardeen",
    "bartik",
    "bassi",
    "beaver",
    "bell",
    "benz",
    "bhabha",
    "bhaskara",
    "black",
    "blackburn",
    "blackwell",
    "bohr",
    "booth",
    "borg",
    "bose",
    "bouman",
    "boyd",
    "brahmagupta",
    "brattain",
    "brown",
    "buck",
    "burnell",
    "cannon",
    "carson",
    "cartwright",
    "cerf",
    "chandrasekhar",
    "chaplygin",
    "chatelet",
    "chatterjee",
    "chebyshev",
    "cohen",
    "chaum",
    "clarke",
    "colden",
    "cori",
    "cray",
    "curran",
    "curie",
    "darwin",
    "davinci",
    "dewdney",
    "dhawan",
    "diffie",
    "dijkstra",
    "dirac",
    "driscoll",
    "dubinsky",
    "easley",
    "edison",
    "einstein",
    "elbakyan",
    "elgamal",
    "elion",
    "ellis",
    "engelbart",
    "euclid",
    "euler",
    "faraday",
    "feistel",
    "fermat",
    "fermi",
    "feynman",
    "franklin",
    "gagarin",
    "galileo",
    "galois",
    "ganguly",
    "gates",
    "gauss",
    "germain",
    "goldberg",
    "goldstine",
    "goldwasser",
    "golick",
    "goodall",
    "gould",
    "greider",
    "grothendieck",
    "haibt",
    "hamilton",
    "haslett",
    "hawking",
    "hellman",
    "heisenberg",
    "hermann",
    "herschel",
    "hertz",
    "heyrovsky",
    "hodgkin",
    "hofstadter",
    "hoover",
    "hopper",
    "hugle",
    "hypatia",
    "ishizaka",
    "jackson",
    "jang",
    "jennings",
    "jepsen",
    "johnson",
    "joliot",
    "jones",
    "kalam",
    "kapitsa",
    "kare",
    "keldysh",
    "keller",
    "kepler",
    "khayyam",
    "khorana",
    "kilby",
    "kirch",
    "knuth",
    "kowalevski",
    "lalande",
    "lamarr",
    "lamport",
    "leakey",
    "leavitt",
    "lederberg",
    "lehmann",
    "lewin",
    "lichterman",
    "liskov",
    "lovelace",
    "lumiere",
    "mahavira",
    "margulis",
    "matsumoto",
    "maxwell",
    "mayer",
    "mccarthy",
    "mcclintock",
    "mclaren",
    "mclean",
    "mcnulty",
    "mendel",
    "mendeleev",
    "meitner",
    "meninsky",
    "merkle",
    "mestorf",
    "minsky",
    "mirzakhani",
    "moore",
    "morse",
    "murdock",
    "moser",
    "napier",
    "nash",
    "neumann",
    "newton",
    "nightingale",
    "nobel",
    "noether",
    "northcutt",
    "noyce",
    "panini",
    "pare",
    "pascal",
    "pasteur",
    "payne",
    "perlman",
    "pike",
    "poincare",
    "poitras",
    "proskuriakova",
    "ptolemy",
    "raman",
    "ramanujan",
    "ride",
    "montalcini",
    "ritchie",
    "rhodes",
    "robinson",
    "roentgen",
    "rosalind",
    "rubin",
    "saha",
    "sammet",
    "sanderson",
    "satoshi",
    "shamir",
    "shannon",
    "shaw",
    "shirley",
    "shockley",
    "shtern",
    "sinoussi",
    "snyder",
    "solomon",
    "spence",
    "stallman",
    "stonebraker",
    "sutherland",
    "swanson",
    "swartz",
    "swirles",
    "taussig",
    "tereshkova",
    "tesla",
    "tharp",
    "thompson",
    "torvalds",
    "tu",
    "turing",
    "varahamihira",
    "vaughan",
    "visvesvaraya",
    "volhard",
    "villani",
    "wescoff",
    "wilbur",
    "wiles",
    "williams",
    "williamson",
    "wilson",
    "wing",
    "wozniak",
    "wright",
    "wu",
    "yalow",
    "yonath",
    "zhukovsky",
]


def get_random_name():
    left = random.choice(names_generator_left)
    right = random.choice(names_generator_right)
    return f"{left}_{right}"


def init_redis():
    redis_service = os.getenv('REDIS', 'redis')
    redis_port = os.getenv('REDIS_PORT', '6379')
    return redis.Redis(host=redis_service, port=redis_port)


# return timestamped message and time in microseconds
def make_timestamp(msg):
    now = datetime.now()
    ts = "%s %s" % (now.isoformat(timespec='microseconds'), msg)
    return (ts, now.timestamp() * 1000000)


def get_timestamps_file():
    try:
        with open(TIMESTAMPS_FILE, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        return []


def record_timestamp_file(msg):
    with open(TIMESTAMPS_FILE, "a+") as f:
        ts, _ = make_timestamp(msg)
        f.write("%s\n" % (ts,))


def clear_timestamps_file():
    with open(TIMESTAMPS_FILE, "w+") as _:
        pass


def get_timestamps_redis(conn, key):
    timestamps = conn.zrange(key, 0, -1)
    return [ts.decode('utf-8') for ts in timestamps]


def record_timestamp_redis(msg, conn, key):
    (timestamp, ms) = make_timestamp(msg)
    conn.zadd(key, {timestamp: ms})


def clear_timestamps_redis(conn, key):
    conn.delete(key)


app = Flask(__name__)
color = os.getenv("COLOR", "invisible")
TIMESTAMPS_FILE = os.getenv("TIMESTAMPS_FILE", "/tmp/timestamps.log")

if os.getenv('USE_REDIS') is None:
    storage_type = 'file'
    get_timestamps = get_timestamps_file
    record_timestamp = record_timestamp_file
    clear_timestamps = clear_timestamps_file
else:
    storage_type = 'redis'
    redis_conn = init_redis()
    redis_key = f"timestamps_{color}"
    get_timestamps = partial(get_timestamps_redis,
                             conn=redis_conn, key=redis_key)
    record_timestamp = partial(
        record_timestamp_redis, conn=redis_conn, key=redis_key)
    clear_timestamps = partial(
        clear_timestamps_redis, conn=redis_conn, key=redis_key)


def redirect_with_name(req):
    args = req.args.copy()
    args.setlist('name', [get_random_name()])
    query = url_encode(args)
    scheme, netloc, path, _, fragment = url_parse(req.url)
    redirect_url = url_unparse((scheme, netloc, path, query, fragment))
    return redirect(redirect_url)


@app.route("/", methods=['GET', 'POST'], defaults={"path": ""})
@app.route("/<path:path>", methods=['GET', 'POST'])
def index(path):
    hostname = socket.gethostname()
    if request.method == 'POST':
        if "clear" in request.form:
            clear_timestamps()
            return redirect(url_for('index', name=get_random_name()))

        if "timestamp" in request.form:
            record_timestamp(msg=f"hostname={hostname} color={color} url={request.url}")
            return redirect_with_name(request)

    # no name parameter ? come back with one !
    if request.args.get('name', None) is None:
        return redirect_with_name(request)

    timestamps = get_timestamps()
    return render_template_string(INDEX,
                                  timestamps=timestamps, storage_type=storage_type,
                                  hostname=hostname, path=path, request=request, color=color)


if __name__ == '__main__':
    host = os.getenv("HOST", "127.0.0.1")
    port = os.getenv("PORT", "5000")
    app.run(host=host, port=port)
