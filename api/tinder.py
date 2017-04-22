from flask import Blueprint, jsonify
import requests
import random

def blueprint(client):
    bp = Blueprint('tinder', __name__)

    @bp.route('/like', methods=['POST', 'GET'])
    def like():
        # TODO train nn to like this user
        n = get_next_user()
        return jsonify(get_extra_information_from_login(n))

    @bp.route('/dislike', methods=['POST', 'GET'])
    def dislike():
        # TODO train nn to dislike this user
        n = get_next_user()
        return jsonify(get_extra_information_from_login(n))

    def get_extra_information_from_login(login):
        repos = requests.get('https://api.github.com/users/'+login+'/repos?client_id='+os.environ.get('CLIENT_ID')+'&client_secret='+os.environ.get('CLIENT_SECRET')).json()
        languages = []
        for repo in repos:
            languages.append(repo['language'])
        languages = list(set(languages))
        if None in languages:
            languages.remove(None)
        user = requests.get('https://api.github.com/users/'+login+'?client_id='+os.environ.get('CLIENT_ID')+'&client_secret='+os.environ.get('CLIENT_SECRET')).json()
        user['languages'] = languages
        return user

    def get_next_user():
        user = client.copenhacks.users.find_one()
        client.copenhacks.users.update({}, {'$push': {'choosed': user['actual']}})
        user = client.copenhacks.users.find_one()

        fol = requests.get('https://api.github.com/users/'+user['actual']+'/followers?client_id='+os.environ.get('CLIENT_ID')+'&client_secret='+os.environ.get('CLIENT_SECRET')).json()
        followers = []
        for f in fol:
            if f['login'] != user['actual'] and f['login'] not in user['choosed']:
                followers.append(f['login'])
        omega = list(set(user['omega'] + followers))

        for u in omega:
            # TODO ask to the nn if its valid or not
            valid = bool(random.getrandbits(1))
            if valid:
                pass
            else:
                omega.remove(u)

        if user['actual'] in omega:
            omega.remove(user['actual'])

        client.copenhacks.users.update({}, {'$set': {'omega': omega}})

        if len(omega) > 0:
            client.copenhacks.users.update({}, {'$set': {'actual': omega[0]}})
            return omega[0]
        else:
            return None

    return bp
