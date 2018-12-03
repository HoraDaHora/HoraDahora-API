
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
from users.models import Profile, Abilities, Availability
from users.serializers import ProfileSerializer, ProfileUpdateSerializer, AbilitiesSerializer, AvailabilitySerializer
from rest_framework import mixins, status, viewsets


@permission_classes((permissions.AllowAny,))
class UserList(APIView):
    def get(self, request, format=None):
        """
        API endpoint that list all users.
        ---
        Body example:
        ```
        [
            {
                "id": 1,
                "username": "user1",
                "email": "top@person.com",
                "profile": {
                    "id": 1,
                    "hours": 5,
                    "abilities": [
                        {
                            "id": 1,
                            "name": "Gamificacao"
                        }
                    ],
                    "user": 1,
                    "phone": 10,
                    "photo": null,
                    "coins": 0
                }
            },
            {
                "id": 2,
                "username": "Silverson",
                "email": "silver@son.com",
                "profile": {
                "id": 2,
                "hours": 10,
                "abilities": [
                    {
                    "id": 1,
                    "name": "teste2"
                    }
                ],
                "user": 2,
                "phone": 96362067,
                "photo": null,
                "coins": 0
                }
            }
        ]
        ```
        """
        users = User.objects.all()
        serializer = UserCreateSerializer(users, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        """
          API endpoint that create the users.
          ---
          Body example:
          ```
          {
            "username": "user2",
            "email": "top@person.com",
            "password": "teste",
            "profile": {
                "id": 1,
                "hours": 15,
                "abilities": [
                    {
                        "id": 1,
                        "name": "Gamificacao"
                    }
                ],
                "user": 1,
                "phone": 990987610,
                "photo": null,
                "coins": 0
            }
          }
          ```
          Response example:
          ```
          {
            "id": 1,
            "username": "user2",
            "email": "top@person.com",
            "profile": {
                "id": 1,
                "hours": 15,
                "abilities": [
                    {
                        "id": 1,
                        "name": "Gamificacao"
                    }
                ],
                "user": 1,
                "phone": 990987610,
                "photo": null,
                "coins": 0
            }
          }
          ```
        """

        serializer = UserCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            user = User.objects.get(username=request.data['username'])
            
            abilities_data = ''
            try:
                profile_data = request.data['profile']
                if profile_data.get('id'):
                    del profile_data['id']
                    abilities_data = profile_data.pop('abilities')
            except KeyError:
                profile_data = {}

            profile_data['user'] = user

            profile = Profile.objects.create(**profile_data)

            for abilitiest in abilities_data:
                abilitiest = Abilities.objects.filter(id=abilitiest['id'])
                profile.abilities.add(*abilitiest)
                profile.save()

            profile_serializer = ProfileSerializer(profile)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((permissions.AllowAny,))
class UserDetail(APIView):
    authentication_classes = (JSONWebTokenAuthentication,
                              SessionAuthentication)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
          API endpoint that get specific user.
          ---
          Body example:
          ```
          {
            "id": 1,
            "username": "user2",
            "email": "top@person.com",
            "profile": {
                "id": 1,
                "hours": 5,
                "abilities": [
                    {
                        "id": 1,
                        "name": "Gamificacao"
                    }
                ],
                "user": 1,
                "phone": 10,
                "photo": null,
                "coins": 0
            }
          }
          ```
        """
        user = self.get_object(pk)
        serializer = UserCreateSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
          API endpoint that update the users.
          ---
          Body example:
          ```
          {
            "username": "user2",
            "email": "top@person.com",
            "password": "teste"
          }
          ```
          Response example:
          ```
          {
            "id": 1,
            "username": "user2",
            "email": "top@person.com",
            "profile": {
                "id": 1,
                "hours": 5,
                "abilities": [
                    {
                        "id": 1,
                        "name": "Gamificacao"
                    }
                ],
                "user": 1,
                "phone": 10,
                "photo": null,
                "coins": 0
            }
          }
          ```
        """
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
        """
        API endpoint that delete users.
        """
        user = self.get_object(pk)
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileList(APIView):

    def get(self, request, format=None):
        """
        API endpoint that list all profiles.
        ---
        Body example:
        ```
        [
            {
                "id": 1,
                "hours": 5,
                "abilities": [
                    {
                        "id": 1,
                        "name": "Gamificacao"
                    }
                ],
                "user": 1,
                "phone": 10,
                "photo": null,
                "coins": 0
            },
            {
                "id": 2,
                "hours": 10,
                "abilities": [
                    {
                    "id": 1,
                    "name": "teste2"
                    }
                ],
                "user": 2,
                "phone": 96362067,
                "photo": null,
                "coins": 0
            }
        ]
        ```
        """

        profile = Profile.objects.all()
        serializer = ProfileSerializer(profile, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        """
          API endpoint that create the profiles.
          ---
          Body example:
          ```
          {
            "hours": 15,
            "abilities": [
                {
                    "id": 1,
                    "name": "Gamificacao"
                }
            ],
            "user": 1,
            "phone": 990987610,
            "photo": null,
            "coins": 0
          }
          ```
          Response example:
          ```
          {
            "id": 1,
            "hours": 15,
            "abilities": [
                {
                    "id": 1,
                    "name": "Gamificacao"
                }
            ],
            "user": 1,
            "phone": 990987610,
            "photo": null,
            "coins": 0
          }
          ```
        """

        serializer = ProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((permissions.AllowAny,))
class ProfileDetail(APIView):

    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        API endpoint that list all profiles.
        ---
        Body example:
        ```
        [
            {
                "id": 1,
                "hours": 5,
                "abilities": [
                    {
                        "id": 1,
                        "name": "Gamificacao"
                    }
                ],
                "user": 1,
                "phone": 10,
                "photo": null,
                "coins": 0
            }
        ]
        ```
        """
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
          API endpoint that update the profiles.
          ---
          Body example:
          ```
          {
            "hours": 15,
            "abilities": [
                {
                    "id": 1,
                    "name": "Gamificacao"
                }
            ],
            "user": 1,
            "phone": 990987610,
            "photo": null,
            "coins": 0
          }
          ```
          Response example:
          ```
          {
            "id": 1,
            "hours": 15,
            "abilities": [
                {
                    "id": 1,
                    "name": "Gamificacao"
                }
            ],
            "user": 1,
            "phone": 990987610,
            "photo": null,
            "coins": 0
          }
          ```
        """
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
        """
        API endpoint that list all abilities.
        ---
        Body example:
        ```
        [
            {
                "id": 1,
                "name": "gamificacao"
            },
            {
                "id": 2,
                "name": "felicidade"
            }
        ]
        ```
        """

        abilities = Abilities.objects.all()
        serializer = AbilitiesSerializer(abilities, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        """
          API endpoint that post the abilities.
          ---
          Body example:
          ```
          {
            "name": "felicidade"
          }
          ```
          Response example:
          ```
          {
            "id": 3,
            "name": "felicidade"
          }
          ```
        """
        serializer = AbilitiesSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((permissions.AllowAny,))
class AbilitiesUpdate(APIView):
    def get_object(self, pk):
        try:
            return Abilities.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        API endpoint that list all abilities.
        ---
        Body example:
        ```
        [
            {
                "id": 1,
                "name": "gamificacao"
            }
        ]
        ```
        """
        abilities = self.get_object(pk)
        serializer = AbilitiesSerializer(abilities)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
          API endpoint that update the profiles.
          ---
          Body example:
          ```
          {
            "id": 3,
            "name": "felicidade"
          }
          ```
          Response example:
          ```
          {
            "id": 3,
            "name": "felicidade"
          }
          ```
        """
        abilities = self.get_object(pk=pk)
        serializer = AbilitiesSerializer(abilities, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AvailabilityList(APIView):

    def get(self, request, format=None):
        availability = Availability.objects.all()
        serializer = AvailabilitySerializer(availability, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AvailabilitySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((permissions.AllowAny,))
class AvailabilityUpdate(APIView):
    def get_object(self, pk):
        try:
            return Availability.objects.get(pk=pk)
        except Availability.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        availability = self.get_object(pk)
        serializer = AvailabilitySerializer(availability)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        availability = self.get_object(pk=pk)
        serializer = AvailabilitySerializer(availability, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((permissions.AllowAny,))
class AvailabilityUser(APIView):
    def get_object(self, pk):
        try:
            return Availability.objects.filter(user=pk)
        except Availability.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        availability = self.get_object(pk)
        serializer = AvailabilitySerializer(availability, many=True)
        return Response(serializer.data)


