import pytest
from django.db import IntegrityError

from apps.users.models import Address


@pytest.mark.django_db
def test_user_can_have_multiple_addresses(user):
    Address.objects.create(
        user=user,
        label="Home",
        recipient_name="Test User",
        phone="+2348000000000",
        country="Nigeria",
        state="Lagos",
        city="Lagos",
        street="123 Test Street",
        postal_code="100001",
    )

    Address.objects.create(
        user=user,
        label="Office",
        recipient_name="Test User",
        phone="+2348000000000",
        country="Nigeria",
        state="Lagos",
        city="Lagos",
        street="456 Office Street",
        postal_code="100002",
    )

    assert user.addresses.count() == 2


@pytest.mark.django_db
def test_user_cannot_have_two_default_addresses(user):
    Address.objects.create(
        user=user,
        label="Home",
        recipient_name="Test User",
        phone="+2348000000000",
        country="Nigeria",
        state="Lagos",
        city="Lagos",
        street="123 Test Street",
        is_default=True,
    )

    with pytest.raises(IntegrityError):
        Address.objects.create(
            user=user,
            label="Office",
            recipient_name="Test User",
            phone="+2348000000000",
            country="Nigeria",
            state="Lagos",
            city="Lagos",
            street="456 Office Street",
            is_default=True,
        )