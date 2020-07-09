from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import *

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_confirm= forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'email_address')

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password2_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords don't match")
        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField(label= ("Password"),
        help_text= ("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = CustomUser
        fields = ('username','email_address', 'password', 'account_type', 'is_active')

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email_address','is_active')
    list_filter = ('is_active','account_type')
    fieldsets = (
        (None, {'fields': ('username', 'email_address','password')}),
        ('Permissions', {'fields': ('account_type','is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email_address', 'password', 'password_confirm')}
        ),
    )
    list_display_links = ('username', 'email_address')
    search_fields = ('username','email_address',)
    ordering = ('username','email_address',)
    filter_horizontal = ()

admin.site.unregister(Group)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(AccountType)
admin.site.register(UserProfile)
admin.site.register(UserLogs)
admin.site.register(LogDetails)
