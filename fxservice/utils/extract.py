import requests
import datetime
from flask import request


def yield_data(data):
    if data == None:
        return []
    for row in data:
        if "@url" in row:
            # Download the data first
            r = requests.get(
                row["@url"], allow_redirects=True, stream=True, timeout=6000
            )
            d = r.json().get("data")
            if d:
                yield from yield_data(d)
        else:
            yield row


def get_url_params() -> (dict, bool):
    _from = request.args.get("from")
    to = request.args.get("to")
    amount = request.args.get("amount")
    if None in (_from, to, amount):
        return {
            "from": _from,
            "to": to,
            "amount": amount,
            "date": datetime.datetime.now().date().strftime("%Y-%m-%d"),
            "client": request.args.get("client", default="default"),
            "method": request.args.get("method", default="day"),
            "places": request.args.get("places", default=6),
        }, True

    date = request.args.get(
        "date", default=datetime.datetime.now().date().strftime("%Y-%m-%d")
    )
    return {
        "from": _from,
        "to": to,
        "amount": amount,
        "date": date,
        "client": request.args.get("client", default="default"),
        "method": request.args.get("method", default="day"),
        "places": request.args.get("places", default=6),
    }, False
