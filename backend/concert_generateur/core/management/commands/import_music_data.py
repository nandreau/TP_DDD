# your_app/management/commands/import_music_data.py

import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from core.models import Genre, GenreFamily
from core.models.artists import Artist
from core.models.tracks import Track
from collections import defaultdict
from tqdm import tqdm
from datetime import datetime

DATA_PATH = os.path.join(settings.BASE_DIR, 'data')

class Command(BaseCommand):
    help = 'Import genres, genre families, artists and tracks from CSVs'

    def handle(self, *args, **kwargs):
        self.import_genre_families()
        self.import_genres()
        self.import_artists()
        self.import_tracks()
        self.stdout.write(self.style.SUCCESS('✅ Import terminé avec succès !'))

    def import_genre_families(self):
        filepath = os.path.join(DATA_PATH, 'df_genre_age_backend.csv')
        with open(filepath, encoding='utf-8') as f:
            reader = list(csv.DictReader(f))
            for row in tqdm(reader, desc="🎼 Importing genre families"):
                family_name = row['Famille musicale']
                age_group_streams = {
                    k: {"streams": float(v)}
                    for k, v in row.items()
                    if k and k != 'Famille musicale' and v.strip() != ''
                }
                GenreFamily.objects.update_or_create(
                    name=family_name,
                    defaults={'age_group_streams': age_group_streams}
                )

    def import_genres(self):
        filepath = os.path.join(DATA_PATH, 'artistes_genres_backend.csv')
        with open(filepath, encoding='utf-8') as f:
            reader = list(csv.DictReader(f))
            for row in tqdm(reader, desc="🎸 Importing genres"):
                family_name = row['famille_musicale']
                genres_list = eval(row['genres']) if row['genres'].startswith('[') else [row['genres']]

                family = GenreFamily.objects.filter(name=family_name).first()

                for genre_name in genres_list:
                    Genre.objects.update_or_create(
                        name=genre_name.strip(),
                        defaults={'family': family}
                    )

    def import_artists(self):
        artists_path = os.path.join(DATA_PATH, 'artistes_genres_backend.csv')
        country_stats_path = os.path.join(DATA_PATH, 'top_artiste_par_pays_backend.csv')

        # Charger les stats de streams par pays
        country_stats = defaultdict(lambda: defaultdict(float))  # artist_name -> pays -> streams
        with open(country_stats_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                artist = row['artist']
                pays = row['pays']
                streams = float(row['streams']) if row['streams'] else 0.0
                country_stats[artist][pays] += streams

        with open(artists_path, encoding='utf-8') as f:
            reader = list(csv.DictReader(f))
            for row in tqdm(reader, desc="🎤 Importing artists"):
                name = row['artistName']
                family_name = row['famille_musicale']
                genres_list = eval(row['genres']) if row['genres'].startswith('[') else [row['genres']]
                popularity = None
                if 'popularity' in row and row['popularity'] and row['popularity'].strip():
                    try:
                        popularity = int(float(row['popularity']))
                    except (ValueError, TypeError):
                        popularity = None

                followers = None
                if 'follower' in row and row['follower'] and row['follower'].strip():
                    try:
                        followers = int(float(row['follower']))
                    except (ValueError, TypeError):
                        followers = None

                family = GenreFamily.objects.filter(name=family_name).first()
                genre_name = genres_list[0].strip() if genres_list else None
                genre = Genre.objects.filter(name=genre_name).first() if genre_name else None

                Artist.objects.update_or_create(
                    name=name,
                    defaults={
                        'genre_family': family,
                        'genre': genre,
                        'spotify_popularity': popularity,
                        'followers': followers,
                        'spotify_streams_total': sum(country_stats[name].values()),
                        'stats_FR': int(country_stats[name].get('FR', 0)),
                        'stats_GB': int(country_stats[name].get('GB', 0)),
                        'stats_DE': int(country_stats[name].get('DE', 0)),
                        'stats_IT': int(country_stats[name].get('IT', 0)),
                        'stats_ES': int(country_stats[name].get('ES', 0)),
                        'stats_BE': int(country_stats[name].get('BE', 0)),
                    }
                )
    def import_tracks(self):
        filepath = os.path.join(DATA_PATH, 'df_tracks_v2.csv')
        with open(filepath, encoding='utf-8') as f:
            reader = list(csv.DictReader(f))
            for row in tqdm(reader, desc="🎶 Importing tracks"):
                artist_name = row['main_artist'].strip()

                artist, created = Artist.objects.get_or_create(name=artist_name)

                if created:
                    self.stdout.write(self.style.WARNING(f"➕ Artist created: {artist_name}"))

                def parse_date(date_str):
                    try:
                        return datetime.strptime(date_str, '%Y-%m-%d').date()
                    except:
                        return None

                Track.objects.update_or_create(
                    title=row['track'],
                    artist=artist,
                    defaults={
                        'artist_2': row.get('artist_2', None),
                        'artist_3': row.get('artist_3', None),
                        'artist_others': row.get('artist_others', None),
                        'release_date': parse_date(row['release_date']),
                        'entry_date': parse_date(row['entry_date']),
                        'entry_rank': int(row['entry_rank']) if row['entry_rank'].isdigit() else None,
                        'current_rank': int(row['current_rank']) if row['current_rank'].isdigit() else None,
                        'peak_rank': int(row['peak_rank']) if row['peak_rank'].isdigit() else None,
                        'peak_date': parse_date(row['peak_date']),
                        'appearances': int(row['appearances']) if row['appearances'].isdigit() else None,
                        'consecutive_appearances': int(row['consecutive_appearances']) if row['consecutive_appearances'].isdigit() else None,
                        'streams': int(row['streams']) if row['streams'].isdigit() else None,
                        'source_date': parse_date(row['source_date']),
                    }
                )
