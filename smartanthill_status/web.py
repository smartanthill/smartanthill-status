# -*- coding: utf-8 -*-
import json

from bottle import Bottle, response
from sqlalchemy.sql.expression import distinct

from smartanthill_status import config
from smartanthill_status.database import db_session
from smartanthill_status.models import BuildStatistics

app = Bottle()


@app.hook("after_request")
def db_disconnect():
    db_session.close()


def _response(obj):
    response.set_header("Access-Control-Allow-Origin",
                        config['API_CORS_ORIGIN'])
    response.set_header("Access-Control-Allow-Methods", "GET, OPTIONS")
    response.set_header("Access-Control-Allow-Headers",
                        "Content-Type, Access-Control-Allow-Headers")
    response.set_header("Content-Type", "application/json")
    return json.dumps(obj, indent=2 if config['DEBUG'] else None)


@app.route("/embedded/envs")
def embedded_envs():
    qs = db_session.query(distinct(BuildStatistics.env))
    return _response([env for (env,) in qs])


@app.route("/embedded/build_memory_consumption/<env:re:[a-z0-9]+>")
def embedded_build_memory_consumption(env):
    qs = db_session.query(BuildStatistics)\
        .filter(BuildStatistics.env == env)\
        .order_by(BuildStatistics.id.desc())\
        .limit(25)
    return _response([bs.to_dict() for bs in qs])
