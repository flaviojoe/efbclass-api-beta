# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import FAQ
from core.mixins import ExcludeAuditFieldsAdminForm


@admin.register(FAQ)
class FAQAdmin(ExcludeAuditFieldsAdminForm, admin.ModelAdmin):
    list_display = ['id', 'pergunta', 'criado_por', 'modificado_por']
    list_display_links = ['pergunta']

    def get_queryset(self, request):
        return super(FAQAdmin, self).get_queryset(request=request).select_related('criado_por', 'modificado_por')
