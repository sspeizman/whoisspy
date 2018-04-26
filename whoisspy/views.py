import math

from django.urls import reverse
from django.shortcuts import render, redirect
from .models import Phrase, Category, UserProfile, Group

def home(request):
	groups = Group.objects.all()
	data = {'groups': groups}
	return render(request, 'whoisspy/home.html', data)

def group_view(request, group_id):
	group = Group.objects.get(id=group_id)
	users = UserProfile.objects.filter(group=group)
	data = {'users': users, 'group': group}
	return render(request, 'whoisspy/groupview.html', data)

def start_game(request):
	UserProfile.objects.update(is_active=False)
	#users = list(UserProfile.objects.filter(id__in=user_ids).order_by('?'))
	user_profiles = UserProfile.objects.all().order_by('?')
	user_list = list(user_profiles)
	user_count = len(user_list)
	spy_count = math.ceil(user_count/2)-1
	categories = Category.objects.order_by('?')
	category = categories[0]
	phrases = list(Phrase.objects.filter(category=category).order_by('?'))
	spy_word = phrases[0]
	print(spy_word)
	plebe_word = phrases[1]
	print(plebe_word)
	spies = user_list[0:spy_count]
	print(spies)
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
	if request.method=="POST":
		user_profile.is_dead=True
		user_profile.save()
		print(request.POST.get('kill'))
		return redirect(reverse('game'))
	data = {'user_profile':user_profile}
	return render(request, 'whoisspy/viewuser.html', data)

def continue_game(request):
	user_profiles = UserProfile.objects.filter(is_active=True)
	spy_count = user_profiles.filter(is_spy=True).filter(is_dead=False).count()
	print(spy_count)
	if spy_count==0:
		return redirect(reverse('endgame'))
	data = {'user_profiles':user_profiles, 'spy_count':spy_count}
	return render(request, 'whoisspy/startgame.html', data)

def end_game(request):
	users = UserProfile.objects.filter(is_active=True)
	spies = users.filter(is_spy=True)
	data = {'users':users, 'spies':spies}
	return render(request, 'whoisspy/endgame.html', data)

