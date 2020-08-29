from django.urls import path
from . import views

urlpatterns = [    
    path('', views.cv, name = 'cv'),
    #new CV content
    path('new/', views.cv_new, name='cv_new'),
    path('new/experience/', views.new, {'part':'experience'}, name='new_experience'),
    path('new/experience/', views.new, {'part':'experience'}, name='new_experience'),
    path('new/skills/', views.new, {'part':'skills'}, name='new_skills'),
    path('new/education/', views.new, {'part':'education'}, name='new_education'),
    path('new/award/', views.new, {'part':'award'}, name='new_award'),
    #edit
    path('edit/about/<int:id>/', views.edit, {'part':'about'}, name='edit_about'),
    path('edit/experience/<int:id>/', views.edit, {'part':'experience'},name='edit_experience'),
    path('edit/skills/<int:id>/', views.edit, {'part':'skills'},name='edit_skills'),
    path('edit/education/<int:id>/', views.edit, {'part':'education'},name='edit_education'),
    path('edit/award/<int:id>/', views.edit, {'part':'award'},name='edit_award'),
    #delete
    path('remove/experience/<int:id>/', views.remove, {'part':'experience'},name='remove_experience'),
    path('remove/skills/<int:id>/', views.remove, {'part':'skills'},name='remove_skills'),
    path('remove/education/<int:id>/', views.remove, {'part':'education'},name='remove_education'),
    path('remove/award/<int:id>/', views.remove, {'part':'award'},name='remove_award'),
]

