from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):  

    def setUp(self):  
        self.browser = webdriver.Firefox()
        self.url = 'http://localhost:8000/cv'
        self.url_edit = 'http://localhost:8000/cv/new/'
        self.url_new_experience = 'http://localhost:8000/cv/new/experience'
        self.url_new_skills = 'http://localhost:8000/cv/new/skills'
        self.url_new_education = 'http://localhost:8000/cv/new/education'
        self.url_new_award = 'http://localhost:8000/cv/new/award'
        

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
        username.send_keys('admin')
        password.send_keys('990903')
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
        
        #login as staff
        username.send_keys('admin')
        password.send_keys('990903')
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
        facility.send_keys('University of Nottingham Ningbo China')
        title.send_keys(Keys.CONTROL,'a')
        title.send_keys(Keys.BACK_SPACE)
        title.send_keys('BSc Student')
        Grade.send_keys(Keys.CONTROL,'a')
        Grade.send_keys(Keys.BACK_SPACE)
        Grade.send_keys('4.0')
        start.send_keys(Keys.CONTROL,'a')
        start.send_keys(Keys.BACK_SPACE)
        start.send_keys('September 2017')
        end.send_keys(Keys.CONTROL,'a')
        end.send_keys(Keys.BACK_SPACE)
        end.send_keys('July 2021')
        submit.click()
        
        #test if the layout change
        self.browser.get(self.url)

        # The creator can see their education item
        self.browser.find_element_by_xpath('//*[contains(text(), "University of Nottingham Ningbo China")]')
        self.browser.find_element_by_xpath('//*[contains(text(), "BSc Student")]')
        self.browser.find_element_by_xpath('//*[contains(text(), "4.0")]')
        self.browser.find_element_by_xpath('//*[contains(text(), "September 2017")]')
        self.browser.find_element_by_xpath('//*[contains(text(), "July 2021")]')
        
    def test_4_delete_education(self):  
    
    def test_5_edit_education(self):
    
if __name__ == '__main__':  
    unittest.main(warnings='ignore')
    
