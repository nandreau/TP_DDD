from django.db import models
from core.models.countries import Country

class CountryDemographics(models.Model):
    country = models.OneToOneField(Country, primary_key=True, on_delete=models.CASCADE, related_name='demographics')
    average_online_ticket_purchase_rate = models.FloatField(null=True, blank=True)
    average_concert_participation_rate = models.FloatField(null=True, blank=True)
    quintile_average_cultural_spending_per_capita = models.FloatField(null=True, blank=True)
    annual_average_cultural_spending_per_capita = models.FloatField(null=True, blank=True)
    mean_estimated_cultural_expenses_until_2030 = models.FloatField(null=True, blank=True)
    spotify_streams_total_per_country = models.BigIntegerField(null=True, blank=True)
    number_of_tracks_per_country = models.IntegerField(null=True, blank=True)
    top_chart_presence_per_country = models.IntegerField(null=True, blank=True)
    average_concert_audience_per_country = models.FloatField(null=True, blank=True)
    average_cultural_spending_per_capita = models.FloatField(null=True, blank=True)
    country_cluster = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Demographics for {self.country.code}"
