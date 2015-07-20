from django import forms
from _1327.polls.models import Poll


class PollForm(forms.ModelForm):

	class Meta:
		model = Poll
		exclude = ('participants', )
