from django.contrib.auth.models import User
from rest_framework import serializers
from advertisements.models import Advertisement

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')

class AdvertisementSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'text', 'creator', 'status', 'created_at')
        read_only_fields = ('id', 'creator', 'created_at')

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        user = self.context["request"].user
        new_status = data.get('status')

        if new_status == Advertisement.OPEN:
            open_ads_count = Advertisement.objects.filter(
                author=user,
                status=Advertisement.OPEN
            ).count()

            if self.instance:
                open_ads_count = Advertisement.objects.filter(
                    author=user,
                    status=Advertisement.OPEN
                ).exclude(pk=self.instance.pk).count()

            if open_ads_count >= 10:
                raise serializers.ValidationError(
                    f"У вас уже есть {open_ads_count} открытых объявлений. Нельзя создать более 10."
                )

        return data