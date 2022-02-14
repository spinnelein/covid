from django import forms



class symptomatic(forms.Form):
    def clean(self):
        symptomatic = self.cleaned_data.get('symptomatic')
        date = self.cleaned_data.get('symptomaticdate')
        if symptomatic == 'True' and not date:
            raise forms.ValidationError('Please select the date when the symptoms began')
    symptomatic = forms.ChoiceField(label = "Is the patient currently experiencing any symptoms that may be related to COVID?", choices=((False, 'No'), (True, 'Yes')),required=False)
    symptomaticdate = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),label = "If so, when did the symptoms begin?",required=False)

class currentsymptoms(forms.Form):
    currentfever = forms.ChoiceField(label = "Has the patient had a fever within the past 24 hours?", choices=((False, 'No'), (True, 'Yes')),required=False)
    improving = forms.ChoiceField(label = "Are their symptoms improving from when they started?", choices=((True, 'Yes'), (False, 'No')),required=False)

class symptoms(forms.Form):
    def clean(self):
        ended = self.cleaned_data.get('twoweeks')
        enddate = self.cleaned_data.get('twoweeksstartdate')
        startdate = self.cleaned_data.get('twoweeksenddate')
        if ended == 'True' and not enddate and not startdate:
            raise forms.ValidationError('Please select the date when the symptoms ended')
    twoweeks = forms.ChoiceField(label = "Has the patient had any COVID related symptoms in the last 10 days?", choices=((False, 'No'), (True, 'Yes')))
    twoweeksstartdate = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),
                                   label="If so, when did the symptoms begin?", required=False)
    twoweeksenddate = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),label = "If so, when did the symptoms end?",required=False)

class dyspnea(forms.Form):
    def clean(self):
        severity = self.cleaned_data.get('dyspnea')
        if severity == 'Severe':
            raise forms.ValidationError('Patient needs to go to the Emergency Room')
    dyspnea = forms.ChoiceField(label="Has the patient been experiencing any shortness of breath (dyspnea)?",
                                      choices=((False, 'None'), ('Mild', 'Mild'),('Moderate', 'Moderate'),('Severe', 'Severe')))

class o2(forms.Form):
    o2monitor = forms.ChoiceField(label = "Does the patient have an oximeter?", choices=((False, 'No'), (True, 'Yes')),required=False)

class lightheadedness(forms.Form):
    lightheadedness = forms.ChoiceField(label = "Is the patient experiencing any lightheadedness?", choices=((False, 'No'), (True, 'Yes')),required=False)

class o2reading(forms.Form):
    def clean(self):
        o2 = int(self.cleaned_data.get('o2sat'))
        if o2 < 90 :
            raise forms.ValidationError('Patient needs to go to the Emergency Room')
    o2sat = forms.ChoiceField(label="What is the O2Sat?",
                                      choices=((100, 'Over 94%'),(94,'90-94'),(89,'Less than 90')))


class acuity(forms.Form):
    def clean(self):
        acuity = self.cleaned_data.get('acuity')
        if acuity == 'True':
            raise forms.ValidationError('Patient needs to go to the Emergency Room')
    acuity = forms.ChoiceField(label = "Are there any changes in mental status or signs of severe hypoxia?", choices=((False, 'No'), (True, 'Yes')),required=False)

class chestpain(forms.Form):
    def clean(self):
        suspicious = self.cleaned_data.get('chestpain')
        if suspicious == 'suspicious':
            raise forms.ValidationError('Patient needs to go to the Emergency Room')
    chestpain = forms.ChoiceField(label = "Is the patient having chest pain?", choices=((False, 'No'), ('suspicious', 'Yes, suspicious'), ('OK', "Yes, but not suspicious")),required=False)

class vv(forms.Form):
    vv = forms.ChoiceField(label = "Is the patient requesting an appointment with a provider?", choices=((False, 'No'), (True, 'Yes')),required=False)

class highrisk(forms.Form):
    highrisk = forms.ChoiceField(label = "Is the patient at high risk for severe disease with COVID?", choices=((False, 'No'), (True, 'Yes')),required=False)
    immunocompromised = forms.ChoiceField(label="Is the patient moderately or severely immunocompromised?",
                                 choices=((False, 'No'), (True, 'Yes')), required=False)
    severlyill = forms.ChoiceField(label="Has the patient been hospitalized for COVID in the last 2 weeks?",
                                 choices=((False, 'No'), (True, 'Yes')), required=False)
    pregnant = forms.ChoiceField(label="Is the patient pregnant or recently pregnant?",
                                 choices=((False, 'No'), (True, 'Yes')), required=False)

class clinic(forms.Form):
    clinic = forms.ChoiceField(label = "Do you feel that the patient needs to be evaluated by a provider?", choices=((False, 'No'), ("clinic", 'in-person appointment'), ("video", 'Video appointment'), ("ER", 'emergency evaluation')),required=False)

class exposure(forms.Form):
    def clean(self):
        exposure = self.cleaned_data.get('exposure')
        date = self.cleaned_data.get('exposuredate')
        if exposure == 'True' and not date:
            raise forms.ValidationError('Please select the date of the most recent exposure')
    exposure = forms.ChoiceField(label = "Has the patient been exposed to a COVID positive individual in the last 10 days?", choices=((False, "No/I don't know"),(True, 'Yes') ))
    exposuredate = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),label = "If so, when was the most recent exposure?",required=False)

class constantexposure(forms.Form):
    def clean(self):
        ongoing = self.cleaned_data.get('ongoingexposure')
        date = self.cleaned_data.get('ongoingexposuredate')
        if ongoing == 'True' and not date:
            raise forms.ValidationError('Please select the date')
    ongoingexposure = forms.ChoiceField(label="Is it an ongoing exposure?",
                                 choices=((False, "No"),(True, 'Yes')), required=False)
    ongoingexposuredate = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),
                       label="If so, what was the first date that the person the patient is exposed to had a positive COVID test or COVID symptoms?",
                       required=False)

class vaccine(forms.Form):
    vaccinated = forms.ChoiceField(label="What is the patient's COVID vaccination status?",
                              choices=((False, 'No vaccines'), (True, 'Up to date (Vaccinated and boosted)'), ('vaccinated', "Vaccinated but not boosted"), ('partial','Partially Vaccinated')))

class covidtest(forms.Form):
    def clean(self):
        tested = self.cleaned_data.get('testresult')
        date = self.cleaned_data.get('testdate')
        if tested != 'False' and not date:
            raise forms.ValidationError("Please select the date of the patient's recent COVID test")
    testresult = forms.ChoiceField(label="What was the result of the patient's most recent COVID test?",
                                choices=((False, "Not Applicable"),(0, "Negative"), (1,"Positive")))
    testdate = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),label = "What was the date of the patient's most recent COVID test?",required=False)
    testtype = forms.ChoiceField(label="What was the type of the patient's most recent COVID test?",
                                choices=((False, "Not Applicable"),('PCR', "Lab PCR"), ('Rapid',"Rapid At-Home Test") ))

    hadcovid = forms.ChoiceField(label="Have they tested positive for COVID in the last 11-90 days and recovered from the acute infection?",
                                choices=((False, "No"),(True, "Yes")))

class healthcare(forms.Form):
    healthcareworker = forms.ChoiceField(label="Is the patient a health care worker?",
                                choices=((False, "No"), (True,"Yes")))
    kpemployee = forms.ChoiceField(label="If so, do they work for Kaiser Permanente?",
                                choices=((False, "No"), (True,"Yes")))
    treatment = forms.ChoiceField(label="Is the patient requesting information about COVID-19 treatment options?",
                                choices=((False, "No"), (True,"Yes")))
    wn = forms.ChoiceField(label="Is the patient requesting a work note?",
                                choices=((True,"Yes"),(False, "No")))
