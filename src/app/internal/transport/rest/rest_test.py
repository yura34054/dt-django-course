import pytest

from django.urls import reverse
from app.internal.services.user_service import create_user, update_user_phone


@pytest.mark.django_db
def test_view(client):
    url = reverse('me', args=['71234567890'])
    response = client.get(url)
    assert response.json() == {}
    assert response.status_code == 403

    create_user(1, 'first_name')

    response = client.get(url)
    assert response.json() == {}
    assert response.status_code == 403

    update_user_phone(1, '71234567890')

    response = client.get(url)
    assert response.json() == {
        "first_name": "first_name",
        "last_name": "",
        "username": "",
        "phone_number": "71234567890",
    }
    assert response.status_code == 200
