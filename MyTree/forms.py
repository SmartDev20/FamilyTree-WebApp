from django import forms

from .models import NewTree


class NewTreeForm(forms.ModelForm) :
      class Meta :
          model = NewTree
          fields = ('name' , 'address','telephone' ,'gender' , 'job',) # '__all__'
