from ninja import Schema


class FriendSchema(Schema):
    username: str


class UserIn(Schema):
    username: str
    password: str


class UserSchema(Schema):
    first_name: str
    last_name: str = None
    username: str = None
    phone_number: str = None
