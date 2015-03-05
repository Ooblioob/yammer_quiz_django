# Create your views here.
from django.http import Http404
from django.shortcuts import render_to_response
import requests
import random
import re
from .models import question_text

def get_profiles(request):
	social = request.user.social_auth.get(provider='yammer')
	access_token = social.extra_data['access_token']

	users = request.session.get('users', None)

	if not users:
		users = get_users(access_token)
		request.session['users'] = users

	picture_users = get_picture_users(users)

	# get 4 random users
	quiz_profiles = random.sample(picture_users, 5)
	answer = quiz_profiles[random.randint(0,4)]

	all_question = question_text.objects.all()
	question = all_question[random.randint(0,len(all_question)-1)].question_text
	question = question.replace("{name}", answer['user'])

	return render_to_response('get_profile.html', {'quiz_profiles': quiz_profiles, 'question': question, 'answer': answer})

def get_users(access_token):
	users = []
	page = 1
	while True:
		response = requests.get(
	    	'https://www.yammer.com/api/v1/users.json?page=%d' % page,
	    	headers = {'Authorization': 'Bearer %s' % access_token['token']})
		if response.json() == []:
			break
		users.extend(response.json())
		page += 1
	return users

def get_picture_users(users):
	picture_users = []
	pattern = re.compile('.+no_photo.png$')
	for user in users:
		if not pattern.match(user['mugshot_url']):
			url = user['mugshot_url_template'].replace('{width}', '400').replace('{height}', '400')
			picture_users.append({'user': user['full_name'], 'pic': url})

	return picture_users