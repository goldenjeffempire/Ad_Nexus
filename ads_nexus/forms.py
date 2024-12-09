from django import forms
from .models import AdCampaign, AdTargeting

class AdCampaignForm(forms.ModelForm):
    class Meta:
        model = AdCampaign
        fields = ['name', 'budget', 'start_date', 'end_date']


class AdTargetingForm(forms.ModelForm):
    class Meta:
        model = AdTargeting
        fields = ['age_range', 'location', 'interests']
