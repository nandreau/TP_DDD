# core/views/dashboard.py
from rest_framework.views import APIView
from rest_framework.response import Response
from core.permission import CanViewDashboardPermission

class DashboardView(APIView):
    permission_classes = [CanViewDashboardPermission]

    def get(self, request, format=None):
        return Response({"message": "Accès autorisé au dashboard !"})
