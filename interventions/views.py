from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Intervention
from .serializers import InterventionSerializer
from rest_framework.permissions import IsAuthenticated

class InterventionListByResidenceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, residence_id):
        status_param = request.query_params.get('status')

        interventions = Intervention.objects.filter(user=request.user, residence_id=residence_id)
        if status_param:
            interventions = interventions.filter(status=status_param)

        serializer = InterventionSerializer(interventions.order_by('-created_at'), many=True)
        return Response(serializer.data)



class CreateInterventionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = InterventionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # 🟢 Set user manually here
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

