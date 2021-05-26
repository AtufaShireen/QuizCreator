from django.forms.models import inlineformset_factory
from django.forms.models import BaseInlineFormSet
from django.forms import ModelForm
from .models import Quizzer,Questions
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
class RequiredFormSet(BaseInlineFormSet): # not required for update form
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def clean(self):
        if not any([form.has_changed() for form in self.forms]):
           
            raise ValidationError([{
                'question':ValidationError(_('Add at least one Question'),code='required')
                }])
        super().clean()
            
QuestionsFormset = inlineformset_factory(Quizzer,Questions,fields=['question','option_1','option_2','option_3','option_4','points','answer'],extra=1,formset=RequiredFormSet) # 

class QuizForm(ModelForm):
    class Meta:
        model=Quizzer
        fields=['title','tags','bg_pic','reattempt','private'] #

    def clean(self):
        super().clean()
        tn=self.cleaned_data.get('tags',[])
        if len(tn)<=2:
            raise ValidationError(_('Please add upto 3 tags'),code='required')