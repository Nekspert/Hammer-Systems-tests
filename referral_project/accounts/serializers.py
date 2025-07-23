from rest_framework import serializers

from .models import Profile


class PhoneRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
            max_length=15,
            help_text="Телефон в формате +71234567890"
    )


class PhoneVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=4)


class ProfileSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    referrals = serializers.SerializerMethodField()
    used_invite = serializers.CharField(
            source='used_invite.invite_code',
            allow_null=True,
            read_only=True
    )

    class Meta:
        model = Profile
        fields = ['phone_number', 'invite_code', 'used_invite', 'referrals']

    def get_referrals(self, obj):
        qs = obj.referrals.select_related('user')
        return [p.user.phone_number for p in qs]


class UseInviteSerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=6)

    def validate_invite_code(self, value):
        try:
            profile = Profile.objects.get(invite_code=value)
        except Profile.DoesNotExist:
            raise serializers.ValidationError('Такого кода не существует')
        return profile

    def save(self, **kwargs):
        profile: Profile = self.context['request'].user.profile
        inviter: Profile = self.validated_data['invite_code']

        if profile.used_invite is not None:
            raise serializers.ValidationError('Код уже активирован')
        if inviter == profile:
            raise serializers.ValidationError('Нельзя активировать свой код')

        profile.used_invite = inviter
        profile.save()
        return profile
