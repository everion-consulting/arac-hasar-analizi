from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UsernameField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import FrontendUser, HasarTahmin


class HasarTahminResource(resources.ModelResource):
    class Meta:
        model = HasarTahmin
        # İstersen buraya include/exclude, export_order vs. ekleyebilirsin


@admin.register(HasarTahmin)
class HasarTahminAdmin(ImportExportModelAdmin):
    resource_class = HasarTahminResource
    list_display = (
        "created_at",
        "marka",
        "model",
        "arac_turu",
        "rayic_bedel",
        "hasar_bedeli",
        "tahmini",
        "min_deger",
        "max_deger",
    )


class FrontendUserForm(forms.ModelForm):
    """
    Admin panelden frontend kullanıcısı oluştururken şifreyi plain text
    olarak girip, DB'de hash'li saklayabilmek için özel form.
    Normal Django User oluşturma ekranındaki kuralları taklit eder:
    - password1 / password2 doğrulaması
    - Django password validators
    """

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = FrontendUser
        fields = ["username", "is_active"]
        field_classes = {"username": UsernameField}

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(_("The two password fields didn’t match."))
        return password2

    def _post_clean(self):
        """
        Django'nun UserCreationForm'undaki gibi password validators çalışsın.
        """
        super()._post_clean()
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password2", error)

    def save(self, commit=True):
        frontend_user = super().save(commit=False)
        raw_password = self.cleaned_data["password1"]

        # Normal Django User ile ilişki kur: username aynı, şifre hash'li
        UserModel = get_user_model()
        django_user, _created = UserModel.objects.get_or_create(
            username=frontend_user.username,
            defaults={"is_staff": False, "is_superuser": False},
        )
        django_user.set_password(raw_password)
        django_user.is_active = frontend_user.is_active
        django_user.is_staff = False  # frontend kullanıcıları admin olmasın
        django_user.save()

        # FrontendUser içindeki password alanına da aynı hash'i yaz (senkron kalsın)
        frontend_user.password = django_user.password

        if commit:
            frontend_user.save()

        return frontend_user


@admin.register(FrontendUser)
class FrontendUserAdmin(admin.ModelAdmin):
    form = FrontendUserForm
    list_display = ("username", "is_active", "created_at")
    search_fields = ("username",)
