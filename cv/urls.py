from django.urls import path
from . import views

urlpatterns = [    
    path('', views.cv, name = 'cv'),
    #new CV content
    path('edit/', views.cv_edit, name='cv_edit'),
    path('edit/about', views.new_about, name='new_about'),
    path('edit/experience', views.new_experience, name='new_experience'),
    path('edit/skills', views.new_skills, name='new_skills'),
    path('edit/education', views.new_education, name='new_education'),
    path('edit/award', views.new_award, name='new_award'),
]

