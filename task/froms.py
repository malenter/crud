from django  import forms
from .models import Task
class Taskfrom(forms.ModelForm):
    class Meta:
        model=Task
        fields=['title','description','important']
        widget ={
            'title':forms.TextInput(attrs={'class':'form-control'}),
             'description':forms.Textarea(attrs={'class':'form-control'}),
              'important':forms.CheckboxInput(attrs={'class':'forms-check-input m-auto'})
            }
    
    