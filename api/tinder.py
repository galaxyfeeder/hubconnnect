from flask import Blueprint, jsonify
import requests
import random
import os
from connector import train, test

def blueprint(client):
    bp = Blueprint('tinder', __name__)

    @bp.route('/like', methods=['POST', 'GET'])
    def like():
        user = client.get_default_database().users.find_one()
        langs = get_languages_information(user['actual'][0])
        train(langs, True)

        n = get_next_users()
        return jsonify(get_extra_information_from_logins(n))

    @bp.route('/dislike', methods=['POST', 'GET'])
    def dislike():
        user = client.get_default_database().users.find_one()
        langs = get_languages_information(user['actual'][0])
        train(langs, False)

        n = get_next_users()
        return jsonify(get_extra_information_from_logins(n))

    def get_languages_information(login):
        repos = requests.get('https://api.github.com/users/'+login+'/repos?client_id='+os.environ.get('CLIENT_ID')+'&client_secret='+os.environ.get('CLIENT_SECRET')).json()
        languages = []
        for repo in repos:
            languages.append(repo['language'])
        return list(set(languages))

    def get_extra_information_from_login(login):
        languages = get_languages_information(login)
        if None in languages:
            languages.remove(None)
        user = requests.get('https://api.github.com/users/'+login+'?client_id='+os.environ.get('CLIENT_ID')+'&client_secret='+os.environ.get('CLIENT_SECRET')).json()
        user['languages'] = languages
        return user

    def get_extra_information_from_logins(logins):
        users = []
        for login in logins:
            user = get_extra_information_from_login(login)
            users.append(user)
        return users

    def get_next_users():
        user = client.get_default_database().users.find_one()

        if len(user['actual']) > 0:
            client.get_default_database().users.update({}, {'$push': {'choosed': user['actual'][0]}})
            user = client.get_default_database().users.find_one()

            fol = requests.get('https://api.github.com/users/'+user['actual'][0]+'/followers?client_id='+os.environ.get('CLIENT_ID')+'&client_secret='+os.environ.get('CLIENT_SECRET')).json()
            followers = []
            for f in fol:
                if f['login'] not in user['actual'] and f['login'] not in user['choosed']:
                    followers.append(f['login'])
            omega = list(set(user['omega'] + followers))

            for u in omega:
                langs = get_languages_information(u)
                valid = test(langs)
                if not valid:
                    omega.remove(u)

            if user['actual'][0] in omega:
                omega.remove(user['actual'][0])

            client.get_default_database().users.update({}, {'$pop': {'actual': -1}})
            if len(omega) > 0:
                added = False
                i = 0
                while not added and i < len(omega):
                    if omega[i] in user['actual']:
                        i += 1
                    else:
                        client.get_default_database().users.update({}, {'$push': {'actual': omega[i]}})
                        omega.remove(omega[i])
                        added = True

                user = client.get_default_database().users.find_one()
                added = False
                while not added and i < len(omega):
                    if omega[i] in user['actual']:
                        i += 1
                    else:
                        if len(user['actual']) < 3 and len(omega) > 3-len(user['actual']):
                            client.get_default_database().users.update({}, {'$push': {'actual': omega[i]}})
                            omega.remove(omega[i])
                        added = True

            client.get_default_database().users.update({}, {'$set': {'omega': omega}})

            user = client.get_default_database().users.find_one()
            if len(user['actual']) > 0:
                return user['actual']
        return []

    return bp
