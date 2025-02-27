from fastapi import HTTPException, status


class ApplicationException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class WalletDoesntExistHTTPException(ApplicationException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Wallet not found"


class NotEnoughFundsHTTPException(ApplicationException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Not enough funds in the wallet"
