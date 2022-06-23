from django import forms
from .models import ListCross


class UserForm(forms.Form):


    cross = forms.ModelChoiceField(queryset=ListCross.objects.all(), label="Cross", empty_label="Выберите Cross", widget=forms.Select(attrs={
"class":"form-control"}))
    login = forms.CharField(max_length=100, label='Ведите логин', widget=forms.TextInput(attrs={"class": "form-control"}))
    pasword = forms.CharField(max_length=100, label='Введите пароль', widget=forms.TextInput(attrs={"class": "form-control", "type": "password"}))
    reg = forms.CharField(max_length=100, label='Введите наименование задачи, которую необходимо удалить. Множественные задачи вводить через '
                                                'запятую. Например: PCE_2G, KOM, SPB, '
                                                'ANR_2G',
                          widget=forms.TextInput(attrs={"class": "form-control"}))
    date = forms.DateField(label='Дата начала', widget=forms.DateInput(attrs={"class": "dateInput", "type": "date", 'name': "date"}))
    date2 = forms.DateField(label='Дата окончания', widget=forms.DateInput(attrs={"class": "dateInput", "type": "date", 'name': "date"}))


