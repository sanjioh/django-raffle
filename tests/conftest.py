from datetime import date

import pytest
from rest_framework.test import APIClient

from apps.raffle.models import Contest, Prize


@pytest.fixture
def contest(prize):
    contest = Contest(
        code='C0001', name='Vinci uno sconto', start=date(2020, 6, 12), end=date(2020, 6, 15), prize=prize,
    )
    contest.clean()
    contest.save()
    return contest


@pytest.fixture
def prize():
    return Prize.objects.create(code='five-percent-discount', name='Sconto del 5%', perday=45)


@pytest.fixture
def apiclient():
    return APIClient()
