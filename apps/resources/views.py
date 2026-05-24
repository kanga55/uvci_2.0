from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Sequence, Resource
from .serializers import SequenceSerializer, ResourceSerializer


class SequenceListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cours_id = request.query_params.get('cours')
        sequences = Sequence.objects.select_related('cours').all()
        if cours_id:
            sequences = sequences.filter(cours_id=cours_id)
        return Response(SequenceSerializer(sequences, many=True).data)

    def post(self, request):
        if not (request.user.is_admin or request.user.is_secretaire):
            return Response({'detail': 'Accès refusé.'}, status=403)
        serializer = SequenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResourceListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        resources = Resource.objects.select_related(
            'sequence', 'enseignant'
        ).all()
        # Filtres optionnels
        enseignant_id = request.query_params.get('enseignant')
        sequence_id   = request.query_params.get('sequence')
        if enseignant_id:
            resources = resources.filter(enseignant_id=enseignant_id)
        if sequence_id:
            resources = resources.filter(sequence_id=sequence_id)
        return Response(ResourceSerializer(resources, many=True).data)

    def post(self, request):
        if not (request.user.is_admin or request.user.is_secretaire):
            return Response({'detail': 'Accès refusé.'}, status=403)
        serializer = ResourceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResourceDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Resource.objects.get(pk=pk)
        except Resource.DoesNotExist:
            return None

    def get(self, request, pk):
        resource = self.get_object(pk)
        if not resource:
            return Response({'detail': 'Ressource introuvable.'}, status=404)
        return Response(ResourceSerializer(resource).data)

    def put(self, request, pk):
        if not (request.user.is_admin or request.user.is_secretaire):
            return Response({'detail': 'Accès refusé.'}, status=403)
        resource = self.get_object(pk)
        if not resource:
            return Response({'detail': 'Ressource introuvable.'}, status=404)
        serializer = ResourceSerializer(resource, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.is_admin:
            return Response({'detail': 'Accès refusé.'}, status=403)
        resource = self.get_object(pk)
        if not resource:
            return Response({'detail': 'Ressource introuvable.'}, status=404)
        resource.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)