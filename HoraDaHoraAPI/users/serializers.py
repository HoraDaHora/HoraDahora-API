from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from users.models import Profile, Abilities, Availability, Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id',
            'owner',
            'interested',
            'date',
            'status',
            'hours',
        ]


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = [
            'id',
            'user',
            'date',
        ]


class AbilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Abilities
        fields = [
            'id',
            'name',
        ]


class ProfileSerializer(serializers.ModelSerializer):
    abilities = AbilitiesSerializer(many=True, required=False)
    class Meta:
        model = Profile
        fields = [
            'id',
            'hours',
            'abilities',
            'user',
            'phone',
            'photo',
            'coins',
            'points',
        ]


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id',
            'hours',
            'abilities',
            'user',
            'phone',
            'photo',
            'coins',
            'points',
        ]
    def update(self, instance, validated_data):
        abilities_data = validated_data.pop('abilities')
        instance.hours = validated_data.get('hours', instance.hours)
        instance.abilities.remove()
        instance.phone = validated_data.get('phone', instance.phone)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.coins = validated_data.get('coins', instance.coins)

        # for abilities in abilities_data:
        #     abilities, created = Abilities.objects.get_or_create(id=abilities['id'])
        #     instance.abilities.set(abilities)
        instance.save()
        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    availability = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = [
            'id', 
            'username',
            'email',
            'password',
            'profile',
            'availability',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            password=make_password(validated_data['password'])
        )
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    availability = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'profile',
            'availability',
        ]

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.password = make_password(validated_data.get('password',
                                                             instance.password
                                                            ))
        instance.save()
        return instance

class UserDetailsSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    availability = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'profile',
            'availability',
        ]