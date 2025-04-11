# core/views/dashboard.py
from rest_framework.views import APIView
from rest_framework.response import Response
from core.permission import HasPermissions

class DashboardView(APIView):
    permission_classes = [HasPermissions]
    required_permissions = ['core.can_view_dashboard']
    permission_logic = 'all'

    def get(self, request, format=None):
        return Response({"message": "Accès autorisé au dashboard !"})
