from django.contrib import admin
from .models import Post,Tag,Category,about, education, experience, skills, award 


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(about)
admin.site.register(education)
admin.site.register(experience)
admin.site.register(skills)
admin.site.register(award)
