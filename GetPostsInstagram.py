import json
import os
from flask import Flask, Response, request
import instaloader
import itertools

from instaloader import ConnectionException

app = Flask(__name__)


context_loader = instaloader.Instaloader()


@app.route('/')
def get_start():
    data = {
        'Welcome': 'Welcome To API Posts Instagram'
    }
    return Response(json.dumps(data), mimetype="application/json")


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
    except ConnectionException:
        error_post = {
            'status': 404,
            'message': 'Not Found when accessing profile'
        }
        return Response(json.dumps(error_post), mimetype='application/json')


if __name__ == '__main__':
    port = int(os.environ.get('PORT',5000))
    app.run(debug=True, host='0.0.0.0', port=port)
