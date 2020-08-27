from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):  

    def setUp(self):  
        self.browser = webdriver.Firefox()
        self.url = 'http://localhost:8000/cv/'
        self.url_edit = 'http://localhost:8000/cv/new/'
        self.url_new_experience = 'http://localhost:8000/cv/new/experience/'
        self.url_new_skills = 'http://localhost:8000/cv/new/skills/'
        self.url_new_education = 'http://localhost:8000/cv/new/education/'
        self.url_new_award = 'http://localhost:8000/cv/new/award/'

        # Create a super user
        self.user = User.objects.create_superuser(
            username='admin_test', 
            email='admin@hellogithub.com', 
            password='admin')
        

    def tearDown(self):  
        self.browser.quit()

    def test_1_the_cv_page_view_not_login(self):  
        self.browser.get(self.url)
        
        # Test website title
        self.assertIn('My CV', self.browser.title)
        
        # Test the layout
        menu = self.browser.find_element_by_id('menu')
        rows = menu.find_elements_by_tag_name('a')  
    
        self.assertIn('Home Page',[row.get_attribute('textContent') for row in rows]) 
        self.assertIn('About',[row.get_attribute('textContent') for row in rows]) 
        self.assertIn('Experience',[row.get_attribute('textContent') for row in rows]) 
        self.assertIn('Education',[row.get_attribute('textContent') for row in rows]) 
        self.assertIn('Skills',[row.get_attribute('textContent') for row in rows]) 
        self.assertIn('Awards',[row.get_attribute('textContent') for row in rows]) 
            
        # Make sure only staff can see the CV edit option
        self.assertFalse(
            any(row.text == 'CV edit' for row in rows)
        )
        
        # Test the title layout
        titles = self.browser.find_elements_by_tag_name('h2')
        
        self.assertIn('Experience',[title.get_attribute('textContent') for title in titles])
        self.assertIn('Skills',[title.get_attribute('textContent') for title in titles])
        self.assertIn('Education',[title.get_attribute('textContent') for title in titles])
        self.assertIn('Awards & Certifications',[title.get_attribute('textContent') for title in titles])
    
    def test_2_the_cv_page_view_login_as_superuser(self):  
        
        # Test edit cv without login
        self.browser.get(self.url_edit)
        
        # User should be redirect to login
        username = self.browser.find_element_by_name("username")
        password = self.browser.find_element_by_name("password")
        login = self.browser.find_element_by_tag_name('button')
        
        #login as staff
        username.send_keys('admin_test')
        password.send_keys('admin')
        login.click()
        time.sleep(1)

        # Now user should be able to edit cv
        self.browser.get(self.url)
        menu = self.browser.find_element_by_id('menu')
        rows = menu.find_elements_by_tag_name('li')  
        
        # User should observe CV edit option in menu
        self.assertIn('CV edit', [row.get_attribute('textContent') for row in rows])

        # User should not be redirect when edit cv
        self.browser.get(self.url_edit)
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_name("username")
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_name("password")
        
        # Test the layout of the edit page 
        title = self.browser.find_element_by_tag_name('h2')
        self.assertEqual('CHOOSE CONTENT TO ADD!', title.text)

        experience = self.browser.find_element_by_link_text('experience')
        education = self.browser.find_element_by_link_text('education')
        skills = self.browser.find_element_by_link_text('skills')
        awards = self.browser.find_element_by_link_text('award')
        
        
    def test_3_add_new_education(self):  
        
        # Test edit cv without login
        self.browser.get(self.url_edit)
        
        # User should be redirect to login
        username = self.browser.find_element_by_name("username")
        password = self.browser.find_element_by_name("password")
        login = self.browser.find_element_by_tag_name('button')
        
        # Login as staff
        username.send_keys('admin_test')
        password.send_keys('admin')
        login.click()
        time.sleep(1)

        # Navigate to add new content page
        self.browser.get(self.url_edit)

        # Choose add new education option
        add_button = self.browser.find_element_by_xpath('//*[contains(text(), "education")]')
        add_button.click()
        
        # Complete and submit the form
        form = self.browser.find_element_by_tag_name('form')
        facility = form.find_element_by_name("facility")
        title = form.find_element_by_name("title")
        Grade = form.find_element_by_name("Grade")
        start = form.find_element_by_name("date_start")
        end = form.find_element_by_name("date_end")
        submit = form.find_element_by_xpath('//*[contains(text(), "Publish")]')
        
        facility.send_keys(Keys.CONTROL,'a') 
        facility.send_keys(Keys.BACK_SPACE)
        facility.send_keys('Test name')
        title.send_keys(Keys.CONTROL,'a')
        title.send_keys(Keys.BACK_SPACE)
        title.send_keys('Test title')
        Grade.send_keys(Keys.CONTROL,'a')
        Grade.send_keys(Keys.BACK_SPACE)
        Grade.send_keys('Test')
        start.send_keys(Keys.CONTROL,'a')
        start.send_keys(Keys.BACK_SPACE)
        start.send_keys('Test start date')
        end.send_keys(Keys.CONTROL,'a')
        end.send_keys(Keys.BACK_SPACE)
        end.send_keys('Test end date')
        submit.click()
        
        # Test if the layout change
        self.browser.get(self.url)

        # The creator can see their education item
        self.browser.find_element_by_xpath('//*[contains(text(), "Test name")]')
        self.browser.find_element_by_xpath('//*[contains(text(), "Test title")]')
        self.browser.find_element_by_xpath('//*[contains(text(), "Test")]')
        self.browser.find_element_by_xpath('//*[contains(text(), "Test start date")]')
        self.browser.find_element_by_xpath('//*[contains(text(), "Test end date")]')
        
    
    def test_4_edit_education(self):
        
        # Login as staff
        self.browser.get(self.url_edit)
        username = self.browser.find_element_by_name("username")
        password = self.browser.find_element_by_name("password")
        login = self.browser.find_element_by_tag_name('button')
        username.send_keys('admin_test')
        password.send_keys('admin')
        login.click()
        time.sleep(1)

        # Click the edit button
        self.browser.get(self.url)
        block = self.browser.find_element_by_xpath('//*[contains(text(), "Test end date")]')
        edit_button = block.find_element_by_id('edit_button')
        edit_button.click()

        # Check the layout of the edit page
        form = self.browser.find_element_by_tag_name('form')
        facility = form.find_element_by_name("facility")
        title = form.find_element_by_name("title")
        Grade = form.find_element_by_name("Grade")
        start = form.find_element_by_name("date_start")
        end = form.find_element_by_name("date_end")
        submit = form.find_element_by_xpath('//*[contains(text(), "Publish")]')

        self.assertIn('Test name',facility.get_attribute('value')) 
        self.assertIn('Test title',title.get_attribute('value'))
        self.assertIn('Test',Grade.get_attribute('value')) 
        self.assertIn('Test start date',start.get_attribute('value'))
        self.assertIn('Test end date',end.get_attribute('value'))

        # Edit the content
        facility.send_keys(Keys.CONTROL,'a') 
        facility.send_keys(Keys.BACK_SPACE)
        facility.send_keys('University of Birmingham')
        submit.click()
        
        # Check if edit success
        self.browser.find_element_by_xpath('//*[contains(text(), "University of Birmingham")]')


    def test_5_delete_education(self):  
        # Login as staff
        self.browser.get(self.url_edit)
        username = self.browser.find_element_by_name("username")
        password = self.browser.find_element_by_name("password")
        login = self.browser.find_element_by_tag_name('button')
        username.send_keys('admin_test')
        password.send_keys('admin')
        login.click()
        time.sleep(1)
        
        # Click on the delete buttom
        self.browser.get(self.url)
        block = self.browser.find_element_by_xpath('//*[contains(text(), "Test end date")]')
        delete_button = block.find_element_by_id('delete_button')
        delete_button.click()

        # User should be redirect to cv page
        menu = self.browser.find_element_by_id('menu')
        rows = menu.find_elements_by_tag_name('a')  
        self.assertIn('Home Page',[row.get_attribute('textContent') for row in rows]) 
        self.assertIn('About',[row.get_attribute('textContent') for row in rows]) 
        self.assertIn('Experience',[row.get_attribute('textContent') for row in rows]) 
        self.assertIn('Education',[row.get_attribute('textContent') for row in rows]) 
        self.assertIn('Skills',[row.get_attribute('textContent') for row in rows]) 
        self.assertIn('Awards',[row.get_attribute('textContent') for row in rows])

        # Check the layout of the CV page
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_xpath('//*[contains(text(), "Test name")]')
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_xpath('//*[contains(text(), "Test title")]')
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_xpath('//*[contains(text(), "Test")]')
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_xpath('//*[contains(text(), "Test start date")]')
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_xpath('//*[contains(text(), "Test end date")]')
    
if __name__ == '__main__':  
    unittest.main(warnings='ignore')
    
