# core/management/commands/import_demographics.py
import csv
import pycountry
from django.core.management.base import BaseCommand
from core.models.countries import Country
from core.models.demographics import CountryDemographics

class Command(BaseCommand):
    help = "Importe les statistiques démographiques à partir d'un fichier CSV"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Chemin complet vers Demographic_stats_per_country.csv')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        count = 0

        try:
            with open(csv_file, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    code = row['CountryCode'].strip().upper()

                    # Récupérer le nom du pays via pycountry
                    try:
                        country_data = pycountry.countries.get(alpha_2=code)
                        country_name = country_data.name if country_data else code
                    except Exception as e:
                        country_name = code  # en cas d'erreur, utiliser le code lui-même

                    # Créer (ou récupérer) l'objet Country
                    country, created = Country.objects.get_or_create(
                        code=code,
                        defaults={'name': country_name}
                    )

                    # Si le nom de pays est vide ou égal au code, mettre à jour
                    if not country.name or country.name == code:
                        country.name = country_name
                        country.save()

                    # Préparer les données démographiques
                    demographics_data = {
                        'average_online_ticket_purchase_rate': float(row['AverageOnlineTicketPurchaseRate'] or 0),
                        'average_concert_participation_rate': float(row['AverageConcertParticipationRate'] or 0),
                        'quintile_average_cultural_spending_per_capita': float(row['QuintileAverageCulturalSpendingPerCapita'] or 0),
                        'annual_average_cultural_spending_per_capita': float(row['AnnualAverageCulturalSpendingPerCapita'] or 0),
                        'mean_estimated_cultural_expenses_until_2030': float(row['MeanEstimatedCulturalExpensesUntil2030'] or 0),
                        'spotify_streams_total_per_country': float(row['SpotifyStreamsTotalPerCountry'] or 0),
                        'number_of_tracks_per_country': float(row['NumberOfTracksPerCountry'] or 0),
                        'top_chart_presence_per_country': float(row['TopChartPresencePerCountry'] or 0),
                        'average_concert_audience_per_country': float(row['AverageConcertAudiencePerCountry'] or 0),
                        'average_cultural_spending_per_capita': float(row['AverageCulturalSpendingPerCapita'] or 0),
                        'country_cluster': row['CountryCluster'] or None,
                    }

                    # Créer ou mettre à jour l'objet CountryDemographics associé au Country
                    CountryDemographics.objects.update_or_create(
                        country=country,
                        defaults=demographics_data
                    )
                    count += 1

            self.stdout.write(self.style.SUCCESS(f"Import terminé, {count} enregistrements traités."))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("Fichier CSV non trouvé."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erreur lors de l'import : {e}"))
