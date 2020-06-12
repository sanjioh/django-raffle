from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny

from apps.raffle.exceptions import ContestInactiveError, ContestMissingError, ContestNotFoundError
from apps.raffle.models import Contest
from apps.raffle.serializers import ContestSerializer


class ContestAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer

    def get_object(self):
        code = self.request.query_params.get('contest')
        if not code:
            raise ContestMissingError
        try:
            contest = self.get_queryset().get(code=code)
        except Contest.DoesNotExist:
            raise ContestNotFoundError(detail=f'Contest code {code} not found.')
        if not contest.is_active:
            raise ContestInactiveError(detail=f'The contest with code {contest.code} is not active.')
        return contest
