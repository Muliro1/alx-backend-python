from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

class DeleteUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response({'detail': 'User account deleted.'}, status=status.HTTP_204_NO_CONTENT)
