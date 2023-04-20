class ValidationError(Exception):
    pass


class AlreadyInFriendsError(ValidationError):
    def __init__(self, username):
        self.message = f"{username} already in friends"
        super().__init__(self.message)


class UserNotFoundError(ValidationError):
    def __init__(self, username):
        self.message = f"User {username} not found"
        super().__init__(self.message)


class NotInFriendsError(ValidationError):
    def __init__(self, username):
        self.message = f"@{username} not in friends"
        super().__init__(self.message)


class AccountAlreadyExistsError(ValidationError):
    def __init__(self, account_name):
        self.message = f'Account "{account_name}" already exists'
        super().__init__(self.message)


class AccountNotFoundError(ValidationError):
    def __init__(self, account_name):
        self.message = f'No account "{account_name}" found'
        super().__init__(self.message)


class NotEnoughMoneyError(ValidationError):
    def __init__(self):
        self.message = "Not enough money"
        super().__init__(self.message)


class NegativeMoneyAmountError(ValidationError):
    def __init__(self):
        self.message = "You can't send negative amount of money"
        super().__init__(self.message)


class CardNotFoundError(ValidationError):
    def __init__(self, card_id):
        self.message = f'No card "{card_id}" found'
        super().__init__(self.message)


class CardPermissionError(ValidationError):
    def __init__(self, card_id):
        self.message = f'You don\'t own card "{card_id}"'
        super().__init__(self.message)
