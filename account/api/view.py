from account.api.serializers import (
    LoginSerializer, RegisterSerializer, UserSerializer
)
from rest_framework import status, permissions
from account.models import UserPublicKey, User
from account.api.serializers import UserPublicKeySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


class RegisterView(APIView):    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Registrazione avvenuta con successo."},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                user = User.objects.get(
                    email=serializer.validated_data['email']
                )
                print(serializer.validated_data)
                token, created = Token.objects.get_or_create(
                    user=user
                )
                return Response(
                    {"message": "Login avvenuto con successo.",
                        "token": token.key},
                    status=status.HTTP_200_OK
                )
            return Response(
                {"message": f"Errore durante il login: {serializer.errors}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {"message": f"Errore durante il login: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SetPublicKeyUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = UserPublicKeySerializer(data=request.data)
        if serializer.is_valid():
            public_key = serializer.validated_data['public_key']
            key_id = serializer.validated_data['key_id']
            obj, created = UserPublicKey.objects.update_or_create(
                user=request.user,
                defaults={'public_key': public_key, 'key_id': key_id}
            )
            return Response({'status': 'ok', 'created': created})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetPublicKeyUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            username = request.query_params.get('username')
            print(username)
            user = User.objects.get(username=username)
            print(user)
            public_key = UserPublicKey.objects.get(user=user)
            print(public_key.key_id)
            key_id = public_key.key_id
            return Response(
                {'public_key': public_key.public_key, 'key_id': key_id},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class InfoUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            serializer_user = UserSerializer(instance=user)
            return Response(
                serializer_user.data,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'message': f'Errore nel ricevere informazioni '
                               f'dell\'utente: {str(e)}'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ListUsers(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
