from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from users.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id',
            'hours',
            'habilities',
            'user',
            'phone',
            'photo',
            'coins',
        ]


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id',
            'hours',
            'habilities',
            'user',
            'phone',
            'photo',
            'coins',
        ]
    def update(self, instance, validated_data):
        instance.hours = validated_data.get('hours', instance.hours)
        instance.habilities = validated_data.get('habilities', instance.habilities)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.coins = validated_data.get('coins', instance.coins)
        instance.save()
        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 
            'username',
            'email',
            'password',
            'profile',
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

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'profile',
        ]

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.password = make_password(validated_data.get('password',
                                                             instance.password
                                                            ))
        instance.save()
        return instance