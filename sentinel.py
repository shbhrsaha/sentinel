
"""
    This script logs into SCORE and submits the course enrollment queue when enrollment spots open up on the course registrars' web site.
    Sending emails by Gmail SMTP adapted from http://segfault.in/2010/12/sending-gmail-from-python/
"""

from splinter import Browser
from bs4 import BeautifulSoup
import sys, urllib, time, datetime, smtplib

# ============== USER INPUT ============== #

NETID = "YOUR_PRINCETON_NETID"
PASSWORD = "YOUR_PRINCETON_PASSWORD"

# The security question keys are verbatim phrases from SCORE's
# security question prompt
SECURITY_QUESTIONS = {
                        "last high school" : "SECURITY_ANSWER",
                        "elementary school" : "SECURITY_ANSWER",
                        "middle name" : "SECURITY_ANSWER"
                     }

# Enter class section number and URL on registrar's web site here
CLASS_NUMBERS = {
                        "23410" : "http://registrar.princeton.edu/course-offerings/course_details.xml?courseid=002056&term=1142",
                }

# gmail information, used for sending email by Gmail SMTP
GMAIL_SENDER = "YOUR_GMAIL_ADDRESS"
GMAIL_PASSWORD = "YOUR_GMAIL_PASSWORD"

# number of seconds to wait before checking the registrar's web site again
WAIT_TIME = 30


# ========== END OF USER INPUT =========== #

# ============== FUNCTIONS =============== #


def submitQueue(NETID, PASSWORD, SECURITY_QUESTIONS):

    browser = Browser()

    # netid page
    browser.visit("https://puaccess.princeton.edu/psp/hsprod/EMPLOYEE/HRMS/h/?tab=DEFAULT")
    browser.fill('userid', NETID)
    browser.find_by_value("Continue").first.click()

    # password page
    browser.fill('Bharosa_Password_PadDataField', PASSWORD)
    browser.evaluate_script("Bharosa_Password_Pad.keyPress('ENTERKEY');")

    # security question page
    html = browser.html

    for key in SECURITY_QUESTIONS.keys():
        
        if key in html:
            
            answer = SECURITY_QUESTIONS[key]

    browser.fill('Bharosa_Challenge_PadDataField', answer)
    browser.evaluate_script("Bharosa_Challenge_Pad.keyPress('ENTERKEY');")

    time.sleep(2)

    # welcome to SCORE
    browser.find_link_by_text("Student Center").first.click()


    # student center, start by busting out of the iframe
    browser.visit("https://puaccess.princeton.edu/psc/hsprod/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?PORTALPARAM_PTCNAV=HC_SSS_STUDENT_CENTER&EOPP.SCNode=HRMS&EOPP.SCPortal=EMPLOYEE&EOPP.SCName=ADMN_SCORE&EOPP.SCLabel=&EOPP.SCPTcname=ADMN_SC_SP_SCORE&FolderPath=PORTAL_ROOT_OBJECT.PORTAL_BASE_DATA.CO_NAVIGATION_COLLECTIONS.ADMN_SCORE.ADMN_S200801281459482840968047&IsFolder=false&PortalActualURL=https%3a%2f%2fpuaccess.princeton.edu%2fpsc%2fhsprod%2fEMPLOYEE%2fHRMS%2fc%2fSA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL&PortalContentURL=https%3a%2f%2fpuaccess.princeton.edu%2fpsc%2fhsprod%2fEMPLOYEE%2fHRMS%2fc%2fSA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL&PortalContentProvider=HRMS&PortalCRefLabel=Student%20Center&PortalRegistryName=EMPLOYEE&PortalServletURI=https%3a%2f%2fpuaccess.princeton.edu%2fpsp%2fhsprod%2f&PortalURI=https%3a%2f%2fpuaccess.princeton.edu%2fpsc%2fhsprod%2f&PortalHostNode=HRMS&NoCrumbs=yes&PortalKeyStruct=yes")
    browser.select('DERIVED_SSS_SCL_SSS_MORE_ACADEMICS', "1005")
    browser.find_by_id("DERIVED_SSS_SCL_SSS_GO_1").first.click()

    # pick semester
    browser.choose("SSR_DUMMY_RECV1$sels$0", "1")
    browser.find_by_id("DERIVED_SSS_SCT_SSR_PB_GO").first.click()

    # select classes to add... class should already be in queue
    browser.find_by_id("DERIVED_REGFRM1_LINK_ADD_ENRL$115$").first.click()

    # confirm classes
    browser.find_by_id("DERIVED_REGFRM1_SSR_PB_SUBMIT").first.click()

def fetchEnrollmentData(class_number, url):
    
    enrolled = 0
    capacity = 0
    
    # Fetch HTML
    f = urllib.urlopen(url)
    html = f.read()
    
    # Get BeautifulSoup Object
    soup = BeautifulSoup(html)
    
    tr_list = soup.find_all('tr')
    
    for tr in tr_list:
    
        # find the row that matches the class number
        td_list = tr.find_all('td')

        if len(td_list) > 0:
            possibleClassNumber = td_list[0].get_text().strip()
        
            if class_number == possibleClassNumber:
        
                # this is the class section! Go get the enrollment data!
                dataSplit = td_list[5].get_text().split(":")
                enrolled = dataSplit[1].split("\n")[0]
                capacity = dataSplit[-1]
    
    return [int(enrolled), int(capacity)]

def generateEnrollmentDictionary():

    enrollment = {}
    
    for class_number in CLASS_NUMBERS.keys():
        enrollment[class_number] = fetchEnrollmentData(class_number, CLASS_NUMBERS[class_number])

    return enrollment

def send_email(netid, class_link, gmail_sender, password):

    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

    sender = "Class Sentinel <sentinel@example.com>"
    recipient = netid + "@princeton.edu"
    subject = "Course queue submitted!"
    body = "Class sentinel submitted your course queue because space opened up in this class: " + class_link

    headers = ["From: " + sender,
               "Subject: " + subject,
               "To: " + recipient,
               "MIME-Version: 1.0",
               "Content-Type: text/html"]
    headers = "\r\n".join(headers)

    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(gmail_sender, password)

    session.sendmail(sender, recipient, headers + "\r\n\r\n" + body)
    session.quit()


# ========== END OF FUNCTIONS ============ #


if __name__ == "__main__":

    # store the current enrollment data in a dictionary. Each value is a list of currently enrolled and enrollment limit
    original_enrollment = generateEnrollmentDictionary()

    # uncomment to immediately submit the course queue for the sample course
    # original_enrollment = {"23410" : [147,140]}

    while True:
        
        try:
            time.sleep(WAIT_TIME)
        
            print str(datetime.datetime.now()) + " Checking Enrollment"
            
            enrollment = generateEnrollmentDictionary()
            
            for class_number in CLASS_NUMBERS:
        
                opportunity = False
                
                # an opportunity opens up if the enrolled number drops or if the capacity goes up
                if enrollment[class_number][0] < original_enrollment[class_number][0]:
                    opportunity = True
                if enrollment[class_number][1] > original_enrollment[class_number][1]:
                    opportunity = True
                
                if opportunity:

                    submitQueue(NETID, PASSWORD, SECURITY_QUESTIONS)
                    original_enrollment = enrollment
                    send_email(NETID, CLASS_NUMBERS[str(class_number)], GMAIL_SENDER, GMAIL_PASSWORD)
                    print "Queue Submitted for Class: " + str(class_number)
        except:
            continue