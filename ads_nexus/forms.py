from django import forms
from .models import AdCampaign, AdTargeting

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

class AdContentForm(forms.Form):
    campaign_description = forms.CharField(widget=forms.Textarea, label="Campaign Description", required=True)
