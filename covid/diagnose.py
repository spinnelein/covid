import datetime

hcwdisclaimer = '''<br><br>As a health care worker, your return to work guidelines are subject to change based on current COVID risk levels. Please contact your employer for more information regarding their policies. '''

signature = '''<br>
Please let us know if you have any further questions or concerns! 
E-visit provider'''

def isolateSymptomatic(patient):
    if patient.get('symptomatic') == 'True' or (patient.get('twoweeks')== 'True'):
        if patient.get('hadcovid') == 'True':
            return False #If they had COVID in the last 90 days, it's not COVID.
        actions = 'Isolate'
        if lastpcrtest(patient):
            try:
                if lastpcrtest(patient) > patient.get('symptomaticdate') and patient.get('testresult') == '0': #If the patient had a negative PCR test after getting sick
                    return False #they don't have covid and don't need to isolate.
                if lastpcrtest(patient) > patient.get('twoweeksstartdate') and patient.get('testresult') == '0':  # If the patient had a negative PCR test after getting sick
                  return False  # they don't have covid and don't need to isolate.
            except:
                pass
        if patient.get('severelyill') == 'True' or patient.get('immunocompromised') == "True":
            duration = 10 #isolate 10 days
        elif patient.get('healthcareworker') == 'True':
            duration = 7
        else:
            duration = 5
        if (datetime.datetime.now().date() - isolationdate(patient)).days > duration: #patient's isolation window is over
            actions = 'No action required. Isolation period over '
            letter = '''Thank you for reaching out with your concerns regarding COVID-19.  It sounds like you may have had a COVID or other upper respiratory infection recently, but your symptoms are improving.  Based on the date when your symptoms started, you no longer need to isolate. Isolation ends when it has been more than 5 days since your symptoms started, AND your fever is gone and your symptoms are improving. If you are still experiencing fever or respiratory symptoms that are not getting better, please contact KP for follow-up.'''
            if (patient.get('currentfever') == 'True' or patient.get('improving') == 'False') and ((datetime.datetime.now().date() - patient.get('symptomaticdate')).days > 5):
                letter = "Thank you for reaching out with your concerns regarding COVID-19.  It has been more than 5 days since your symptoms started, but you are still feeling sick.  Because of this, you need to continue isolation until you have been fever free for more than 24 hours and until your respiratory symptoms are improving. Symptoms such as mild cough or loss of taste or smell may persist for several weeks after your infection is over.  These symptoms are not a sign that you are still contagious.  If your symptoms are recurring after initial improvement, if your symptoms are worsening, or if you still have a fever after 1 week, you may need further evaluation to make sure that you don't have a more serious infection or secondary infection.  Please call (503)813-2000 to speak to one of our nurses to discuss symptoms if you are concerned."
                actions = "Prolonged illness, additional diagnosis required."
                return [letter.replace('\n', '<br>'), '', actions]
            elif patient.get('exposure') == 'True' and patient.get('testresult') != '1': #exposed after isolation is over
                return quarantine(patient)
            else:
                return False
        else:
            letter = '''I'm sorry to hear that you have not been feeling well.  Based on CDC guidelines regarding COVID-like symptoms, you need to isolate for ''' + str(duration) + ''' days, beginning on ''' + isolationdate(patient).strftime("%B %d, %Y") + ''' and ending on ''' + (isolationdate(patient)+datetime.timedelta(days=duration)).strftime("%B %d, %Y")+ '''.  This means that you should stay home (not go to work) and isolate from others in your home, wear a well-fitted mask if you must be around others, and do not travel during this time period.'''
            if duration > 5:
                yesand = False
                letter += ''' You need to isolate for longer than the normal guidelines due to '''
                if patient.get('severelyill') == 'True':
                    letter+= '''having been severely ill with COVID'''
                    yesand = True
                if patient.get('immunocompromised') == "True":
                    if yesand:
                        letter += ', '
                    yesand = True
                    letter += '''being immunocompromised'''
                if patient.get('healthcareworker') == 'True':
                    if yesand:
                        letter += ' and '
                    letter += '''being a health care worker'''
                letter += '.'

            letter += ''' After this date you can end your isolation if your fever is gone and your other symptoms are improving. If you are still experiencing fever or respiratory symptoms that are not getting better on '''+ (isolationdate(patient)+datetime.timedelta(days=duration)).strftime("%B %d, %Y") + ''' please contact KP for follow-up. You should not go to routine medical appointments for 20 days. If you have an appointment scheduled during this time, please reschedule or call to discuss if you need to be seen.'''
            if patient.get('healthcareworker') == 'True' and patient.get('severelyill') == 'False' and patient.get('immunocompromised') == "True":
                letter += "As an immunocompromised heath care worker you may return to work after 7 days (on " + (isolationdate(patient)+datetime.timedelta(days=7)).strftime("%B %d, %Y")
                letter += "), if you have had 2 negative rapid antigen tests 24 hours apart."
            if patient.get('healthcareworker') == 'True':
                letter += hcwdisclaimer
            letter += gettested(patient,'symptomaticisolation')


        worknote = ''
        if patient.get('wn') == 'True':
            actions += ''', Worknote Off for ''' + str(duration) + ''' days, beginning on ''' + isolationdate(patient).strftime("%B %d, %Y") + ''' and ending on ''' + (isolationdate(patient)+datetime.timedelta(days=duration)).strftime("%B %d, %Y")
            letter += '''<br>I have written a work note indicating these isolation guidelines.  This will authorize you to be off of work beginning on ''' + isolationdate(patient).strftime("%B %d, %Y") + ''' and ending on ''' + (isolationdate(patient)+datetime.timedelta(days=duration)).strftime("%B %d, %Y")+ '''.   You can print this work note by logging into KP.org and then going to "Medical Record" and then inside that "Letters" where you will find the letter I am writing.  

        Below there is a message that says "You requested a doctor's note. However, based on your interview, I don't think you need to stop your normal activities.". Please ignore this message. I do think we need to keep you out of work/school until your isolation period is over. 
        '''
            worknote = '''Please excuse patient from work during the time period outlined below.
            
            Due to '''
            if patient.get('testresult') == '1':
                worknote += "positive COVID test on " + patient.get('testdate').strftime("%B %d, %Y") + 'and '
            worknote += '''ongoing COVID symptoms. 
        They should follow CDC recommendations for isolation:

        - Stay home for ''' + str(
                duration) + ''' days. After that continue to wear a mask around others for ''' + str(
                10 - duration) + ''' additional days.
        Patient can stop home isolation under the following conditions: -5 days since start of symptoms. - no fever and symptoms improving x 24 hours.
        - If symptoms develop, get a test and stay home.
        '''
            if patient.get('healthcareworker') == 'True':
                worknote += '''<br>Health care workers w/o symptoms may be able to work after possible/confirmed exposure to COVID-19 & should check with their employer.'''
            worknote += '''<br>NOTE: This note also serves as an off work note and a return to work note.
                * Close Contact: Within 6 feet of someone for a cumulative total of 15 minutes or more over a 24-hour period with someone who has COVID-19.
                '''

        return [letter.replace('\n', '<br>'),worknote.replace('\n', '<br>'),actions]
    return False #They don't need to isolate.

def isolateAsymptomatic(patient):
    worknote = ''
    if patient.get('testresult') == '1': #if positive test results but no symptoms
        if patient.get('hadcovid') == "True" and patient.get('testtype') == 'PCR': #positive PCR for previous COVID patients means nothing
            return False #no isolation
        if patient.get('immunocompromised') == "True" or patient.get('healthcareworker') == 'True':
            duration = 10 #isolate 10 days
        else:
            duration = 5
        if (datetime.datetime.now().date() - isolationdate(patient)).days > duration: #patient's isolation window is over
            letter = 'You no longer need to isolate.'
            actions = "No action, isolation ended"
        else:
            letter = '''Thank you for reaching out with your concerns regarding COVID-19.  I'm sorry to hear that you have tested positive for COVID, but I'm glad to hear that you are not currently having any symptoms.  Because you have tested positive for COVID, '''
            letter += '''you need to isolate for ''' + str(duration) + ''' days, beginning on ''' + isolationdate(
                patient).strftime("%B %d, %Y") + ''' and ending on ''' + (isolationdate(patient) + datetime.timedelta(days=duration)).strftime("%B %d, %Y")
            letter += '''After this date you can end your isolation. '''
            if duration > 5:
                yesand = False
                letter += '''. You need to isolate for longer than the normal guidelines due to '''
                if patient.get('immunocompromised') == "True":
                    if yesand:
                        letter += ', '
                    yesand = True
                    letter += '''being immunocompromised'''
                if patient.get('healthcareworker') == 'True':
                    if yesand:
                        letter += 'and '
                    '''being a health care worker'''

            letter += '''This means that you should stay home and isolate from others in your home, well a well-fitted mask if you must be around others, and do not travel.  After your initial isolation ends, you should continue to take precautions for ''' + str(10-duration) + ''' additional days after your isolation ends.  This involves wearing a well-fitted mask any time you are around others inside your home or in public, not going to places where you are unable to wear a mask, and avoiding being around people who are at high risk for COVID complications.  You should not go to routine medical appointments for 20 days. If you have an appointment scheduled during this time, please reschedule or call to discuss if you need to be seen.  
            
            If you develop symptoms at any time between now and 10 days after your positive test, you should continue to isolate until you are fever-free for at least 24 hours and your symptoms are improving.
            '''
            letter += gettested(patient,'isolateAsymptomatic')
            if patient.get('healthcareworker') == 'True' and patient.get('immunocompromised') == "True":
                letter += "As an immunocompromised heath care worker you may return to work after to 7 days (on " + (isolationdate(patient)+datetime.timedelta(days=7)).strftime("%B %d, %Y")
                letter += "), if you have had 2 negative rapid antigen tests 24 hours apart."
            if patient.get('healthcareworker') == 'True' and patient.get('immunocompromised') == "False":
                letter += "As a heath care worker you may return to work after to 7 days (on " + (isolationdate(patient)+datetime.timedelta(days=7)).strftime("%B %d, %Y")
                letter += "), if you have taken a rapid antigen test with a negative result prior to returning to work."
            if patient.get('healthcareworker') == 'True':
                letter += hcwdisclaimer
            worknote = ''
            actions = '''Isolate'''
            if patient.get('wn') == 'True':
                actions += ''', Worknote Off for ''' + str(duration) + ''' days, beginning on ''' + isolationdate(patient).strftime("%B %d, %Y") + ''' and ending on ''' + (
                                  isolationdate(patient) + datetime.timedelta(days=duration)).strftime("%B %d, %Y")
                letter += '''<br>I have written a work note indicating that you have tested positive for COVID and outlining the isolation recommendations.  This will authorize you to be off of work beginning on ''' + isolationdate(patient).strftime("%B %d, %Y") + ''' and ending on ''' + (isolationdate(patient)+datetime.timedelta(days=duration)).strftime("%B %d, %Y") + '''.   You can print this work note by logging into KP.org and then going to "Medical Record" and then inside that "Letters" where you will find the letter I am writing.  
 
Below there is a message that says "You requested a doctor's note. However, based on your interview, I don't think you need to stop your normal activities.". Please ignore this message. I do think we need to keep you out of work/school until your quarantine period is over. 
'''

                worknote = '''Persons with positive COVID-19 testing with no symptoms & who were directed to care for themselves at home may discontinue isolation as below. 

If tested positive for COVID-19 with no symptoms:
- Stay home for '''+str(duration)+ ''' days.
- If you have no symptoms at the end of the '''+str(duration)+ ''' days, you can leave your home.  
- After that continue to wear a mask around others for '''+ str(10-duration)+''' additional days.
- Test on day 5 if possible.
- If symptoms develop, get a test and stay home. If you develop a fever, continue to stay home for 24 hours after your fever resolves.
'''
                if patient.get('healthcareworker') == 'True':
                    worknote += '''<br>Health care workers w/o symptoms may be able to work after possible/confirmed exposure to COVID-19 & should check with their employer.'''
                worknote += '''<br>NOTE: This note also serves as an off work note and a return to work note.
        * Close Contact: Within 6 feet of someone for a cumulative total of 15 minutes or more over a 24-hour period with someone who has COVID-19.
        '''
        return [letter.replace('\n', '<br>'),worknote.replace('\n', '<br>'), actions]
    return False #They don't need to isolate.

def quarantine(patient):
    if patient.get('exposure') == 'True':
        if patient.get('vaccinated') == 'True' or patient.get('hadcovid') == "True":
            return False #don't quarantine if you're fully vaccinated or have had covid recently
        else:
            exposuredate = getexposuredate(patient)
            letter = "Thank you for reaching out with your concerns regarding COVID-19.  Based on my review of your E-visit, you do not currently have COVID symptoms, but you have had a significant exposure, so you need to quarantine until we know if you have an infection or not."
            letter += "<br><br>"
            duration = 0
            if patient.get('ongoingexposure') == 'True':
                letter += '''<br>Because this is an ongoing exposure, you need to quarantine during the entire quarantine period of the individual you are exposed to as well as the recommended time period.'''
                duration += 10
            if patient.get('healthcareworker') == 'True':
                duration += 10
                letter +='''Since you are a health care worker, you need to quarantine for 10 days. (''' + exposuredate.strftime("%B %d, %Y") + ' to ' + (exposuredate+datetime.timedelta(days=duration)).strftime("%B %d, %Y") + '''). You may return to work after 7 days ('''+(exposuredate+datetime.timedelta(days=7)).strftime("%B %d, %Y") +''') if you have a negative antigen test within 48 hours before your return to work. '''
                letter += hcwdisclaimer
            else:
                duration +=5
                precautions = duration + 5
                letter += '''You need to quarantine for '''+str(duration)+''' days. (''' + exposuredate.strftime("%B %d, %Y") + ' to ' + (exposuredate+datetime.timedelta(days=duration)).strftime("%B %d, %Y") + ''') While you are quarantining, you should be cautious around other members of your household who have not been exposed and wear a well-fitted mask when you are in contact with them.  You should not travel. After this date, you should continue to take precautions for 10 days after your exposure.  This involves wearing a well-fitted mask any time you are around others inside your home or in public, not going to places where you are unable to wear a mask, and avoiding being around people who are at high risk for COVID complications.  You should continue to take precautions until ''' + (exposuredate+datetime.timedelta(days=precautions)).strftime("%B %d, %Y") + '''. You should not go to any routine medical appointments for 14 days. If you have an appointment scheduled during this time, please reschedule or call to discuss if you need to be seen.'''
                letter += '''. If you develop symptoms at any time between now and ''' +(exposuredate+datetime.timedelta(days=precautions)).strftime("%B %d, %Y") + ''', you should isolate and get a COVID test to determine if you have an infection.<br>'''
            letter += gettested(patient,'quarantine')
            actions = 'Quarantine'
            worknote = ''
            if patient.get('wn') == 'True':
                actions += ''', Worknote Off for ''' + str(duration) + ''' days, beginning on ''' + exposuredate.strftime("%B %d, %Y") + ' to ' + (exposuredate+datetime.timedelta(days=duration)).strftime("%B %d, %Y")
                letter += '''<br><br>I have written a work note indicating these quarantine guidelines.  This will authorize you to be off of work beginning on ''' + exposuredate.strftime("%B %d, %Y") + ' to ' + (exposuredate+datetime.timedelta(days=duration)).strftime("%B %d, %Y")+ '''.   You can print this work note by logging into KP.org and then going to "Medical Record" and then inside that "Letters" where you will find the letter I am writing.  

            Below there is a message that says "You requested a doctor's note. However, based on your interview, I don't think you need to stop your normal activities.". Please ignore this message. I do think we need to keep you out of work/school until your quarantine period is over. 
            '''

                worknote = '''Patient may have been exposed to a “close contact” with COVID-19. 
            They should follow CDC recommendations for quarantine:

            If exposed to someone with COVID-19:
            - Stay home for ''' + str(
                    duration) + ''' days. After that continue to wear a mask around others for ''' + str(
                    10 - duration) + ''' additional days.
            - If you can’t quarantine you must wear a mask for 10 days.
            - Test on day 5 if possible.
            - If symptoms develop, get a test and stay home.
            '''
                if patient.get('healthcareworker') == 'True':
                    worknote += '''<br>Health care workers w/o symptoms may be able to work after possible/confirmed exposure to COVID-19 & should check with their employer.'''
                worknote += '''<br>NOTE: This note also serves as an off work note and a return to work note.
                    * Close Contact: Within 6 feet of someone for a cumulative total of 15 minutes or more over a 24-hour period with someone who has COVID-19.]
                    '''
            if (datetime.datetime.now().date() - exposuredate).days > duration:  # patient's isolation window is over
                letter = '''You have been exposed to a COVID positive individual but no longer need to isolate. If you develop COVID symptoms please contact again.'''


            return [letter.replace('\n', '<br>'), worknote.replace('\n', '<br>'),actions]
    return False

def getexposuredate(patient):
    if patient.get('ongoingexposuredate'):
        return patient.get('ongoingexposuredate')
    else:
        return patient.get('exposuredate')

def isolationdate(patient):
    if patient.get('testresult') == '1': #patient has tested positive for COVID
        if patient.get('symptomatic') == 'True': #if symptomatic
            if datetime.datetime.today().date() - patient.get('testdate') < datetime.timedelta(days=10):#if the last positive test was within 10 days
                if patient.get('testdate') < patient.get('symptomaticdate'): #if the patient tested positive before showing symptoms
                    return patient.get('testdate') #isolate starting on the test date
                return patient.get('symptomaticdate') #isolate starting on the first day of symptoms
        return patient.get('testdate')  # isolate starting on the test date
    if patient.get('symptomatic') == 'True':
        return patient.get('symptomaticdate')
    if patient.get('twoweeks') == 'True':
        return patient.get('twoweeksstartdate')


def Testnoquarantine(patient):
    if patient.get('exposure') == 'True' and (patient.get('vaccinated') == 'True' or patient.get('hadcovid') == "True"):
        letter = '''Thank you for reaching out with your concerns regarding COVID-19.  
        Based on my review of your E-visit, you do not currently have COVID symptoms, but you have had a significant exposure.  
        
        Because '''
        if patient.get('vaccinated') == 'True':
            letter += '''you indicated that you are fully vaccinated against COVID-19'''
        else:
            letter += '''you have had a COVID infection in the past 90 days and are most likely protected from re-infection with COVID-19 within this time period'''
        letter +=''', the CDC currently does not recommend any work restrictions while waiting to see if symptoms develop.'''
        letter += '<br><br>'
        letter += gettested(patient,'testnoquarantine')
        letter += '''While you are waiting to see if symptoms develop, you should follow all recommended infection prevention and control practices while at work.  You should also be cautious around other members of your household who have not been exposed and wear a well-fitted mask when you are in contact with them.  You should not travel. You should not go to routine medical appointments for 14 days. If you have an appointment scheduled during this time, please reschedule or call to discuss if you need to be seen. You should continue these precautions until ''' + (getexposuredate(patient)+datetime.timedelta(days=10)).strftime("%B %d, %Y") +'.'
        letter += '<br><br>'
        letter += '''If you develop symptoms at any time between now and '''+ (getexposuredate(patient)+datetime.timedelta(days=10)).strftime("%B %d, %Y") +''', you should stay home from work, isolate, and get a '''
        if patient.get('hadcovid') == True:
            letter += "rapid at-home "
        letter +=  '''COVID test to determine if you have an infection.'''
        worknote = "Patient does not need a work note."
        actions = 'No quarantine or isolation required'
        return [letter.replace('\n', '<br>'), worknote.replace('\n', '<br>'),actions]

def nothing(patient):
    actions = ''
    letter = ''
    worknote = ''
    if patient.get('exposure') == 'False':
        letter = "Thank you for reaching out with your concerns regarding COVID-19.  Based on my review of your current symptoms and exposure history, you do not need to quarantine or isolate.  If you do develop symptoms or have new exposures in the future, please check in again for further recommendations."
        letter +=gettested(patient, 'none')
        worknote = 'Patient does not need a work note.'
        actions = 'No Actions'
    if patient.get('symptomatic') == "True" and patient.get('wn') == 'True':  # If they're sick but have no exposure and need a work note
        # and it's confirmed to not be COVID
        actions = 'Work note ' + patient.get('symptomaticdate').strftime("%B %d, %Y") + " to " + (patient.get('symptomaticdate') + datetime.timedelta(days=3)).strftime("%B %d, %Y")
        letter = '''I'm sorry to hear that you are not feeling well. Since you have '''
        if patient.get('testresult') == 'False':
            letter += 'tested negative for COVID-19,'
        elif patient.get('hadcovid') == 'True':
            letter += 'had and recovered from COVID in the last 90 days,'
        letter += ''' you do not need to isolate currently. This is because you are not at risk for passing COVID on to other people.  However, your symptoms may be due to another viral infection, so in order to prevent possible transmission of this virus, you should stay home until you have had no fever for 24 hours and your symptoms are starting to improve.'''
        letter += '''I have written a work note indicating that you are ill from non-COVID illness.  You can print this work note by logging into KP.org and then going to "Medical Record" and then inside that "Letters" where you will find the letter I am writing.

Below there is a message that says "You requested a doctor's note. However, based on your interview, I don't think you need to stop your normal activities.". Please ignore this message. Follow instructions in the work note that I gave you.
There's a 3 day work note on kp.org, starting on the day you got sick and ending on ''' + (
                        patient.get('symptomaticdate') + datetime.timedelta(days=3)).strftime("%B %d, %Y")
        worknote = '''Please excuse patient from work during the time period outlined below. Patient has tested negative for COVID, and may return to work after meeting the following criteria:
Return to work 24 hours after resolution of fever w/o fever reducing medications OR 24 hours after improvement of respiratory symptoms whichever is later. (Fever is defined as 100.0F or higher.)
'''
    return [letter.replace('\n', '<br>'), worknote.replace('\n', '<br>'),actions]


def lastpcrtest(patient):
    if patient.get('testresult') != 'False': #If the patient has been tested
        if patient.get('testtype') == 'PCR': #and it was a PCR test
            return patient.get('testdate') #return the date
    else:
        return False

def lasttest(patient): #returns date of last covid test
    if patient.get('testresult') != 'False': #If the patient has been tested
        return patient.get('testdate') #return the date
    else:
        return False

def generateletter(results):
    patient = {}

    for d in results:
        patient.update(d)  # put the results into a single dictionary

    letter = diagnose(patient)
    letter = mixins(patient,letter)
    kaiserblurb = '''<br><br>You can also get further recommendations and guidance from KP Employee health. You can call employee health at 1-844-951-2060 and leave a message or visit https://sp-cloud.kp.org/sites/EmployeeHealth for further information or to make a report online. '''
    if patient.get('kpemployee') == 'True':
        letter[0] += kaiserblurb.replace('\n', '<br>')
    letter[0] += signature.replace('\n', '<br>')
    return letter

def gettested(patient,action):
    getpcr = '''<br><br>You should get tested with a laboratory PCR test.
        
        To schedule a laboratory PCR COVID test please go to kp.org or the KP app. Follow the links to schedule an appointment and select your reason for your appointment as "COVID-19 test". You will be asked a couple of questions and then will be able to see the testing appointments we have available.

Please wear a mask when you go to get tested. When you arrive, follow signs for COVID-19 testing or go to registration. Let them know you are there for COVID-19 testing
The results usually come back within 36 hours and will be available on your KP.org account to review.
If you need proof of your test result, log into your KP.org account. Right-click on the test result to print out a copy of the result.

If you are unable to schedule a COVID test through Kaiser, you can get a free COVID-19 test at more than 200 community sites:
<ul>  
<li>Oregon testing sites: https://govstatus.egov.com/or-oha-covid-19-testing</li>  
<li>Washington testing sites: https://www.doh.wa.gov/Emergencies/COVID19/TestingforCOVID19</li> 
</ul>'''
    rapid = '''You should get tested with an FDA-approved rapid at-home antigen test for COVID.  
       
       You can either get an at-home rapid test through your Kaiser pharmacy by scheduling an appointment on kp.org to pick one up, or you can try to find one at your local pharmacy.'''

    anytest = '''You can get testing with either a FDA-approved rapid at-home test or schedule a laboratory PCR test. 

    You can either get an at-home rapid test through your Kaiser pharmacy by scheduling an appointment on kp.org to pick one up or you can try to find one at any local pharmacy or online. 

    To schedule a clinic PCR COVID test please go to kp.org or the KP app. Follow the links to Schedule an appointment and select your reason for your appointment as "COVID-19 test". You will be asked a couple of questions and then will be able to see the testing appointments we have available.

    Please wear a mask when you go to get tested. When you arrive, follow signs for COVID-19 testing or go to registration. Let them know you are there for COVID-19 testing
    The results usually come back within 36 hours and will be available on your KP.org account to review.
    If you need proof of your test result, log into your KP.org account. Right-click on the test result to print out a copy of the result.

    If you are unable to schedule a COVID test through Kaiser, you can get a free COVID-19 test at more than 200 community sites:
    <ul>  
    <li>Oregon testing sites: https://govstatus.egov.com/or-oha-covid-19-testing</li>  
    <li>Washington testing sites: https://www.doh.wa.gov/Emergencies/COVID19/TestingforCOVID19</li> 
    </ul>'''

    hadcovid = '''Because you have tested positive for COVID-19, we do not recommend that you retest for COVID with a laboratory PCR test within 90 days after you tested positive (even if you develop new symptoms).  This is because there may still be inactive viral particles from your last infection that could cause repeat PCR tests to read positive.  A positive PCR COVID test within 90 days of previous COVID infection does not give us any information about if you have a new infection.'''

    message = ''

    negativerapid = '''Even though you tested negative with a home rapid antigen test, this does not completely rule out a COVID infection, especially if you tested early in your infection or when you didn't have symptoms.  If you are having ongoing symptoms suspicious for COVID-19 or if you have had a serious exposure to COVID-19, I would recommend either retesting with an at-home rapid test 24 hours or more after the initial negative test or scheduling a laboratory COVID-19 test (if you have not had another infection with COVID-19 within the past 90 days). '''
 #To improve results, antigen tests should be used twice over a three-day period with at least 24 hours and no more than 48 hours between tests.
    #symptomatic isolation
    if action =='symptomaticisolation':
        if patient.get('hadcovid') == "False":
            if lastpcrtest(patient): #if patient had a pcr test
                if patient.get('testdate') > isolationdate(patient) or (patient.get('testresult') == '1' and (datetime.datetime.today().date() - patient.get('testdate')) < datetime.timedelta(days=90)): #if patient tested after their symptoms date, or tested positive
                    pass #if tested after symptoms, or tested positive any time in the last 90 days
                else:
                    message += getpcr #PCR test if negative antigen test and (early in symptoms or significant exposure) and no COVID90
            elif patient.get('testresult') != '1':
                if patient.get('testresult') == '0':
                    message += negativerapid
                message += "I recommend that you get a COVID test within about 48 hours since your symptoms began"
                message += getpcr


        if patient.get('hadcovid') == "True":
            message += '''Since you have had COVID and recovered in the last 90 days, you should do two consecutive rapid tests (NOT PCR lab tests) to find out if you have COVID again.'''
            message += ''' If the result of this is negative, please contact again so we can update your isolation plan to reflect a negative COVID result.'''
        return message
    if action == 'isolateAsymptomatic':
        if patient.get('hadcovid') == "False":
            if lastpcrtest(patient):  # if patient had a pcr test
                if patient.get('testdate') > isolationdate(patient) or (patient.get('testresult') == '1' and (
                        datetime.datetime.today().date() - patient.get('testdate')) < datetime.timedelta(
                        days=90)):  # if patient tested after their symptoms date, or tested positive
                    pass  # if tested after symptoms, or tested positive any time in the last 90 days
                else:

                    message += getpcr#ryan when should they get tested
            else:
                message += 'You tested positive with an at home rapid antigen test.  In order to verify this result, you should get a laboratory PCR test.  '
                message += getpcr

        if patient.get('hadcovid') == "True":
            message += '''Since you have had COVID and recovered in the last 90 days, you should do two consecutive rapid tests (NOT PCR lab tests) to find out if you have COVID again.'''
        message += ''' If the result of this is negative, please contact again so we can update your isolation plan to reflect a negative COVID result.'''    # quarantine
        return message

    if action == 'quarantine':
        message = '''You should get tested for COVID 5 days after your exposure, even if you are asymptomatic.'''
        if patient.get('testresult') == '0':
            message += negativerapid
        if patient.get('hadcovid') == "True":
            message += rapid
            message += hadcovid
        else:
            message += anytest

    if action == 'testnoquarantine':
        message = '''You should get tested for COVID 5 days after your exposure, even if you are asymptomatic.'''
        if patient.get('hadcovid') == "True":
            message += rapid
            message += hadcovid
        else:
            message += anytest
    if action == "none":
        if patient.get('hadcovid') == 'True':
            message = hadcovid
        else:
            message = '''You do not need to get tested for COVID unless you develop symptoms.'''


    return message

def mixins(patient,letter):
    message = letter[0]
    worknote = letter[1]
    actions = letter[2]

    if ((patient.get('highrisk') == 'True' and patient.get('dyspnea') == 'Mild')
            or (patient.get('o2') == '94' and patient.get('dyspnea') == 'Mild')
            or patient.get('lightheadedness') == 'True'
            or patient.get('clinic') == "clinic"
            or patient.get('chestpain') == 'OK'
            or (patient.get('highrisk') == 'True' and patient.get('vv') == 'True')
        ):
        message += "<br><br>Based on the symptoms you are having currently, I think that you need to have an office visit for further evaluation.  I will have the scheduling staff contact you today to get an appointment.  If you miss the call or have further questions, please call (503)813-2000 to talk to a staff member.  If your symptoms are getting worse, please go to urgent care for further evaluation."
        officevisit = True
        actions += "Schedule office visit"
    else:
        officevisit = False

    if (patient.get('vv') == 'True'
        or (patient.get('highrisk') == 'False' and patient.get('dyspnea') == 'Mild')
        or patient.get('clinic') == "video"
        and officevisit == False
        ):
        message += "<br><br>Based on the symptoms that you are having currently, I think that you should have a virtual visit to discuss your concerns with a provider.  I will have the scheduling staff contact you today to get an appointment.  If you miss the call or have further questions, please call (503)813-2000 to talk to a staff member."
        actions += ", Schedule video visit"

    if 'Quarantine' or 'Isolate' in actions:
        if patient.get('pregnant') == 'True':
            actions += ', Televisit to discuss pregnancy and COVID'
            message +='<br><br>I think you should also have a telehealth visit to discuss guidelines and considerations for COVID around the time of pregnancy.'


    if patient.get('treatment') == 'True':
        message += '''<br><br>Regarding potential treatments for COVID such as monoclonal antibodies and/or antiviral medications:

The previously available monoclonal antibody treatment (Regeneron) is no longer being administered as it is not effective against the Omicron variant which is now the predominant COVID variant in the population.

All treatments, monoclonal antibody IV infusions and oral antiviral medication, are specialized non-FDA approved medication released for emergency use. The medication is distributed and allocated by state and remains in extremely short supply.  Kaiser Permanente Northwest has developed a robust ethical system to proactively connect patients at greatest risk to all COVID-19 treatment options.  '''

    if patient.get('vaccinated') == "vaccinated": #vaccinated, not boosted.
        message += '''<br> <br>It looks like you have completed your primary COVID-19 vaccination series, but you have not yet received your booster shot.  For now, the best strategy to prevent serious illness with COVID is to get vaccinated and boosted at the appropriate and recommended times as outlined by the CDC.  You are now eligible for a COVID booster vaccine with either of the mRNA vaccines currently available (either Pfizer or Moderna).

For the latest COVID-19 vaccines and resources, please see:
https://healthy.kaiserpermanente.org/oregon-washington/health-wellness/coronavirus-information/covid-vaccine?kp_shortcut_referrer=kp.org/covidvaccine 
OR call our recorded hotline at 1-855-550-0951. Also available in Spanish.'''

    if patient.get('vaccinated') == "partial":
        message += '''<br><br>It looks like you have not yet completed your primary COVID-19 vaccination series.  For now, the best strategy to prevent serious illness with COVID is to get vaccinated and boosted at the appropriate and recommended times as outlined by the CDC.  I would recommend that you get your COVID vaccines updated as soon as possible.

For the latest COVID-19 vaccines and resources, please see:
https://healthy.kaiserpermanente.org/oregon-washington/health-wellness/coronavirus-information/covid-vaccine?kp_shortcut_referrer=kp.org/covidvaccine 
OR call our recorded hotline at 1-855-550-0951. Also available in Spanish.
'''

    if patient.get('vaccinated') == "False": #no vaccines
        message += '''<br><br>It looks like you have not yet been vaccinated against COVID-19.  For now, the best strategy to prevent serious illness with COVID is to get vaccinated and boosted at the appropriate and recommended times as outlined by the CDC.  I would recommend that you get started with the COVID vaccination series as soon as possible.

For the latest COVID-19 vaccines and resources, please see:
https://healthy.kaiserpermanente.org/oregon-washington/health-wellness/coronavirus-information/covid-vaccine?kp_shortcut_referrer=kp.org/covidvaccine 
OR call our recorded hotline at 1-855-550-0951. Also available in Spanish.'''


    return [message.replace('\n', '<br>'), worknote.replace('\n', '<br>'),actions]


def diagnose(patient):

    if isolateSymptomatic(patient):
        return isolateSymptomatic(patient)

    if isolateAsymptomatic(patient):
        return isolateAsymptomatic(patient)

    if quarantine(patient):
        return quarantine(patient)

    if Testnoquarantine(patient):
        return Testnoquarantine(patient)

    if nothing(patient):
        return nothing(patient)
    return ["I got lost. ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR","ERROR "]

