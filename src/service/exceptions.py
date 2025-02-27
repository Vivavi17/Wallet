class ServiceException(Exception): ...


class WalletDoesntExistServiceException(ServiceException):
    message = "Wallet doesnt exist"
