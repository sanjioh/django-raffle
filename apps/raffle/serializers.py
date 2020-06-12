from rest_framework import serializers


class ContestSerializer(serializers.Serializer):
    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        winner = obj.play()
        if winner:
            return {'winner': winner, 'prize': {'code': obj.prize.code, 'name': obj.prize.name}}
        return {'winner': winner, 'prize': None}
