import math

from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, UpdateView 
from .models import Phrase, Category, UserProfile, Group

def home(request):
	groups = Group.objects.exclude(name='Custom Group')
	UserProfile.objects.update(is_active=False, is_spy=False, is_dead=False)
	num_player_options = range(3,21)
	data = {
		'groups': groups,
		'num_player_options': num_player_options,
	}
	return render(request, 'whoisspy/home.html', data)

class CustomGroup(View):

	def get(self, request, *args, **kwargs):
		group, created = Group.objects.get_or_create(name='Custom Group')
		for existing_user in group.userprofile_set.all():
			existing_user.delete()
		for player in range(int(request.GET.get('num_players'))):
			up = UserProfile.objects.create(is_active=True)
			up.group.add(group)
			up.save()
		return redirect(reverse('startgame'))

def group_view(request, group_id):
	try:
		group = Group.objects.get(id=group_id)
		user_profiles = UserProfile.objects.filter(group=group)
	except Group.DoesNotExist:
		group = None
		user_profiles = UserProfile.objects.exclude(group__name='Custom Group')
	if request.method=='POST':
		selected_ids = request.POST.getlist('check')
		for selected_id in selected_ids:
			player = user_profiles.get(id=selected_id)
			player.is_active=True
			player.save()
		return redirect(reverse('startgame'))
	data = {'user_profiles': user_profiles, 'group': group}
	return render(request, 'whoisspy/groupview.html', data)

def start_game(request):
	user_profiles = UserProfile.objects.filter(is_active=True).order_by('?')
	user_list = list(user_profiles)
	user_count = len(user_list)
	if user_count < 9:
		spy_count = 2
	elif user_count < 13:
		spy_count = 3
	elif user_count < 17:
		spy_count = 4
	else:
		spy_count = 5
	# spy_count = math.ceil(user_count/2)-1
	categories = Category.objects.order_by('?')
	category = categories[0]
	phrases = list(Phrase.objects.filter(category=category).order_by('?'))
	spy_word = phrases[0]
	plebe_word = phrases[1]
	spies = user_list[0:spy_count]
	for spy in spies:
		spy.is_spy=True
		spy.phrase=spy_word
		spy.is_active=True
		spy.save()
	plebes = user_list[spy_count:]
	for plebe in plebes:
		plebe.is_spy=False
		plebe.phrase=plebe_word
		plebe.is_active=True
		plebe.save()
	data = {'spy_count':spy_count, 'user_profiles':user_profiles.order_by('?')}
	return render(request, 'whoisspy/startgame.html', data)

def view_user(request, user_id):
	user_profile = UserProfile.objects.get(id=user_id)
	if 'change_name' in request.GET:
		user_profile.name = request.GET.get('change_name')
		user_profile.save()
	if request.method=="POST":
		user_profile.is_dead=True
		user_profile.save()
		return redirect(reverse('game'))
	data = {'user_profile':user_profile}
	return render(request, 'whoisspy/viewuser.html', data)

def continue_game(request):
	user_profiles = UserProfile.objects.filter(is_active=True)
	spy_count = user_profiles.filter(is_spy=True).filter(is_dead=False).count()
	pleb_count = user_profiles.filter(is_spy=False).filter(is_dead=False).count()
	if spy_count==0:
		return redirect(reverse('endgame'))
	if pleb_count==0:
		return redirect(reverse('losegame'))
	if spy_count + pleb_count < 3:
		return redirect(reverse('losegame'))
	data = {'user_profiles':user_profiles, 'spy_count':spy_count}
	return render(request, 'whoisspy/startgame.html', data)

def end_game(request):
	users = UserProfile.objects.filter(is_active=True)
	spies = users.filter(is_spy=True)
	remaining_plebs = users.filter(is_spy=False).filter(is_dead=False)
	for pleb in remaining_plebs:
		pleb.score += 1
		pleb.save()
	data = {'users':users, 'spies':spies}
	return render(request, 'whoisspy/endgame.html', data)

def lose_game(request):
	users = UserProfile.objects.filter(is_active=True)
	spies = users.filter(is_spy=True)
	for spy in spies.filter(is_dead=False):
		spy.score += 1
		spy.save()
	data = {'users':users, 'spies':spies}
	return render(request, 'whoisspy/losegame.html', data)

