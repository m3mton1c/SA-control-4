class CustomExceptionA(Exception):
    def __init__(self):
        self.status_code = 400
        self.detail = "Ошибка типа A (не выполнено условие)"


class CustomExceptionB(Exception):
    def __init__(self):
        self.status_code = 404
        self.detail = "Ресурс не найден"