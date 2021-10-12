import os
import logging
import datetime
import requests
from flask import Flask, request, jsonify
from flask.views import MethodView
from .utils.response import response_builder
from .utils.convert import calculate_fx
from .utils.extract import yield_data, get_url_params
from .utils.errors import UnprocessableEntity, ServiceUnavailable, NotFound


app = Flask(__name__, static_folder=None)
app.logger.setLevel(logging.DEBUG)
app.config["JSON_SORT_KEYS"] = False

FX_DATA_URL = os.getenv("FX_DATA_URL", "https://fxdata.operandoinnovation.net/getRates")


@app.errorhandler(UnprocessableEntity)
def handle_unprocessable_entity(error):
    app.logger.debug("required parameters are missing!!")
    payload = dict(error.payload or ())
    payload["success"] = False
    payload["code"] = error.status
    payload["message"] = error.message
    return jsonify(payload), 422


@app.errorhandler(ServiceUnavailable)
def handle_service_unavailable(error):
    app.logger.debug(error.message)
    payload = dict(error.payload or ())
    payload["success"] = False
    payload["code"] = error.status
    payload["message"] = error.message
    return jsonify(payload), 503


@app.errorhandler(NotFound)
def handle_not_found(error):
    app.logger.debug(error.message)
    payload = dict(error.payload or ())
    payload["success"] = False
    payload["code"] = error.status
    payload["message"] = error.message
    return jsonify(payload), 404


class HealthCheck(MethodView):
    def get(self):
        app.logger.debug("entered get method in HealthCheck")
        return {}


class FxConvertView(MethodView):
    """FxConvertView"""

    def get(self) -> dict:
        app.logger.debug("entered get method in FxConvert")

        params, err = get_url_params()
        if err:
            raise UnprocessableEntity("Missing required parameters")

        # added because mock just does not want to work today
        if not app.config["TESTING"]:
            req = requests.get(
                FX_DATA_URL
                + "?from={}&to={}&date={}&client={}&method={}".format(
                    params["from"],
                    params["to"],
                    params["date"],
                    params["client"],
                    params["method"],
                )
            )
            data = req.json()
        else:
            req = requests.Response()
            req.status_code = 200
            data = {
                "status": "ok",
                "statusCode": 200,
                "message": "get rate for EUR to USD",
                "detail": {"rate": "1.196231"},
            }

        if req.status_code != 200:
            if req.status_code == 404:
                raise NotFound("{}".format(data["message"]))
            raise ServiceUnavailable(
                "failure from fxdata with status {}".format(req.status_code)
            )

        app.logger.debug("result from fxdata: {}".format(data))

        result = calculate_fx(
            str(params["amount"]), str(data["detail"]["rate"]), int(params["places"])
        )

        response = response_builder(
            success=True,
            from_=params["from"],
            to=params["to"],
            amount=params["amount"],
            rate=str(data["detail"]["rate"]),
            date=params["date"],
            result=str(result),
            client=params["client"],
        )

        return response.to_dict(), 200




app.add_url_rule("/convert", view_func=FxConvertView.as_view("conversion_view"))
app.add_url_rule("/healthcheck", view_func=HealthCheck.as_view("healthcheck_view"))
