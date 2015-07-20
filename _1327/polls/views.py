import datetime

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from _1327.polls.forms import PollForm

from _1327.polls.models import Poll, Choice
from _1327.user_management.shortcuts import get_object_or_error


def list(request):
	running_polls = []
	finished_polls = []
	# do not show polls that start in the future and that a user is not allowed to see
	for poll in Poll.objects.filter(start_date__lte=datetime.date.today()):
		if request.user.has_perm(Poll.VIEW_PERMISSION_NAME):
			if datetime.date.today() <= poll.end_date and not poll.participants.filter(id=request.user.pk).exists():
				running_polls.append(poll)
			else:
				finished_polls.append(poll)

	return render(
		request,
		'polls_index.html',
		{
			"running_polls": running_polls,
			"finished_polls": finished_polls,
		}
	)


def results(request, poll_id):
	poll = get_object_or_error(Poll, request.user, ['polls.view_poll'], id=poll_id)

	if poll.start_date > datetime.date.today():
		# poll is not open
		raise Http404

	if not poll.participants.filter(id=request.user.pk).exists() and poll.end_date > datetime.date.today():
		messages.info(request, _("You have to vote before you can see the results!"))
		return HttpResponseRedirect(reverse('polls:vote', args=[poll.id]))

	return render(
		request,
		'polls_results.html',
		{
			"poll": poll,
		}
	)


def vote(request, poll_id):
	poll = get_object_or_error(Poll, request.user, ['polls.view_poll', 'polls.change_poll'], id=poll_id)

	if poll.start_date > datetime.date.today():
		# poll is not open
		raise Http404

	if poll.end_date < datetime.date.today() or poll.participants.filter(id=request.user.pk).exists():
		messages.info(request, _("You can not vote for polls that are already finished, or that you have already voted for!"))
		return HttpResponseRedirect(reverse('polls:results', args=[poll_id]))

	if request.method == 'POST':
		choices = request.POST.getlist('choice')
		if len(choices) == 0:
			messages.error(request, _("You must select one Choice at least!"))
			return HttpResponseRedirect(reverse('polls:vote', args=[poll_id]))
		if not poll.is_multiple_choice_question:
			if len(choices) != 1:
				messages.error(request, _("You can only select one option!"))
				return HttpResponseRedirect(reverse('polls:vote', args=[poll_id]))

		for choice_id in choices:
			choice = poll.choices.get(id=choice_id)
			choice.votes += 1
			choice.save()

		poll.participants.add(request.user)
		messages.success(request, _("We've received your vote!"))
		return HttpResponseRedirect(reverse('polls:results', args=[poll_id]))

	return render(
		request,
		'polls_vote.html',
		{
			"poll": poll,
			"widget": "checkbox" if poll.is_multiple_choice_question else "radio"
		}
	)


def create(request):
	if not request.user.has_perm('polls.add_poll'):
		return HttpResponseForbidden()

	if request.method == 'POST':
		form = PollForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('polls:list'))
	else:
		form = PollForm()

	ChoiceFormset = modelformset_factory(Choice, exclude=('index', 'poll', 'votes'))
	formset = ChoiceFormset(queryset=Choice.objects.filter(poll=form.instance.id))

	return render(
		request,
		'polls_create.html',
		{
			"form": form,
			"formset": formset,
		}
	)


