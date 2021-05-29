from rest_framework import serializers


class ExcludeAuditFieldsAdminForm:
    exclude = ['criado_por', 'modificado_por']


class AuditFieldsSerializersMixin(object):
    criado_por = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # criado_por = serializers.ReadOnlyField(source='criado_por.username')
    # modificado_por = serializers.ReadOnlyField(source='modificado_por.username')


class AssociandoUserRequestMixin(object):

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(criado_por=user, modificado_por=user)


class SetExtraForms(object):

    def get_extra(self, request, obj=None, **kwargs):
        return 0
