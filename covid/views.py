from django.shortcuts import render
from .forms import *
from formtools.wizard.views import CookieWizardView
from .diagnose import generateletter

FORMS = [('symptomatic',symptomatic),
         ('symptoms',symptoms),
         ('currentsymptoms',currentsymptoms),
         ('dyspnea',dyspnea),
         ('o2',o2),
         ('o2reading',o2reading),
         ('acuity', acuity),
         ('chestpain', chestpain),
         ('lightheadedness',lightheadedness),
         ('vv', vv),
         ('highrisk', highrisk),
         ('clinic', clinic),
         ('exposure', exposure),
         ('constantexposure', constantexposure),
         ('vaccine', vaccine),
         ('covidtest', covidtest),
         ('healthcare', healthcare)

         ]

TEMPLATES = {'symptomatic':'symptomatic.html',
             'dyspnea':'dyspnea.html',
             'acuity':'acuity.html',
             'exposure':'exposure.html',
             'chestpain':'chestpain.html',
             'highrisk':'highrisk.html',
             'vaccine':'vaccine.html',
             'covidtest':'covidtest.html',
             'currentsymptoms':'currentsymptoms.html',
             'redflag':'generic.html'
             }


def showsymptoms(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('symptomatic') or {}
    symptomatic = cleaned_data.get('symptomatic')
    if symptomatic == 'True': #don't show 14 day question if they are currently symptomatic
        return False
    else:
        return True


def asymptomatic(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('symptomatic') or {}
    symptomatic = cleaned_data.get('symptomatic')
    if symptomatic == 'True': #don't show red flag questions if asymptomatic
        return True
    else:
        return False

def showo2(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('dyspnea') or {}
    if cleaned_data.get('dyspnea') != 'False' and cleaned_data != {}: #don't ask about dyspnea if they don't have it
        return True
    else:
        return False

def showo2reading(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('o2') or {}
    if cleaned_data.get('o2monitor') != 'True': #don't ask what their o2 reading is if they don't have a monitor
        return False
    else:
        return True

def showongoing(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('exposure') or {}
    if cleaned_data.get('exposure') == 'True': #don't ask what their o2 reading is if they don't have a monitor
        return True
    else:
        return False


class QuizWizard(CookieWizardView):
    def get_template_names(self):
        template = TEMPLATES.get(self.steps.current)
        if template:
            return template
        else:
            return 'generic.html'


    def done(self, form_list, **kwargs):
        patient = [form.cleaned_data for form in form_list]
        patientmessage = generateletter(patient)

        return render(self.request, 'results.html', {
            'form_data': [form.cleaned_data for form in form_list],'diagnosis': [patientmessage[0]],'worknote': [patientmessage[1]],'actions':[patientmessage[2]]})

