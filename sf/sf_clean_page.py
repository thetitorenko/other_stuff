""" Clean SF web pages script v0.2 """

import os, re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from html.entities import name2codepoint


# Function to get a list of all HTML files in a given directory
def get_html_files(directory):
    html_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            # Check if the file has a .html extension
            if file.endswith('.html'):
                # Add the absolute path of the HTML file
                html_files.append(os.path.join(root, file))
    return html_files  # Return the list of HTML file paths


# Get the absolute path to the current script and call function
script_dir = os.path.dirname(os.path.abspath(__file__))
html_files = get_html_files(script_dir)

# Stage 1: Cleaning web pages
# Looping through files, cleaning and save them
for html_file in html_files:
    # Open the HTML file
    with open(html_file, 'r', encoding='utf-8') as f:
        html_ = f.read()

    # Remove the SingleFile's comment
    cleaned_html = re.sub(r'<!--.*?-->', '', html_, flags=re.DOTALL)

    # def unescape(s):
    #     for name in name2codepoint:
    #         s = s.replace(f'&{name};', chr(name2codepoint[name]))
    #     return s

    # corrected_html = unescape(str(cleaned_html))

    # Parse the HTML file
    soup = BeautifulSoup(cleaned_html, 'html.parser')

    # List of classes to remove
    classes_to_remove = [
        'sf-header__navigation-and-user-menu',              # User menu and link to main page
        'sf-breadcrumbs sf-courseware-page__breadcrumbs',   # Address bar
        'sequence-tab-view-navigation__tabs-container',     # Navigation bar
        'sequence-tab-view-navigation__button-with-fade',   # Navigation arrow
        'sf-sequence-tab-view__numbers',                    # Unit number
        'sf-footer',                                        # Footer
        # Modules button
        'sf-round-icon-button sf-round-icon-button--large sf-round-icon-button--white sf-courseware-page__modules-button',
        'sc-dEVLtI GnPHU uw__messenger-layout',             # Support button
        'sf-sequence-tab-view__nav-buttons',                # Navigation buttons
        'sf-exam-timer sf-exam-wrapper-timer',              # Exam timer
        ]

    # Loop through the classes and remove the tags
    for class_name in classes_to_remove:
        tags_to_remove = soup.find_all(class_=class_name)
        for tag in tags_to_remove:
            tag.decompose()

    # Save the modified HTML file
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))

# Stage 2: Cleaning answers
# Looping through files
for html_file in html_files:
    # Create a new objects to start the ChromeDriver service
    service = Service()
    options = webdriver.FirefoxOptions()
    options.set_preference('javascript.enabled', False)
    driver = webdriver.Firefox(service=service, options=options)

    # Load the web page
    driver.get(f'file:///{html_file}')

    # Get the HTML content
    html_ = driver.page_source

    # Parse the HTML file
    soup = BeautifulSoup(html_, 'html.parser')
    
    # List of classes to remove
    classes_to_remove = [
        'status-icon',              # Answer status (check mark) 1
        'indicator-container',      # Answer status (check mark) 2
        'feedback-hint-correct',    # Answer feedback 1
        'feedback-content',         # Answer feedback 2
        'submission-feedback',      # Answer attempt counter
        'notification success notification-submit',    # Answer mark counter 1
        'problem-progress',         # Answer mark counter 2
        ]

    # Iterate over all classes in classes_to_remove
    for class_name in classes_to_remove:
        # Use CSS selector to find elements with the class
        for element in soup.select(f'.{class_name}'):
            print(element)
            # Decompose (delete) the element
            element.decompose()

    # Write the modified HTML to a new file
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    # Close the Selenium driver
    driver.quit()
