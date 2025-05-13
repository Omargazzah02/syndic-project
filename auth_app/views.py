from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner, IsManager, IsAdmin
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError







class LoginView(APIView):
    def post(self, request):
        # Vérifie que les données nécessaires sont présentes dans la requête
        username = request.data.get("username")
        password = request.data.get("password")

        # Vérifie si le nom d'utilisateur et le mot de passe sont fournis
        if not username or not password:
            return Response({'error': 'Nom d\'utilisateur et mot de passe sont requis.'}, status=400)

        try:
            user = authenticate(username=username, password=password)
        except Exception as e:
            return Response({'error': f'Erreur lors de l\'authentification : {str(e)}'}, status=500)

        if user is None:
            return Response({'error': 'Nom d\'utilisateur ou mot de passe incorrect.'}, status=400)

        try:
            refresh = RefreshToken.for_user(user)
        except Exception as e:
            return Response({'error': f'Erreur lors de la génération du token : {str(e)}'}, status=500)

        return Response({
            "access": str(refresh.access_token),
            "role": user.role
        })



class ModifyPasswordView(APIView):
    permission_classes = [IsAuthenticated,IsOwner]  # Or your custom IsOwner permission

    def put(self, request):
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        
        if not old_password or not new_password:
            return Response({"error": "Ancien mot de passe et nouveau mot de passe requis."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not request.user.check_password(old_password):
            return Response({"error": "L'ancien mot de passe est incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(new_password, user=request.user)
        except ValidationError as e:
            return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        request.user.set_password(new_password)
        request.user.save()

        return Response({"message": "Mot de passe modifié avec succès."}, status=status.HTTP_200_OK)





class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        data = request.data

        # Extract fields from request
        username = data.get("username")
        email = data.get("email")
        phone = data.get("phone")
        first_name = data.get("first_name")
        last_name = data.get("last_name")

        # Optional: validate required fields
        if not username or  not email:
            return Response(
                {"error": "First name, last name, and email are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update user fields
        user.username = username
        user.email = email
        user.phone = phone 
        user.first_name = first_name
        user.last_name = last_name

        user.save()

        return Response(
            {"message": "Profile updated successfully."},
            status=status.HTTP_200_OK
        )

    



class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
