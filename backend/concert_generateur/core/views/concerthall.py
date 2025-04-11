# # core/views/concerthall.py
# from rest_framework.generics import RetrieveAPIView
# from core.models.concerthall import ConcertHall
# from core.serializers.concerthall import ConcertHallSerializer
# from core.permissions import HasPermissions

# class ConcertHallReadOnlyView(RetrieveAPIView):
#     queryset = ConcertHall.objects.all()
#     serializer_class = ConcertHallSerializer
#     permission_classes = [HasPermissions]
#     required_permissions = ['core.view_concerthall']
#     permission_logic = 'all'
#     lookup_field = 'id'
