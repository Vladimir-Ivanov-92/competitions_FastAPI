class ResponseError(Exception):
    """
    Собственный класс исключения для вывода ошибок
    """

    def __init__(self, status, message, e=None):
        self.status = status
        self.message = f"{message}"
        self.e = e
