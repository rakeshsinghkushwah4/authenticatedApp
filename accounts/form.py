from django import forms
from accounts.models import MyProfile

class RegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter username','class':'input100'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter password','class':'input100'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter confirm password','class':'input100'}))
    class Meta:
        model = MyProfile
        fields = ['username','password','confirm_password','name','gender','phone','profile_pic','register_type']

        widgets={
            'name': forms.TextInput(attrs={'placeholder':'Enter name','class':'input100'}),
            'gender': forms.Select(attrs={'id':'gender','class':'form-control custom-selec selcls input100'}),
            'phone' : forms.TextInput(attrs={'placeholder':'Enter Phone','class':'input100'}),
            'register_type' : forms.Select(attrs={'id':'type','class':'form-control  custom-selec selcls input100'})
        }

class UserLogin(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter username','class':'input100'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter password','class':'input100'}))
