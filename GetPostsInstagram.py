import json
import os
from flask import Flask, Response, request
import instaloader
import itertools
from dotenv import load_dotenv
from instaloader import ConnectionException

load_dotenv()

app = Flask(__name__)
context_loader = instaloader.Instaloader()

username = os.getenv('INSTA_USERNAME')
password = os.getenv('INSTA_PASSWORD')
context_loader.login(username, password)


@app.route('/')
def get_start():
    data = {
        'Welcome': 'Welcome To API Posts Instagram'
    }
    return Response(json.dumps(data), mimetype="application/json")


@app.route('/favicon.ico')
def favicon():
    return '', 204


@app.route('/<name_profile>', methods=['GET'])
def get_posts(name_profile):
    start_post = request.args.get('start', default=0, type=int)
    close_post = request.args.get('close', default=4, type=int)

    try:
        profile = instaloader.Profile.from_username(context_loader.context, name_profile)
        posts = []

        for post in itertools.islice(profile.get_posts(), start_post, close_post):
            posts.append({'caption': f'{post.caption}', 'url': f'{post.url}', 'title': f'{post.title}'})
        return Response(json.dumps(posts), mimetype='application/json')
    except instaloader.exceptions.ProfileNotExistsException:
        error_post = {
            'status': 404,
            'message': 'Perfil no encontrado.'
        }
        return Response(json.dumps(error_post), mimetype='application/json')
    except instaloader.exceptions.LoginRequiredException:
        error_post = {
            'status': 403,
            'message': 'Se requiere autenticación para acceder a este perfil.'
        }
        return Response(json.dumps(error_post), mimetype='application/json')
    except Exception as e:
        error_post = {
            'status': 500,
            'message': str(e)
        }
        return Response(json.dumps(error_post), mimetype='application/json')


if __name__ == '__main__':
    port = int(os.environ.get('PORT',5000))
    app.run(debug=False, host='0.0.0.0', port=port)
