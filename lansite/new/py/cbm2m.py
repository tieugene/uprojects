from django import oldforms
from django.db import models
from django.utils.functional import curry

class CheckBoxManyToMany(models.ManyToManyField):
	def get_manipulator_field_objs(self):
		if self.rel.raw_id_admin:
			return [oldforms.RawIdAdminField]
		else:
			choices = self.get_choices_default()
		return [curry(oldforms.CheckboxSelectMultipleField, choices=choices)]

	def get_manipulator_fields(self, opts, manipulator, change, name_prefix='', rel=False, follow=True):
		"""
		Returns a list of oldforms.FormField instances for this field. It
		calculates the choices at runtime, not at compile time.
		name_prefix is a prefix to prepend to the "field_name" argument.
		rel is a boolean specifying whether this field is in a related context.
		"""
		field_objs, params = self.prepare_field_objs_and_params(manipulator, name_prefix)
		# BooleanFields (CheckboxFields) are a special case. They don't take is_required.
		if 'is_required' in params:
			del params['is_required']
		# Finally, add the field_names.
		field_names = self.get_manipulator_field_names(name_prefix)
		return [man(field_name=field_names[i], **params) for i, man in enumerate(field_objs)]
