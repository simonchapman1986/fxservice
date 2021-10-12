class Response:
    """Response class to"""

    def __init__(self):
        self.success = None
        self.from_ = None
        self.to = None
        self.amount = None
        self.date = None
        self.rate = None
        self.result = None
        self.client = None

    def __str__(self):
        return str(self.__repr__())

    def __repr__(self):
        return {
            "success": self.success,
            "query": {"from": self.from_, "to": self.to, "amount": self.amount},
            "date": self.date,
            "client": self.client,
            "rate": self.rate,
            "result": self.result,
        }

    def to_dict(self):
        return self.__repr__()


def response_builder(
    success=False, from_="", to="", amount="", date="", rate="", result="", client=""
) -> Response:
    """builds json response

    :param success: [description], defaults to False
    :type success: bool, optional
    :param from_: [description], defaults to ""
    :type from_: str, optional
    :param to: [description], defaults to ""
    :type to: str, optional
    :param amount: [description], defaults to ""
    :type amount: str, optional
    :param date: [description], defaults to ""
    :type date: str, optional
    :param rate: [description], defaults to ""
    :type rate: str, optional
    :param result: [description], defaults to ""
    :type result: str, optional
    :return: [description]
    :rtype: Response
    """
    resp = Response()
    resp.success = success
    resp.from_ = from_
    resp.to = to
    resp.amount = amount
    resp.date = date
    resp.rate = rate
    resp.result = result
    resp.client = client
    return resp
