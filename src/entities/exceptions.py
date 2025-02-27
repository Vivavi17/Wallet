class EntitiesException(Exception): ...


class NotEnoughFundsException(EntitiesException):
    message = "Not Enough Funds"
