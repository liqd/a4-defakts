from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from adhocracy4.projects import models


def set_is_archived_true(modeladmin, request, queryset):
    queryset.update(is_archived=True)


set_is_archived_true.short_description = _('archive')


def set_is_archived_false(modeladmin, request, queryset):
    queryset.update(is_archived=False)


set_is_archived_false.short_description = _('dearchive')


class ProjectAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['information'].widget = CKEditorUploadingWidget(
            config_name='collapsible-image-editor')
        self.fields['result'].widget = CKEditorUploadingWidget(
            config_name='collapsible-image-editor')

    class Meta:
        model = models.Project
        fields = '__all__'


class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    list_display = (
        '__str__', 'organisation', 'is_draft', 'is_archived', 'created'
    )
    list_filter = ('is_draft', 'is_archived', 'organisation',
                   'is_app_accessible')
    search_fields = ('name',)
    raw_id_fields = ('moderators', 'participants')
    date_hierarchy = 'created'

    actions = [
        set_is_archived_true,
        set_is_archived_false,
    ]

    fieldsets = (
        (None, {
            'fields': ('name', 'organisation')
        }),
        (_('Information and result'), {
            'fields': ('description', 'information', 'result'),
        }),
        (_('Settings'), {
            'classes': ('collapse',),
            'fields': ('access', 'is_draft', 'is_archived',
                       'is_app_accessible', 'moderators', 'participants')
        }),
        (_('Images'), {
            'classes': ('collapse',),
            'fields': ('image', 'image_copyright', 'tile_image',
                       'tile_image_copyright')
        }),
        (_('Contact'), {
            'classes': ('collapse',),
            'fields': ('contact_name', 'contact_address_text',
                       'contact_phone', 'contact_email', 'contact_url'),
        }),
    )


# Overwrite adhocracy4.projects.admin
admin.site.unregister(models.Project)
admin.site.register(models.Project, ProjectAdmin)
