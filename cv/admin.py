from django.contrib import admin
from .models import about, education, experience, skills, award 

admin.site.register(about)
admin.site.register(education)
admin.site.register(experience)
admin.site.register(skills)
admin.site.register(award)
