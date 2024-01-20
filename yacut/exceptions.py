class InvalidRequest(Exception):
    status_code = 400

    def __init__(self, message):
        super().__init__()
        self.message = message
        self.status_code = self.status_code

    def to_dict(self):
        return dict(message=self.message)