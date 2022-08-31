
from datetime import datetime, date, timedelta
from django import forms
from django.forms import DateInput, TextInput, ImageField
from django.forms import widgets
from django.core.exceptions import ValidationError
from django.core import validators

from main.models import Peoples, Otpuska, Tabel, Proba, Programm


class UserForm(forms.ModelForm):
 #   form_name=forms.CharField(label='Имя:')
 #   form_familia=forms.CharField(label='Фамилия:')
 #   form_img=forms.ImageField()

    class Meta:
        model=Peoples
        fields=["name", "sename","familia", "photo", "female", "dateOfBirth", "dolzhnost"]
        widgets= {"dateOfBirth":DateInput(attrs={'type':'date'}),
                  "name":TextInput(attrs={'placeholder':'Введите имя'})
                  }


class OtpuskForm(forms.ModelForm):

    class Meta:
        model=Otpuska
        fields=["title_otpusk", "nachOtpusk", "kolvoDney", "zayvlenie"]
        widgets = {"nachOtpusk": DateInput(format='%Y-%m-%d', attrs={'type':'date'}),
                   }

#       def clean(self):
#            cleaned_data = self.cleaned_data
            # Check 1: Must have valid user.
            # To Be Developed
 #           return cleaned_data


class Search(forms.Form):
    search_familia=forms.CharField(initial='Фамилия',  label='Фамилия')
    search_name=forms.CharField(initial='Имя', label='Имя')


class EditForm(forms.ModelForm):
    programma = forms.ModelMultipleChoiceField(
        queryset=Programm.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:

        model=Peoples
        fields=["id", "name", "sename","familia", "female", "dateOfBirth", "dolzhnost",  "dateStartWork",  "otdel_people"]
        widgets= {"dateOfBirth":DateInput(format='%Y-%m-%d', attrs={'type':'date'}),
                  "dateStartWork": DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                  "name":TextInput(attrs={'placeholder':'Введите имя'}),
                  "sename": TextInput(attrs={'placeholder':'Отчество'}),

                  }

class ProbaForm(forms.Form):
        programma = forms.ModelMultipleChoiceField(
            queryset=Programm.objects.all(),
            widget=forms.CheckboxSelectMultiple
        )



class ZayavaForm(forms.Form):
    zayvlenie=forms.ImageField(required=False)



#class EditForm(forms.Form):
#    name=forms.CharField(max_length=50)
#    sename=forms.CharField(max_length=50)
#    familia=forms.CharField(max_length=100)
#    female=forms.CharField(max_length=10)
#    dolzhnost=forms.CharField(max_length=100)

 #   dateOfBirth=forms.DateField()
 #   photo=forms.ImageField()


class DateForm(forms.Form):
    date=forms.CharField(required=False, widget=DateInput(format='%d-%m-%Y', attrs={'type': 'month'}), label='КАЛЕНДАРЬ')

 #   def clean(self):
 #       super().clean()
 #       errors={}
 #       if not self.cleaned_data['date']:
 #           errors['date']=ValidationError('Укажите дату')
 #       if errors:
 #           raise ValidationError(errors)

#    def clean_date(self):
#        val= self.cleaned_data['date']
#        self.cleaned_data['date']=datetime.strptime(val, "%Y-%m")

#        return val
        #date=forms.ChoiceField(choices=((1,'a'), (2,'b'), (3,'c')))


class TabelForm(forms.Form):
    typeSmena=[(7, '7'),
               (4, '4'),
               (12, '12'),
               (16, '16')]
    confirmWork = forms.ChoiceField(choices=typeSmena, label="Введите исправление")
    deleteWork=forms.BooleanField(label="Удалить?", required=False)


class CreateWorkDayForm(forms.ModelForm):

    class Meta:
        model=Tabel
        fields=['dataTabel', 'workTime', 'primechanie']
        widgets = {"dataTabel": DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                   "primechanie":TextInput(attrs={'placeholder':'Укажите, за что переработка'})
                   }

class CreateTabelNewDay(forms.Form):
    tabelDateWork=forms.DateField(required=False, widget=DateInput(format='%Y-%m-%d', attrs={'type': 'date'}), label=False)



#class CreateWorkDayForm(forms.Form):
#    typeWorkday = [(7, '7'),
#                 (4, '4'),
#                 (12, '12'),
#                 (16, '16')]
#    newDateWorkday=forms.DateField(required=False, widget=DateInput(format='%d-%m-%Y', attrs={'type': 'date'}), label="Выбери дату:")
 #   newWorkday=forms.ChoiceField(choices=typeWorkday, required=False, label="Рабочий день:")

class manForm(forms.ModelForm):
     class Meta:
         model=Proba
         fields=['name', 'sename', 'age', 'e_mail', 'data']
         widgets = {"data": DateInput(format='%d-%m-%Y', attrs={'type': 'date'})}



