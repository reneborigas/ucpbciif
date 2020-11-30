from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from rest_framework import serializers
from .models import *
from committees.serializers import CommitteeSerializer, PositionSerializer
from settings.serializers import AppNameSerializer


class AccountTypeSerializer(ModelSerializer):
    class Meta:
        model = AccountType
        fields = "__all__"


class ContentTypeSerializer(ModelSerializer):
    class Meta:
        model = ContentType
        fields = "__all__"


class UserLogsDetailsSerializer(ModelSerializer):
    class Meta:
        model = LogDetails
        fields = "__all__"
        read_only_fields = ("logDetails",)


class UserLogsSerializer(ModelSerializer):
    content_typeText = serializers.CharField(read_only=True)
    logDetails = UserLogsDetailsSerializer(many=True, required=False)
    userName = serializers.CharField(read_only=True)

    def create(self, validated_data):
        logDetails = validated_data.pop("logDetails")
        log = UserLogs.objects.create(**validated_data)

        for detail in logDetails:
            LogDetails.objects.create(**detail, logDetails=log)

        return log

    class Meta:
        model = UserLogs
        fields = "__all__"


class UserAppsSerializer(ModelSerializer):
    installedApps = AppNameSerializer(many=True, required=False)

    class Meta:
        model = UserApps
        fields = "__all__"
        read_only_fields = ("user",)


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"
        read_only_fields = ("user",)


class UserSerializer(ModelSerializer):
    committees = CommitteeSerializer(many=True, required=False)
    appAccess = UserAppsSerializer(many=True, required=False)
    profile = UserProfileSerializer(many=True, required=False)
    fullName = serializers.CharField(read_only=True)
    account_type_text = serializers.CharField(read_only=True)
    committeePosition = serializers.CharField(read_only=True)
    # position  = PositionSerializer(read_only=True)

    committeeId = serializers.CharField(read_only=True)
    positionId = serializers.CharField(read_only=True)

    def create(self, validated_data):
        profile = validated_data.pop("profile")
        user = CustomUser.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()

        if profile:
            for prof in profile:
                UserProfile.objects.create(**prof, user=user)

        return user

    def update(self, instance, validated_data):
        profile = validated_data.get("profile")
        instance.username = validated_data.get("username", instance.username)
        instance.email_address = validated_data.get("email_address", instance.email_address)
        instance.account_type = validated_data.get("account_type", instance.account_type)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.save()

        keep_profile = []
        if profile:
            for prof in profile:
                if "id" in prof.keys():
                    if UserProfile.objects.filter(id=prof["id"]).exists():
                        e = UserProfile.objects.get(id=prof["id"])
                        e.name = prof.get("name", e.name)
                        e.age = prof.get("age", e.age)
                        e.birthdate = prof.get("birthdate", e.birthdate)
                        e.birthplace = prof.get("birthplace", e.birthplace)
                        e.gender = prof.get("gender", e.gender)
                        e.profile_picture = prof.get("profile_picture", e.profile_picture)
                        e.digital_signature = prof.get("digital_signature", e.digital_signature)
                        e.save()
                        keep_profile.append(e.id)
                    else:
                        continue
                else:
                    e = UserProfile.objects.create(**prof, user=instance)
                    keep_profile.append(e.id)

            for prof in instance.profile.all():
                if prof.id not in keep_profile:
                    prof.delete()

        return instance

    class Meta:
        model = CustomUser
        fields = "__all__"
