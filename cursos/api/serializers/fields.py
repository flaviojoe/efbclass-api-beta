# -*- coding: utf-8 -*-
from rest_framework import serializers


class UsuarioField(serializers.RelatedField):
	def to_representation(self, value):
		return value.get_full_name()
