from django import forms
from .models import education, experience, about, award, skills

class AboutForm(forms.ModelForm):
    class Meta:
        model = about
        fields = '__all__'

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = experience
        fields = '__all__'

class EducationForm(forms.ModelForm):
    class Meta:
        model = education
        fields = '__all__'

class SkillsForm(forms.ModelForm):
    class Meta:
        model = skills
        fields = '__all__'

class AwardForm(forms.ModelForm):
    class Meta:
        model = award
        fields = '__all__'
