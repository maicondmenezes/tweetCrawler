from django.forms import ModelForm
from .models import Querie

class QuerieForm(ModelForm):
    class Meta:
        model = Querie
        fields = [ 'entry', 'start_day', 'end_day', 'rank_size' ]
        
