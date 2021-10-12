class UnprocessableEntity(Exception):
    def __init__(self, message, status=422, payload=None):
        self.message = message
        self.status = status
        self.payload = payload


class ServiceUnavailable(Exception):
    def __init__(self, message, status=503, payload=None):
        self.message = message
        self.status = status
        self.payload = payload


class NotFound(Exception):
    def __init__(self, message, status=404, payload=None):
        self.message = message
        self.status = status
        self.payload = payload
