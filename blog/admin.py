from django.contrib import admin
from .models import Post,Tag,Category,about 


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(about)

