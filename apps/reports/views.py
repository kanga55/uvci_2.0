from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Sum
from .models import Report
from .serializers import ReportSerializer
from apps.teachers.models import Teacher
from apps.activities.models import Activity


class ReportListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        reports = Report.objects.select_related('enseignant', 'genere_par').all()
        return Response(ReportSerializer(reports, many=True).data)


class GenerateReportView(APIView):
    """
    POST /api/reports/generate/
    Génère et sauvegarde un rapport récapitulatif.
    Corps : { "type_report": "paiement", "annee_academique": "2025-2026" }
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if not (request.user.is_admin or request.user.is_secretaire):
            return Response({'detail': 'Accès refusé.'}, status=403)

        type_report      = request.data.get('type_report', 'global')
        annee_academique = request.data.get('annee_academique', '')
        enseignant_id    = request.data.get('enseignant_id')

        teachers = Teacher.objects.all()
        if enseignant_id:
            teachers = teachers.filter(pk=enseignant_id)

        reports_crees = []

        for teacher in teachers:
            activities = Activity.objects.filter(
                enseignant=teacher,
                annee_academique=annee_academique
            )
            total_heures = activities.aggregate(
                total=Sum('heures')
            )['total'] or 0
            montant_total = float(total_heures) * float(teacher.taux_horaire)

            report = Report.objects.create(
                enseignant=teacher,
                type_report=type_report,
                annee_academique=annee_academique,
                total_heures=total_heures,
                montant_total=montant_total,
                genere_par=request.user
            )
            reports_crees.append(report)

        return Response(
            ReportSerializer(reports_crees, many=True).data,
            status=status.HTTP_201_CREATED
        )