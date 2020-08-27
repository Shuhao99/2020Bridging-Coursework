from django.urls import resolve, reverse
from django.test import TestCase
from django.apps import apps
from django.contrib.auth.models import User
from .models import about, experience, education, award, skills
from .views import cv 

class CVPageTest(TestCase):
    def setUp(self):
        # Create a super user
        self.user = User.objects.create_superuser(
            username='admin_test', 
            email='admin@hellogithub.com', 
            password='admin')

        # Create a test object for each model
        self.about = about.objects.create(
            name = 'Test about'
        )

        self.experience = experience.objects.create(
            experience_title = 'Test experience title',
            experience_text = 'Test experience text',
            experience_name = 'Test experience name',
            experience_date_start = 'Test experience start date',
            experience_date_end = 'Test experience end date'
        )

        self.education = education.objects.create(
            facility = 'Test facility',
            title = 'Test title',
            Grade = 'Test grade',
            date_start = 'Test start',
            date_end = 'Test end'
        )

        self.skills = skills.objects.create(
            name = 'Test skill name'
        )
        
        self.award = skills.objects.create(
            name = 'Test skill name'
        )
        
        # Prepare URL for unittest
        self.url = '/cv/'
        self.url_add_new = '/cv/new/'
        self.url_new_experience = '/cv/new/experience/'
        self.url_delete_experience = '/cv/remove/experience/'
        self.url_edit_experience = '/cv/edit/experience/'

    # Model test
    def test_model_test_about(self):
        self.assertEqual(self.about.__str__(), self.about.name)

    
    def test_model_test_experience(self):
        self.assertEqual(self.experience.__str__(), self.experience.experience_title)
    
    def test_model_test_education(self):
        self.assertEqual(self.education.__str__(), self.education.facility)
    
    def test_model_test_skills(self):
        self.assertEqual(self.skills.__str__(), self.skills.name)
    
    def test_model_test_award(self):
        self.assertEqual(self.award.__str__(), self.award.name)
    
    
    # View test
    def test_root_url_resolves_to_cv_page_view(self):
        found = resolve('/cv/')  
        self.assertEqual(found.func, cv)
    
    
    def test_cv_page_returns_correct_html(self):
       response = self.client.get(self.url)
       self.assertTemplateUsed(response, 'cv/cv.html')
       # Make sure CV edit option is hidden from guests
       self.assertNotContains(response, 'CV edit')

    
    def test_guest_edit_cv(self):
        response = self.client.post(self.url_add_new)
        # User should be redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/login/')
    
    
    def test_staff_edit_cv(self):
        # Staff login
        response = self.client.post('/login/', {'username': self.user.username, 'password': 'admin'})
        # Now cv edit option should show up
        response = self.client.get(self.url_add_new)
        self.assertTemplateUsed(response, 'cv/cv_edit.html')


    def test_staff_an_experience_POST(self):
        # Staff login
        response = self.client.post('/login/', {'username': self.user.username, 'password': 'admin'})
        # Make new post
        response = self.client.post(self.url_new_experience,data={
            'part':'experience',
            'experience_title':'University of Nottingham',
            'experience_name':'Summer Research',
            'experience_text':'Apply NLP tech in order classify',
            'experience_date_start': 'June 2019',
            'experience_date_end':'August 2019'
        })
        # Experience has two objects because one object has been created in Setup
        self.assertEqual(experience.objects.count(),2)
        new_experience = experience.objects.all()[1]
        self.assertEqual(new_experience.experience_title,'University of Nottingham')
        self.assertEqual(new_experience.experience_name,'Summer Research')

             
    def test_redirect_after_post(self):
        # Staff login
        response = self.client.post('/login/', {'username': self.user.username, 'password': 'admin'})
        # Make new post
        response = self.client.post(self.url_new_experience, data={
            'part':'experience',
            'experience_title':'University of Nottingham',
            'experience_name':'Summer Research',
            'experience_text':'Apply NLP tech in order classify',
            'experience_date_start': 'June 2019',
            'experience_date_end':'August 2019'
        })
        # Check if the new content be added
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'],'/cv/')
    
    
    def test_desplay_all_experience_items(self):
        # we have already create an experience at the beginning
        response = self.client.get('/cv/')
        self.assertIn('Test experience title', response.content.decode())
        self.assertIn('Test experience text', response.content.decode())
        self.assertIn('Test experience name', response.content.decode())
        self.assertIn('Test experience end date', response.content.decode())
        self.assertIn('Test experience start date', response.content.decode())
    
    
    def test_delete_experience(self):
        # Staff login
        response = self.client.post('/login/', {'username': self.user.username, 'password': 'admin'})
        # Delete designated post
        self.assertEqual(experience.objects.count(), 1)
        self.url_delete_experience = self.url_delete_experience + str(self.experience.id) + '/'
        response = self.client.post(self.url_delete_experience, {'part':'experience'}) 
        # Check if the post has been deleted
        self.assertEqual(experience.objects.count(), 0)
    
    
    def test_delete_experience_not_login(self):
        # Try to delete
        self.url_delete_experience = self.url_delete_experience + str(self.experience.id) + '/'
        response = self.client.post(self.url_delete_experience, {'part':'experience'})
        # Check if guest be redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'],'/login/')
        # Check if the object number does not decrease
        self.assertEqual(experience.objects.count(), 1)
    
    def test_edit_experience(self):
        # Staff login
        response = self.client.post('/login/', {'username': self.user.username, 'password': 'admin'})
        # Edit experience
        self.url_edit_experience = self.url_edit_experience + str(self.experience.id) + '/'
        response = self.client.post(self.url_edit_experience, data={
            'part':'experience',
            'experience_title':'EDIT_title',
            'experience_name':'EDIT_name',
            'experience_text':'EDIT_text',
            'experience_date_start': 'EDIT_start',
            'experience_date_end':'EDIT_end'
        })
        # Check if edit
        response = self.client.get('/cv/')
        self.assertIn('EDIT_title', response.content.decode())
        self.assertIn('EDIT_name', response.content.decode())

    def test_guest_edit_experience(self):
        # Edit experience
        self.url_edit_experience = self.url_edit_experience + str(self.experience.id) + '/'
        response = self.client.post(self.url_edit_experience, data={
            'part':'experience',
            'experience_title':'EDIT_title',
            'experience_name':'EDIT_name',
            'experience_text':'EDIT_text',
            'experience_date_start': 'EDIT_start',
            'experience_date_end':'EDIT_end'
        })
        # Guest should be redirect
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'],'/login/')



        


        

    
    

    