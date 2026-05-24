from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Sum
from .models import Activity, AnneeAcademique
from .serializers import ActivitySerializer, AnneeAcademiqueSerializer
from apps.teachers.models import Teacher


class AnneeAcademiqueListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        annees = AnneeAcademique.objects.all()
        return Response(AnneeAcademiqueSerializer(annees, many=True).data)

    def post(self, request):
        if not request.user.is_admin:
            return Response({'detail': 'Accès refusé.'}, status=403)
        serializer = AnneeAcademiqueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivityListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        activities = Activity.objects.select_related(
            'enseignant', 'resource'
        ).all()
        # Filtres
        enseignant_id    = request.query_params.get('enseignant')
        annee_academique = request.query_params.get('annee')
        if enseignant_id:
            activities = activities.filter(enseignant_id=enseignant_id)
        if annee_academique:
            activities = activities.filter(annee_academique=annee_academique)
        return Response(ActivitySerializer(activities, many=True).data)

    def post(self, request):
        if not (request.user.is_admin or request.user.is_secretaire):
            return Response({'detail': 'Accès refusé.'}, status=403)
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VolumeHoraireView(APIView):
    """
    GET /api/activities/volume/?annee=2025-2026
    Retourne le volume horaire total par enseignant pour une année.
    C'est la vue clé pour les tableaux de bord et les états de paiement.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        annee = request.query_params.get('annee', '')

        teachers = Teacher.objects.prefetch_related('activities').all()
        result = []

        for teacher in teachers:
            activities = teacher.activities.all()
            if annee:
                activities = activities.filter(annee_academique=annee)

            total_heures = activities.aggregate(
                total=Sum('heures')
            )['total'] or 0

            result.append({
                'enseignant_id':  teacher.id,
                'enseignant_nom': teacher.get_full_name(),
                'grade':          teacher.get_grade_display(),
                'statut':         teacher.get_statut_display(),
                'taux_horaire':   float(teacher.taux_horaire),
                'total_heures':   float(total_heures),
                'montant_du':     float(total_heures) * float(teacher.taux_horaire),
            })

        # Trier par total d'heures décroissant
        result.sort(key=lambda x: x['total_heures'], reverse=True)
        return Response(result)