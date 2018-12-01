
from __future__ import unicode_literals
from users.serializers import UserCreateSerializer, UserUpdateSerializer
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from django.http import Http404
from django.contrib.auth.models import User
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from users.models import Profile, Abilities
from users.serializers import ProfileSerializer, ProfileUpdateSerializer, AbilitiesSerializer


@permission_classes((permissions.AllowAny,))
class UserList(APIView):

    def get(self, request, format=None):

        users = User.objects.all()
        serializer = UserCreateSerializer(users, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):

        serializer = UserCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            user = User.objects.get(username=request.data['username'])

            try:
                profile_data = request.data['profile']
                if profile_data.get('id'):
                    del profile_data['id']
            except KeyError:
                profile_data = {}

            profile_data['user'] = user

            abilities_data = profile_data.pop('abilities')

            profile = Profile.objects.create(**profile_data)

            for abilitiest in abilities_data:
                abilitiest = Abilities.objects.filter(id=abilitiest['id'])
                profile.abilities.add(*abilitiest)
                profile.save()

            profile_serializer = ProfileSerializer(profile)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class UserDetail(APIView):
    authentication_classes = (JSONWebTokenAuthentication,
                              SessionAuthentication)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserCreateSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk=pk)
        serializer = UserUpdateSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()

            # profile_data = request.data['profile']

            # abilities_data = profile_data.pop('abilities')

            # profile = Profile.objects.filter(user=user).update(
            #     **profile_data
            # )

            # profile = Profile.objects.get(user=user)
            # profile.abilities.clear()

            # for abilitiest in abilities_data:
            #     abilitiest = Abilities.objects.filter(id=abilitiest['id'])
            #     profile.abilities.add(*abilitiest)
            #     profile.save()
            
            # profile_serializer = ProfileUpdateSerializer(profile)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileList(APIView):

    def get(self, request, format=None):

        profile = Profile.objects.all()
        serializer = ProfileSerializer(profile, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):

        serializer = ProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class ProfileDetail(APIView):

    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        profile = self.get_object(pk=pk)

        abilities_data = request.data.pop('abilities')

        profile = Profile.objects.filter(pk=pk).update(
            **request.data
        )

        profile = Profile.objects.get(pk=pk)
        profile.abilities.clear()

        for abilitiest in abilities_data:
            abilitiest = Abilities.objects.filter(id=abilitiest['id'])
            profile.abilities.add(*abilitiest)
            profile.save()
        
        profile_serializer = ProfileUpdateSerializer(profile)

        return Response(profile_serializer.data, status=status.HTTP_200_OK)


class AbilitiesList(APIView):

    def get(self, request, format=None):

        abilities = Abilities.objects.all()
        serializer = AbilitiesSerializer(abilities, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):

        serializer = AbilitiesSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class AbilitiesUpdate(APIView):
    def get_object(self, pk):
        try:
            return Abilities.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        abilities = self.get_object(pk)
        serializer = AbilitiesSerializer(abilities)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        abilities = self.get_object(pk=pk)
        serializer = AbilitiesSerializer(abilities, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


