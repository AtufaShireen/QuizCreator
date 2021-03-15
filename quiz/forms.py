# from django.forms.models import inlineformset_factory #  BaseInlineFormSet,
from . import models
# from django.utils.translation import ugettext_lazy as _

# from publishing.utils.forms import is_empty_form, is_form_persisted


# def is_empty_form(form):
#     """
#     A form is considered empty if it passes its validation,
#     but doesn't have any data.
#     This is primarily used in formsets, when you want to
#     validate if an individual form is empty (extra_form).
#     """
#     if form.is_valid() and not form.cleaned_data:
#         return True
#     else:
#         # Either the form has errors (isn't valid) or
#         # it doesn't have errors and contains data.
#         return False


# def is_form_persisted(form):
#     """
#     Does the form have a model instance attached and it's not being added?
#     e.g. The form is about an existing Book whose data is being edited.
#     """
#     if form.instance and not form.instance._state.adding:
#         return True
#     else:
#         # Either the form has no instance attached or
#         # it has an instance that is being added.
#         return False


# class BaseQuestionsFormset(BaseInlineFormSet):
#     class Meta:
#         model = models.Quizzer

#     def add_fields(self, form, index):
#         super(BaseQuestionsFormset, self).add_fields(form, index)

#         # save the formset in the 'nested' property
#         form.nested = AnswersFormset(
#             instance=form.instance,
#             data=form.data if form.is_bound else None,
#             files=form.files if form.is_bound else None,
#             prefix='answer-%s-%s' % (
#                 form.prefix,
#                 AnswersFormset.get_default_prefix()))

#     def is_valid(self):
#         result = super(BaseQuestionsFormset, self).is_valid()

#         if self.is_bound:
#             for form in self.forms:
#                 if hasattr(form, 'nested'):
#                     result = result and form.nested.is_valid()

#         return result

#     def save(self, commit=True):

#         result = super(BaseQuestionsFormset, self).save(commit=commit)
#         for form in self.forms:
#             if hasattr(form, 'nested'):
#                 if not self._should_delete_form(form):
#                     form.nested.save(commit=commit)

#         return result

#     def _is_adding_nested_inlines_to_empty_form(self, form):
#         """
#         Are we trying to add data in nested inlines to a form that has no data?
#         e.g. Adding Images to a new Book whose data we haven't entered?
#         """
#         if not hasattr(form, 'nested'):
#             # A basic form; it has no nested forms to check.
#             return False

#         if is_form_persisted(form):
#             # We're editing (not adding) an existing model.
#             return False

#         if not is_empty_form(form):
#             # The form has errors, or it contains valid data.
#             return False

#         # All the inline forms that aren't being deleted:
#         non_deleted_forms = set(form.nested.forms).difference(
#             set(form.nested.deleted_forms)
#         )

#         # At this point we know that the "form" is empty.
#         # In all the inline forms that aren't being deleted, are there any that
#         # contain data? Return True if so.
#         return any(not is_empty_form(nested_form) for nested_form in non_deleted_forms)

#     def clean(self):
#         """
#         If a parent form has no data, but its nested forms do, we should
#         return an error, because we can't save the parent.
#         For example, if the Book form is empty, but there are Images.
#         """
#         super().clean()

#         for form in self.forms:
#             if not hasattr(form, 'nested') or self._should_delete_form(form):
#                 continue

#             if self._is_adding_nested_inlines_to_empty_form(form):
#                 form.add_error(
#                     field=None,
#                     error=_('You are trying to add image(s) to a book which '
#                             'does not yet exist. Please add information '
#                             'about the book and choose the image file(s) again.'))


# QuestionsFormset = inlineformset_factory(models.Quizzer, models.Questions,exclude=['quizz','slug'])
# AnswersFormset = inlineformset_factory(models.Questions, models.Answer, fields=['option', 'coorect'], extra=1)
