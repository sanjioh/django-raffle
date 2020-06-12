from datetime import datetime

import pytest
from django.shortcuts import reverse
from django.utils.timezone import make_aware

url = reverse('play')


WIN_RESPONSE = {'data': {'winner': True, 'prize': {'code': 'five-percent-discount', 'name': 'Sconto del 5%'}}}
LOSS_RESPONSE = {'data': {'winner': False, 'prize': None}}
INACTIVE_RESPONSE = {
    'error': {
        'status': '422',
        'title': 'Contest is not active',
        'detail': 'The contest with code C0001 is not active.',
    },
}
MISSING_RESPONSE = {
    'error': {'status': '400', 'title': 'Missing contest', 'detail': 'Contest must be provided as query parameter.'},
}
NOT_FOUND_RESPONSE = {
    'error': {'status': '404', 'title': 'Contest not found', 'detail': 'Contest code C0001 not found.'},
}


@pytest.mark.django_db
def test_contest_api_success(apiclient, contest, freezer):
    query_params = {'contest': 'C0001'}
    freezer.move_to(make_aware(datetime(2020, 6, 12, 0, 31, 18)))
    response = apiclient.get(url, query_params)
    assert response.status_code == 200
    assert response.json() == LOSS_RESPONSE

    freezer.move_to(make_aware(datetime(2020, 6, 12, 0, 31, 19)))
    response = apiclient.get(url, query_params)
    assert response.status_code == 200
    assert response.json() == WIN_RESPONSE

    freezer.move_to(make_aware(datetime(2020, 6, 12, 0, 31, 20)))
    response = apiclient.get(url, query_params)
    assert response.status_code == 200
    assert response.json() == LOSS_RESPONSE


@pytest.mark.django_db
def test_contest_api_failure_contest_inactive(apiclient, contest, freezer):
    query_params = {'contest': 'C0001'}
    for dt in (make_aware(datetime(2020, 6, 10)), make_aware(datetime(2020, 6, 20))):
        freezer.move_to(dt)
        response = apiclient.get(url, query_params)
        assert response.status_code == 422
        assert response.json() == INACTIVE_RESPONSE


@pytest.mark.django_db
def test_contest_api_failure_contest_missing_query_param(apiclient):
    response = apiclient.get(url)
    assert response.status_code == 400
    assert response.json() == MISSING_RESPONSE


@pytest.mark.django_db
def test_contest_api_failure_contest_not_found(apiclient):
    query_params = {'contest': 'C0001'}
    response = apiclient.get(url, query_params)
    assert response.status_code == 404
    assert response.json() == NOT_FOUND_RESPONSE
