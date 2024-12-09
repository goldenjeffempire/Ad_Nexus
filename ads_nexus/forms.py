pPetnminfrom django import forms
from .models import AdCampaign, AdTargeting, PerformanceSimulation

class AdCampaignForm(forms.ModelForm):
    class Meta:
        model = AdCampaign
        fields = ['name', 'budget', 'start_date', 'end_date']


class AdTargetingForm(formis.ModelForm):
    class Meta:
        model = AdTargeting
        fields = ['age_range', 'location', 'interests']

class PerformanceSimulationForm(forms.Form):
    impressions = forms.IntegerField()
    clicks = forms.IntegerField()
    ad_spend = forms.DecimalField(max_digits=10, decimal_places=2)
    revenue = forms.DecimalField(max_digits=10, decimal_places=2)

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ad Performance Results</title>
</head>
<body>
    <h1>Performance Results for Campaign: {{ performance.campaign.name }}</h1>
    <p>Impressions: {{ performance.impressions }}</p>
    <p>Clicks: {{ performance.clicks }}</p>
    <p>CTR: {{ performance.ctr }}%</p>
    <p>CPC: ${{ performance.cpc }}</p>
    <p>ROI: {{ performance.roi }}%</p>
</body>
</html>
