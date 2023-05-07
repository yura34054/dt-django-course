from app.internal.services import user_service

from .schemas import FriendSchema, UserSchema


def get_user(request):
    return user_service.get_user_info(request.auth)


def update_user(request, user: UserSchema):
    user_service.update_user(request.auth, user.first_name, user.last_name, user.username, user.phone_number)
    return {"message": "info updated successfully"}


def update_phone(request, phone_number: str):
    user_service.update_user_phone(request.auth, phone_number)
    return {"message": "phone number updated"}


def get_interactions(request):
    return user_service.get_interactions(request.auth)


def add_friend(request, friend: FriendSchema):
    user_service.add_friend(request.auth, friend.username)
    return {"message": f"@{friend.username} added to friends"}


def remove_friend(request, friend: FriendSchema):
    user_service.remove_friend(request.auth, friend.username)
    return {"message": f"@{friend.username} removed from friends"}


def list_friends(request):
    return user_service.list_friends(request.auth)
