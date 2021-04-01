from django.forms.models import inlineformset_factory
from django.forms.models import BaseInlineFormSet
from django.forms import ModelForm
from .models import Quizzer,Questions
# class RequiredFormSet(BaseInlineFormSet): # not required for update form
#     def __init__(self, *args, **kwargs):
#         super(RequiredFormSet, self).__init__(*args, **kwargs)
        
#         self.forms[0].empty_permitted = False
#         print('----------self.forms[0]',self.forms[0])
            
QuestionsFormset = inlineformset_factory(Quizzer,Questions,fields=['question','option_1','option_2','option_3','option_4','answer'],extra=1) # ,formset=RequiredFormSet

class QuizForm(ModelForm):
    class Meta:
        model=Quizzer
        fields=['title','tags','bg_pic','reattempt']