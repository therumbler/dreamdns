import logging
import os
import sys

from flask import Flask, request, abort
from dreamhost import dynamic_dns

logger = logging.getLogger(__name__)


DREAMHOST_API_KEY = os.environ["DREAMHOST_API_KEY"]


app = Flask(__name__)

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


@app.route("/")
def index():
    api_key = request.args.get("key")
    hostname = request.args.get("hostname")
    ip = request.args.get("ip")

    if api_key != DREAMHOST_API_KEY:
        logger.error('invalid api key')
        abort(403, "invalid api key")

    if not hostname:
        logger.error("no hostname entered")
        abort(400, "missing hostname parameter")

    if not ip:
        logger.error("no ip entered")
        abort(400, "missing ip parameter")

    logger.info("ip = %s", ip)
    resp = dynamic_dns(ip, hostname)
    return resp

