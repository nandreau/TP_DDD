from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.permission import HasPermissions
from core.services import generate_event_proposal
from core.models.concerthall import ConcertHall
from core.models.artists import Artist
from core.models.event import Event
from django.utils.timezone import make_aware
from datetime import datetime
from dateutil.parser import parse as parse_datetime


class GenerateEventView(APIView):
    permission_classes = [HasPermissions]
    allowed_roles = ['admin', 'organizer']
    required_permissions = ['core.generate_event']

    def post(self, request):
        data = request.data
        try:
            # Vérifier si les champs nécessaires sont présents dans les données
            proposal = generate_event_proposal(
                country_code=data['country_code'],
                concert_hall_id=data['concert_hall_id'],
                genre_family_name=data['genre_family_name'],
                event_start=data['event_start'],
                taille_casting=int(data.get('taille_casting', 10)),
                quality_score=int(data.get('quality_score', 3)),
                custom_title=data.get('custom_title', None)
            )
            return Response(proposal, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ValidateEventView(APIView):
    permission_classes = [HasPermissions]
    allowed_roles = ['admin', 'organizer']
    required_permissions = ['core.validate_event']

    def post(self, request):
        data = request.data
        try:
            concert_hall = ConcertHall.objects.get(id=data['concert_hall_id'])
            artist_ids = [int(a) for a in request.data.get('artist_ids', [])]
            artists = list(Artist.objects.filter(id__in=artist_ids))

            if len(artists) != len(artist_ids):
                return Response({"error": "Some artists were not found"}, status=404)

            event_start = make_aware(parse_datetime(data['event_start']))
            event_end = make_aware(parse_datetime(data['event_end']))

            event_proposal = Event.objects.create(
                title=data['title'],
                concert_hall=concert_hall,
                event_start=event_start,
                event_end=event_end,
                organizer=request.user,
            )

            event_proposal.artists.set(artists)

            event_proposal.save()

            return Response({"message": "Event proposal validated successfully"}, status=status.HTTP_200_OK)
        except ConcertHall.DoesNotExist:
            return Response({"error": "Concert hall not found"}, status=status.HTTP_404_NOT_FOUND)
        except Artist.DoesNotExist:
            return Response({"error": "Some artists were not found"}, status=status.HTTP_404_NOT_FOUND)
        except KeyError as e :
            return Response({"error": f"Missing required field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
