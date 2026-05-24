from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Teacher, Department
from .serializers import TeacherSerializer, DepartmentSerializer


class IsAdminOrSecretaire(permissions.BasePermission):
    """Permission : seuls Admin et Secrétaire peuvent modifier."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_secretaire
        )


class DepartmentListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not (request.user.is_admin):
            return Response({'detail': 'Accès refusé.'}, status=403)
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherListCreateView(APIView):
    permission_classes = [IsAdminOrSecretaire]

    def get(self, request):
        teachers = Teacher.objects.select_related('department').all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherDetailView(APIView):
    permission_classes = [IsAdminOrSecretaire]

    def get_object(self, pk):
        try:
            return Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            return None

    def get(self, request, pk):
        teacher = self.get_object(pk)
        if not teacher:
            return Response({'detail': 'Enseignant introuvable.'}, status=404)
        return Response(TeacherSerializer(teacher).data)

    def put(self, request, pk):
        teacher = self.get_object(pk)
        if not teacher:
            return Response({'detail': 'Enseignant introuvable.'}, status=404)
        serializer = TeacherSerializer(teacher, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.is_admin:
            return Response({'detail': 'Accès refusé.'}, status=403)
        teacher = self.get_object(pk)
        if not teacher:
            return Response({'detail': 'Enseignant introuvable.'}, status=404)
        teacher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)