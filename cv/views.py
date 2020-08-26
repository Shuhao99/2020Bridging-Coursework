from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from .forms import AboutForm, EducationForm, ExperienceForm, SkillsForm, AwardForm
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
    return render(request, 'cv/cv.html', {'about': about_, 'skills': skills_, 'experience': experience_, 'education': education_, 'award': award_, 'edit': Edit})

def cv_new(request):
    if (not request.session.get('is_login', None)) or (not (request.user.is_staff)):
        return redirect('login')
    elif not (request.user.is_staff):
        return redirect('login')
    return render(request, 'cv/cv_edit.html')

def new(request, part):
    if not request.session.get('is_login', None):
        return redirect('login')
    elif not (request.user.is_staff):
        return redirect('login')
    if request.method == "POST":
        if (part == 'education'):
            form = EducationForm(request.POST)
        elif (part == 'experience'):
            form = ExperienceForm(request.POST)
        elif (part == 'skills'):
            form = SkillsForm(request.POST)
        elif (part == 'award'):
            form = AwardForm(request.POST)
        else:
            raise Http404

        if form.is_valid():
            form.save()
            return redirect('cv')
    else:
        if (part == 'education'):
            form = EducationForm()
        elif (part == 'experience'):
            form = ExperienceForm()
        elif (part == 'skills'):
            form = SkillsForm()
        elif (part == 'award'):
            form = AwardForm()
        else:
            raise Http404
    return render(request, 'cv/cv_new.html', {'form': form})

def edit(request, id, part):
    if not request.session.get('is_login', None):
        return redirect('login')
    elif not (request.user.is_staff):
        return redirect('login')
    if request.method == "POST":
        if(part == 'about'):
            Part = get_object_or_404(about, id=id)
            form = AboutForm(request.POST, instance=Part)
        elif (part == 'education'):
            Part = get_object_or_404(education, id=id)
            form = EducationForm(request.POST, instance=Part)
        elif (part == 'experience'):
            Part = get_object_or_404(experience, id=id)
            form = ExperienceForm(request.POST, instance=Part)
        elif (part == 'skills'):
            Part = get_object_or_404(skills, id=id)
            form = SkillsForm(request.POST, instance=Part)
        elif (part == 'award'):
            Part = get_object_or_404(award, id=id)
            form = AwardForm(request.POST, instance=Part)
        else:
            raise Http404
        if form.is_valid():
            Part = form.save(commit=False)
            Part.save()
            return redirect('cv')
    else:
        if(part == 'about'):
            Part = get_object_or_404(about, id=id)
            form = AboutForm(instance=Part)
        elif (part == 'education'):
            Part = get_object_or_404(education, id=id)
            form = EducationForm(instance=Part)
        elif (part == 'experience'):
            Part = get_object_or_404(experience, id=id)
            form = ExperienceForm(instance=Part)
        elif (part == 'skills'):
            Part = get_object_or_404(skills, id=id)
            form = SkillsForm(instance=Part)
        elif (part == 'award'):
            Part = get_object_or_404(award, id=id)
            form = AwardForm(instance=Part)
        else:
            raise Http404

    return render(request, 'cv/cv_new.html', {'form': form})

def remove(request, id, part):
    if not request.session.get('is_login', None):
        return redirect('login')
    elif not (request.user.is_staff):
        return redirect('login')
    if (part == 'education'):
        Part = get_object_or_404(education, id=id)
    elif (part=='experience'):
        Part = get_object_or_404(experience, id=id)
    elif (part=='skills'):
        Part = get_object_or_404(skills, id=id)
    elif (part == 'award'):
        Part = get_object_or_404(award, id=id)
    else:
        raise Http404
    Part.delete()
    return redirect('cv')
