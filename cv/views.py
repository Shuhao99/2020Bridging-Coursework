from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from .forms import AboutForm, EducationForm, ExperienceForm,SkillsForm,AwardForm
from django.urls import reverse
from django.utils import timezone
from .models import about, experience, education, skills, award
from django.contrib.auth.models import User
from django.http import Http404 

# Create your views here.
def cv(request):
    Edit = request.user.is_staff
    about_ = about.objects.all()
    skills_ = skills.objects.all()
    experience_ = experience.objects.all()
    education_ = education.objects.all()
    award_ = award.objects.all()
    return render(request, 'cv/cv.html', {'about': about_, 'skills': skills_, 'experience': experience_, 'education': education_, 'award': award_, 'edit':Edit})

def cv_edit(request):
    if (not request.session.get('is_login', None)) or (not (request.user.is_staff)):
        return redirect('login')
    return render(request, 'cv/cv_edit.html')

def new_about(request):
    about_ = get_object_or_404(about, id=1)
    if not request.session.get('is_login', None):
        return redirect('login')
    elif not (request.user.is_staff):
        return redirect('login')
    if request.method == "POST":
        form_about = AboutForm(request.POST, instance=about_)
        if form_about.is_valid():
            form_about.save()
            return redirect('cv')
    else:
        form_about = AboutForm(request.POST, instance=about_)
        
    return render(request, 'cv/cv_new.html', {'form': form_about})

def new_skills(request):
    if not request.session.get('is_login', None):
        return redirect('login')
    elif not (request.user.is_staff):
        raise redirect('login')
    if request.method == "POST":
        form_skills = SkillsForm(request.POST)
        if form_skills.is_valid():
            form_skills.save()
            return redirect('cv')
    else:
        form_skills = SkillsForm()
        
    return render(request, 'cv/cv_new.html', {'form': form_skills})

def new_experience(request):
    if not request.session.get('is_login', None):
        return redirect('login')
    elif not (request.user.is_staff):
        raise redirect('login')
    if request.method == "POST":
        form_experience = ExperienceForm(request.POST)
        if form_experience.is_valid():
            form_experience.save()
            return redirect('cv')
    else:
        form_experience = ExperienceForm()
        
    return render(request, 'cv/cv_new.html', {'form': form_experience})

def new_education(request):
    education_ = education.objects.all()
    if not request.session.get('is_login', None):
        return redirect('login')
    elif not (request.user.is_staff):
        raise redirect('login')
    if request.method == "POST":
        form_eduction = EducationForm(request.POST)
        if form_eduction.is_valid():
            form_eduction.save()
            return redirect('cv')
    else:
        form_eduction = EducationForm()
        
    return render(request, 'cv/cv_new.html', {'form':form_eduction})


def new_award(request):
    award_ = award.objects.all()
    if not request.session.get('is_login', None):
        return redirect('login')
    elif not (request.user.is_staff):
        raise redirect('login')
    if request.method == "POST":
        form_award = AwardForm(request.POST)
        if form_award.is_valid():
            form_award.save()
            return redirect('cv')
    else:
        form_award = AwardForm()
        
    return render(request, 'cv/cv_new.html', {'form':form_award })