from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from account.models import CustomUser


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the requiredname
    fields, plus a repeated password."""
    user_id = forms.CharField(label="ID", widget=forms.TextInput)
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput)
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)
    name = forms.CharField(label='이름', widget=forms.TextInput)
    nickname= forms.CharField(label='닉네임', widget=forms.TextInput)

    class Meta:
        model = CustomUser
        fields = ('user_id', 'user_id', 'name', 'email', 'nickname', 'profile_image')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('user_id', 'password', 'name', 'email', 'nickname', 'profile_image', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('user_id', 'name', 'email', 'last_login', 'date_joined', 'is_admin', 'mail_receive', 'note_receive')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('user_id', 'password', 'nickname')}),
        ('개인정보', {'fields': ('name', 'email')}),
        ('수신여부', {'fields': ('mail_receive','note_receive',)}),
        ('권한', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_id', 'password1', 'password2', 'name', 'nickname', 'email'),
        }),
    )
    search_fields = ('user_id', 'name', 'email')
    ordering = ('date_joined',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(CustomUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)