from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from ckeditor.widgets import CKEditorWidget
from .forms import CustomUserForm
from .models import Services, Blog, Gallery, CustomUser

# Form for Blog admin with CKEditor
class BlogAdminForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['services', 'title', 'image', 'description']
        widgets = {
            'description': CKEditorWidget(),  # Using CKEditor for rich text editing
        }

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    form = CustomUserForm
    model = CustomUser
    list_display = ('email', 'username', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    ordering = ('email',)

    def get_fieldsets(self, request, obj=None):
        # Define fieldsets for editing existing users
        if obj is not None:
            if request.user.groups.filter(name='Admin-HostProvider').exists():
                return (
                    (None, {'fields': ('email', )}),
                    ('Personal info', {'fields': ('username', 'phone_number')}),
                    ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
                )
            else:
                return (
                    (None, {'fields': ('email',)}),
                    ('Personal info', {'fields': ('username', 'phone_number')}),
                )

        # Define fieldsets for adding new users
        if request.user.groups.filter(name='Admin-HostProvider').exists():
            return (
                (None, {'fields': ('email', 'password1', 'password2')}),  # Include password fields for confirmation
                ('Personal info', {'fields': ('username', 'phone_number')}),
                ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
            )
        else:
            return (
                (None, {'fields': ('email', 'password1', 'password2')}),  # Include password fields for confirmation
                ('Personal info', {'fields': ('username', 'phone_number')}),
            )

    def get_list_display(self, request):
        if request.user.groups.filter(name='Admin-HostProvider').exists():
            return ('email', 'username', 'is_active', 'is_staff')
        else:
            return ('email', 'username')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Admin-HostProvider').exists():
            return qs
        else:
            return qs.filter(email=request.user)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if not request.user.groups.filter(name='Admin-HostProvider').exists():
            # Set the email field to read-only
            if 'email' in form.base_fields:
                form.base_fields['email'].widget.attrs['readonly'] = 'readonly'

            # Restrict fields to only 'username' and 'phone_number' for non-admin users
            allowed_fields = ['email', 'username', 'phone_number']
            for field in list(form.base_fields.keys()):
                if field not in allowed_fields:
                    form.base_fields.pop(field)
        return form


# Blog Admin with CKEditor support
class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Admin-HostProvider').exists():
            return qs
        # else:
        #     return qs.filter(services__user=request.user)
        blogs = Blog.objects.filter(services__id=request.user.id-1)
        print(request.user.id)
        return blogs


    def get_list_display(self, request):
        if request.user.groups.filter(name='Admin-HostProvider').exists():
            return ('services', 'title', 'image', 'description')
        else:
            return ('services', 'title', 'image', 'description')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.groups.filter(name='Admin-HostProvider').exists():
            form.base_fields['services'].queryset = CustomUser.objects.filter(pk=request.user.pk)
        return form


# Services Admin
class ServicesAdmin(admin.ModelAdmin):
    # Define the readonly_fields attribute
    # readonly_fields = ['user']

    # def get_readonly_fields(self, request, obj=None):
    #     # Make the 'user' field read-only for non-admin users
    #     if not request.user.groups.filter(name='Admin-HostProvider').exists():
    #         return ['user']
    #     return super().get_readonly_fields(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.groups.filter(name='Admin-HostProvider').exists():
            # Set the queryset for the 'user' field to the current user
            form.base_fields['user'].queryset = CustomUser.objects.filter(pk=request.user.pk)
        return form

    def get_list_display(self, request):
        if request.user.groups.filter(name='Admin-HostProvider').exists():
            return ('service_title', 'short_description')
        else:
            return ('service_title', 'short_description', 'user')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Admin-HostProvider').exists():
            return qs
        elif qs.filter(user=request.user.id-1).exists():
            return qs.filter(user=request.user.id-1)
        else:
            return qs.filter(user=request.user.id)

    def get_fieldsets(self, request, obj=None):
        # Ensure the 'user' field is included in the fieldsets for non-admin users
        if not request.user.groups.filter(name='Admin-HostProvider').exists():
            return (
                (None, {'fields': ('user', 'service_title', 'short_description',)}),
            )
        return super().get_fieldsets(request, obj)

# Gallery Admin
class GalleryAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Admin-HostProvider').exists():
            return qs
        elif qs.filter(category__user=request.user.id-1).exists():
            return qs.filter(category__user=request.user.id-1)
        else:
            return qs.filter(category__user=request.user.id)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.groups.filter(name='Admin-HostProvider').exists():
            form.base_fields['category'].queryset = CustomUser.objects.filter(pk=request.user.pk)
        return form
        # if request.user.groups.filter(name='Admin-HostProvider').exists():
        #     return qs
        # else:
        #     return qs.filter(category__user=request.user)

# Register models in the admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Services, ServicesAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Gallery, GalleryAdmin)
