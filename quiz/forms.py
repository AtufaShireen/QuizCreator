from django.forms.models import inlineformset_factory
from django.forms import ModelForm
QuestionsFormset = inlineformset_factory(Quizzer,Questions,fields=['question','option_1','option_2','option_3','option_4','answer'],extra=1)

class QuizForm(ModelForm):
    class Meta:
        model=Quizzer
        fields=['title','tags']