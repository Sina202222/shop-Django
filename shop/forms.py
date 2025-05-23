from crispy_forms.helper import FormHelper
from allauth.account.forms import LoginForm,SignupForm,ChangePasswordForm,ResetPasswordForm,ResetPasswordKeyForm,SetPasswordForm
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.utils.translation import gettext_lazy as _  # این خط را اضافه کنید




        
# class PasswordChangeForm(ChangePasswordForm):
#       def __init__(self, *args, **kwargs):
#         super(PasswordChangeForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper(self)

#         self.fields['oldpassword'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-2','placeholder':'Enter currunt password','id':'password3'})
#         self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-2','placeholder':'Enter new password','id':'password4'})
#         self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-2','placeholder':'Enter confirm password','id':'password5'})
#         self.fields['oldpassword'].label="Currunt Password"
#         self.fields['password2'].label="Confirm Password"
# class PasswordResetForm(ResetPasswordForm):
#       def __init__(self, *args, **kwargs):
#         super(PasswordResetForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper(self)

#         self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control mb-2','placeholder':' Enter Email','id':'email1'})
#         self.fields['email'].label="Email"
# class PasswordResetKeyForm(ResetPasswordKeyForm):
#       def __init__(self, *args, **kwargs):
#         super(PasswordResetKeyForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-2','placeholder':'Enter new password','id':'password6'})
#         self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-2','placeholder':'Enter confirm password','id':'password7'})
#         self.fields['password2'].label="Confirm Password"
# class PasswordSetForm(SetPasswordForm):
#       def __init__(self, *args, **kwargs):
#         super(PasswordSetForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-2','placeholder':'Enter new password','id':'password8'})
#         self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter confirm password','id':'password9'})
#         self.fields['password2'].label="Confirm Password"