from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UserSerializer

class CurrentUserView(APIView):
    serializer_class = UserSerializer

    def get(self, request):
        return Response(self.serializer_class(request.user).data)
