from django import forms
from scrapingApp.models import UserProfileInfo


class newUserForm(forms.ModelForm):
    verify_email = forms.EmailField(label='Enter Your Email Again')
    Confirm_password = forms.CharField(label='Enter Your Passward Again')

    class Meta():
        model=UserProfileInfo
        fields="__all__"

    def clean(self):
        all_clean_data = super().clean()
        email = all_clean_data['email']
        vmail = all_clean_data['verify_email']
        passw = all_clean_data['password']
        vpass = all_clean_data['Confirm_password']
        if email != vmail:
            raise forms.ValidationError("MAKE SURE EMAIL MATCH")
        if passw != vpass :
            raise forms.ValidationError("MAKE SURE PASSWORD MATCH")
