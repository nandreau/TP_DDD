# core/management/commands/import_csv.py
import csv
from datetime import datetime
from math import isnan
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models.concerthall import ConcertHall
from core.models.event import Event
from tqdm import tqdm


def clean_str(val):
    if val is None:
        return ''
    if isinstance(val, float) and isnan(val):
        return ''
    return str(val).strip()


def parse_datetime_flexible(date_str):
    date_str = clean_str(date_str)
    if not date_str:
        return None
    try:
        return timezone.make_aware(datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S"))
    except ValueError:
        try:
            return timezone.make_aware(datetime.strptime(date_str, "%Y-%m-%d"))
        except ValueError as e:
            raise e


class Command(BaseCommand):
    help = "Import des données depuis ConcertHall.csv et EventsData.csv"

    def add_arguments(self, parser):
        parser.add_argument('--concert_hall', type=str, required=True)
        parser.add_argument('--event', type=str, required=True)

    def handle(self, *args, **kwargs):
        concert_hall_csv = kwargs['concert_hall']
        event_csv = kwargs['event']

        failures = {
            'concert_halls': [],
            'event_start_parsing': [],
            'event_end_parsing': [],
            'events': [],
            'concert_hall_linking': []
        }

        # === Import ConcertHalls ===
        with open(concert_hall_csv, 'r', encoding='utf-8') as f:
            reader = list(csv.DictReader(f))
            reader = [{k.strip(): v for k, v in row.items()} for row in reader]
            for row in tqdm(reader, desc="Import Concert Halls"):
                try:
                    ConcertHall.objects.update_or_create(
                        concert_hall_id=clean_str(row.get('ConcertHallId')),
                        defaults={
                            'name': clean_str(row.get('ConcertHallName')),
                            'capacity': int(row['Capacity']) if row.get('Capacity') else None,
                            'city': clean_str(row.get('City')),
                            'state': clean_str(row.get('State')),
                            'country': clean_str(row.get('Country')),
                            'country_code': clean_str(row.get('CountryCode')),
                            'postal_code': clean_str(row.get('PostalCode')),
                            'address': clean_str(row.get('Address')),
                            'latitude': float(row['Latitude']) if row.get('Latitude') else None,
                            'longitude': float(row['Longitude']) if row.get('Longitude') else None,
                            'image_url': clean_str(row.get('ImageUrl')),
                        }
                    )
                except Exception as e:
                    failures['concert_halls'].append((clean_str(row.get('ConcertHallId')), str(e)))

        # === Import Events ===
        with open(event_csv, 'r', encoding='utf-8') as f:
            reader = list(csv.DictReader(f))
            reader = [{k.strip(): v for k, v in row.items()} for row in reader]
            for row in tqdm(reader, desc="Import Events"):
                event_start_str = f"{clean_str(row.get('EventDateStart'))} {clean_str(row.get('EventTimeStart'))}"
                event_end_str = f"{clean_str(row.get('EventDateEnd'))} {clean_str(row.get('EventTimeEnd'))}"

                event_start = None
                event_end = None
                try:
                    if event_start_str.strip():
                        event_start = parse_datetime_flexible(event_start_str)
                except Exception as e:
                    failures['event_start_parsing'].append((clean_str(row.get('EventName')), str(e)))

                try:
                    if event_end_str.strip():
                        event_end = parse_datetime_flexible(event_end_str)
                except Exception as e:
                    failures['event_end_parsing'].append((clean_str(row.get('EventName')), str(e)))

                try:
                    hall_id = clean_str(row.get('ConcertHallId'))
                    concert_hall = ConcertHall.objects.filter(concert_hall_id=hall_id).first()
                    if not concert_hall:
                        failures['concert_hall_linking'].append((clean_str(row.get('EventName')), f"ConcertHallId '{hall_id}' introuvable"))
                        continue

                    Event.objects.update_or_create(
                        event_id=clean_str(row.get('EventId')),
                        defaults={
                            'title': clean_str(row.get('EventName')),
                            'event_start': event_start,
                            'event_end': event_end,
                            'image_url': clean_str(row.get('ImagesUrl')),
                            'concert_hall': concert_hall,
                        }
                    )
                except Exception as e:
                    failures['events'].append((clean_str(row.get('EventName')), str(e)))

        # Résumé
        if any(failures.values()):
            print("\n⚠️  Import terminé avec des erreurs.\n")
            for key, values in failures.items():
                if values:
                    print(f"- {key.replace('_', ' ').capitalize()} : {len(values)}")
                    for name, err in values[:5]:
                        print(f"  [{name}] → {err}")
            print("\n💡 PS : seules les 5 premières erreurs de chaque type sont affichées.")
        else:
            print("\n✅ Import terminé avec succès, sans aucune erreur.")
