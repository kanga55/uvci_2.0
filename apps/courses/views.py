from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Course
from .serializers import CourseSerializer


class CourseListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        courses = Course.objects.select_related('department').all()
        # Filtres optionnels par niveau ou filière
        niveau  = request.query_params.get('niveau')
        filiere = request.query_params.get('filiere')
        if niveau:
            courses = courses.filter(niveau=niveau)
        if filiere:
            courses = courses.filter(filiere__icontains=filiere)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not (request.user.is_admin or request.user.is_secretaire):
            return Response({'detail': 'Accès refusé.'}, status=403)
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return None

    def get(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response({'detail': 'Cours introuvable.'}, status=404)
        return Response(CourseSerializer(course).data)

    def put(self, request, pk):
        if not (request.user.is_admin or request.user.is_secretaire):
            return Response({'detail': 'Accès refusé.'}, status=403)
        course = self.get_object(pk)
        if not course:
            return Response({'detail': 'Cours introuvable.'}, status=404)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.is_admin:
            return Response({'detail': 'Accès refusé.'}, status=403)
        course = self.get_object(pk)
        if not course:
            return Response({'detail': 'Cours introuvable.'}, status=404)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)