from app.infrastructure.exceptions.base import AppException


class PollDoesNotExist(AppException):
    def __init__(self):
        super().__init__("Такой опрос не существует.")

class YouCantDeletePollWhichNotBelongToYou(AppException):
    def __init__(self):
        super().__init__("Вы не можете удалить опрос который вам не принадлежит.")

class PollVariantDoesNotExist(AppException):
    def __init__(self):
        super().__init__("Такого варианта в опросе не существует.")

class YouCantDeletePollVariantWhichNotBelongToYou(AppException):
    def __init__(self):
        super().__init__("Вы не можете удалить вариант опроса который вам не принадлежит.")
