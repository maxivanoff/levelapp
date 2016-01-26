from django import forms

class SubmitJobForm(forms.Form):

    inputfile = forms.FileField(label='Select a File', help_text='Energy curve file')
    name = forms.CharField(max_length=128, help_text="Molecule's name")
    i1 = forms.IntegerField(help_text="Atomic number of the first atom")
    m1 = forms.IntegerField(help_text="Mass of the first atom")
    i2 = forms.IntegerField(help_text="Atomic number of the second atom")
    m2 = forms.IntegerField(help_text="Mass of the second atom")

