from core.models import ConcertHall, GenreFamily, Artist, CountryDemographics
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta

def calculer_duree_evenement(artistes_sorted, taille_casting):
    def interp(popularity, min_time, max_time):
        return min_time + (max_time - min_time) * (popularity / 100)

    total_minutes = 0
    if taille_casting == 1:
        total_minutes = interp(artistes_sorted[0]["popularity"], 60, 90)
    elif 2 <= taille_casting <= 4:
        total_minutes = sum(interp(a["popularity"], 30, 60) for a in artistes_sorted)
    else:
        total_minutes = sum(interp(a["popularity"], 15, 30) for a in artistes_sorted)

    return timedelta(minutes=int(total_minutes))


def generate_event_proposal(country_code, concert_hall_id, genre_family_name, event_start, taille_casting=10, quality_score=3, custom_title=None):
    try:
        concert_hall = ConcertHall.objects.get(id=concert_hall_id)
        genre_family = GenreFamily.objects.get(name__iexact=genre_family_name)
        demo = CountryDemographics.objects.get(country__code=country_code)
    except (ConcertHall.DoesNotExist, GenreFamily.DoesNotExist, CountryDemographics.DoesNotExist) as e:
        raise ValueError(str(e))

    artistes_genre = Artist.objects.filter(genre_family=genre_family)
    if not artistes_genre.exists():
        raise ValueError("No artists found for this genre.")

    artistes = []
    for artist in artistes_genre:
        popularity = artist.spotify_popularity
        popularity = popularity if popularity is not None else 0
        artistes.append({
            "id": artist.id,
            "artistName": artist.name,
            "streams_pays": getattr(artist, f'stats_{country_code}', 0),
            "longevite_moyenne": artist.longevity,
            "popularity": popularity,
            "score": popularity,  # Identique
            "famille_musicale": genre_family.name
        })

    score_ranges = {
        1: (0, 40),
        2: (40, 55),
        3: (55, 70),
        4: (70, 85),
        5: (85, 100),
    }

    min_score, max_score = score_ranges.get(quality_score, (0, float('inf')))
    if quality_score == 1:
        artistes_filtres = [a for a in artistes if not a["score"] or a["score"] < 40]
    else:
        artistes_filtres = [a for a in artistes if min_score <= a["score"] <= max_score]

    filtrage_applique = True
    if len(artistes_filtres) < taille_casting:
        artistes_filtres = artistes
        filtrage_applique = False

    artistes_sorted = sorted(artistes_filtres, key=lambda x: x["score"], reverse=True)[:taille_casting]

    popularite_totale = sum(a["popularity"] for a in artistes_sorted)
    popularite_moyenne = popularite_totale / taille_casting
    facteur_popularite = popularite_moyenne / 100

    base_prix_billet = 40  # Valeur par défaut
    if quality_score == 1:
        base_prix_billet = 20
    elif quality_score == 2:
        base_prix_billet = 25
    elif quality_score == 3:
        base_prix_billet = 40
    elif quality_score == 4:
        base_prix_billet = 45
    elif quality_score == 5:
        base_prix_billet = 60

    prix_billet = base_prix_billet + (base_prix_billet * facteur_popularite)
    participants_estimes = int(popularite_totale * 100)
    revenus_estimes = participants_estimes * prix_billet

    duration = calculer_duree_evenement(artistes_sorted, taille_casting)
    event_end = datetime.fromisoformat(event_start) + duration

    return {
        "casting": artistes_sorted,
        "revenus": {
            "prix_billet": prix_billet,
            "participants_estimes": participants_estimes,
            "revenus_estimes": revenus_estimes
        },
        "event_preview": {
            "title": custom_title if custom_title else f"{genre_family.name} Night",
            "event_start": event_start,
            "event_end": event_end.isoformat(),
            "concert_hall": concert_hall.id,
            "country": country_code
        },
        "filtrage": {
            "quality_score": quality_score,
            "filtrage_applique": filtrage_applique,
            "popularite_moyenne_casting": popularite_moyenne
        }
    }
