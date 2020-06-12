from datetime import datetime, timedelta

import pytest
from django.utils.timezone import make_aware

NOW = make_aware(datetime(2020, 6, 13, 10, 20))
WIN_PERIOD = timedelta(seconds=1878, microseconds=260869)


@pytest.mark.django_db
@pytest.mark.freeze_time(NOW)
def test_active(contest, freezer):
    assert contest.is_active
    freezer.move_to(make_aware(datetime(2020, 6, 11, 10, 20)))
    assert not contest.is_active
    freezer.move_to(make_aware(datetime(2020, 6, 16, 10, 20)))
    assert not contest.is_active


@pytest.mark.django_db
def test_update_win_at(contest):
    assert contest.win_at == make_aware(datetime(2020, 6, 12)) + WIN_PERIOD
    next_win_at = contest.next_win_at
    contest.update_win_at()
    contest.refresh_from_db()
    assert contest.win_at == next_win_at


@pytest.mark.django_db
def test_next_win_at(contest):
    assert contest.next_win_at == contest.win_at + WIN_PERIOD
    del contest.next_win_at
    contest.win_at += WIN_PERIOD * 45
    contest.save()
    assert contest.win_at == make_aware(datetime(2020, 6, 12, 23, 59, 59, 999974))
    assert contest.next_win_at == make_aware(datetime(2020, 6, 13)) + WIN_PERIOD


@pytest.mark.django_db
def test_win_period(contest, prize):
    assert contest.win_period == WIN_PERIOD
    del contest.win_period
    prize.perday = 1
    prize.save()
    assert contest.win_period == timedelta(seconds=43200)
