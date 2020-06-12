from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import DatabaseError, models, transaction
from django.utils.functional import cached_property
from django.utils.timezone import make_aware, now
from django.utils.translation import gettext as _

SECONDS_IN_DAY = 86400
MICROSECONDS_IN_DAY = SECONDS_IN_DAY * 1000 * 1000
MAX_PRIZES_PER_DAY = SECONDS_IN_DAY - 1


def midnight(date):
    return make_aware(datetime.combine(date, datetime.min.time()))


class Contest(models.Model):
    code = models.CharField(_('code'), max_length=5, unique=True)
    name = models.CharField(_('name'), max_length=256)
    start = models.DateField(_('start'))
    end = models.DateField(_('end'))
    prize = models.ForeignKey('Prize', verbose_name=_('prize'), related_name='contests', on_delete=models.PROTECT)
    win_at = models.DateTimeField(_('win at'))

    class Meta:
        verbose_name = _('contest')
        verbose_name_plural = _('contests')

    def __str__(self):
        return f'{self.code}'

    def clean(self):
        if self.start >= self.end:
            raise ValidationError(_('Start date must be earlier than end date.'))
        self.win_at = midnight(self.start) + self.win_period

    @property
    def is_active(self):
        today = now().date()
        return self.start <= today <= self.end

    def play(self):
        if now() < self.win_at:
            return False
        try:
            self.update_win_at()
        except DatabaseError:
            return False
        return True

    def update_win_at(self):
        with transaction.atomic():
            self = Contest.objects.select_for_update(nowait=True).get(pk=self.pk)
            self.win_at = self.next_win_at
            self.save()

    @cached_property
    def next_win_at(self):
        next_win_at = self.win_at + self.win_period
        if next_win_at.date() > self.win_at.date():
            next_win_at = midnight(next_win_at.date()) + self.win_period
        return next_win_at

    @cached_property
    def win_period(self):
        num_periods = self.prize.perday + 1
        extra_us = MICROSECONDS_IN_DAY % num_periods
        period_us = (MICROSECONDS_IN_DAY - extra_us) / num_periods
        return timedelta(microseconds=int(period_us))


class Prize(models.Model):
    code = models.CharField(_('code'), max_length=32, unique=True)
    name = models.CharField(_('name'), max_length=256)
    perday = models.PositiveIntegerField(
        _('perday'), validators=[MinValueValidator(1), MaxValueValidator(MAX_PRIZES_PER_DAY)],
    )

    class Meta:
        verbose_name = _('prize')
        verbose_name_plural = _('prizes')

    def __str__(self):
        return f'{self.code}'
