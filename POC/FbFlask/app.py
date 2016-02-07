from flask import Flask, redirect, url_for, session, request
from flask_oauth import OAuth
import logging
from logging.handlers import RotatingFileHandler
import urllib2
from flask import Flask
import requests


SECRET_KEY = 'development key'
DEBUG = True
FACEBOOK_APP_ID = '1718539425078474'
FACEBOOK_APP_SECRET = 'b59c25703907472c97b76d8b4f157754'


app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email, user_photos, read_custom_friendlists' }
)

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@app.route('/friends')
def friends():

    userID = 10208654415267951
    token = 'CAAYbAKP23MoBAEZCZCfYVYsC1mXjSoIFSBtTKDEw0ztos3DEdGUzhqL8duRQ4jt1gSrkbaQCmaPe907LwD2g1SUBK1HAR43ekgIeUW9o7WfAnOuA1YI4NDMF3UT0LYgmk5hforb7LnXGOjMlShPvl9IqUXvAHln0MpnbahzWNWVQUvBzPX82QPipWZBugFKuayE8C61ama8AkqwmXzv'
    url = 'https://graph.facebook.com/v2.5/'+ str(userID) + "/friendlists?access_token="+token
    # 10208654415267951/friendlists?access_token=CAAYbAKP23MoBAEZCZCfYVYsC1mXjSoIFSBtTKDEw0ztos3DEdGUzhqL8duRQ4jt1gSrkbaQCmaPe907LwD2g1SUBK1HAR43ekgIeUW9o7WfAnOuA1YI4NDMF3UT0LYgmk5hforb7LnXGOjMlShPvl9IqUXvAHln0MpnbahzWNWVQUvBzPX82QPipWZBugFKuayE8C61ama8AkqwmXzv
    response = requests.get(url, data=[])
    app.logger.info(response.text)

    return response.text


@app.route('/pics')
def pics():

    userID = 10208654415267951
    token = 'CAAYbAKP23MoBAEZCZCfYVYsC1mXjSoIFSBtTKDEw0ztos3DEdGUzhqL8duRQ4jt1gSrkbaQCmaPe907LwD2g1SUBK1HAR43ekgIeUW9o7WfAnOuA1YI4NDMF3UT0LYgmk5hforb7LnXGOjMlShPvl9IqUXvAHln0MpnbahzWNWVQUvBzPX82QPipWZBugFKuayE8C61ama8AkqwmXzv'
    url = 'https://graph.facebook.com/v2.5/'+ str(userID) + "/photos?access_token="+token
    # 10208654415267951/friendlists?access_token=CAAYbAKP23MoBAEZCZCfYVYsC1mXjSoIFSBtTKDEw0ztos3DEdGUzhqL8duRQ4jt1gSrkbaQCmaPe907LwD2g1SUBK1HAR43ekgIeUW9o7WfAnOuA1YI4NDMF3UT0LYgmk5hforb7LnXGOjMlShPvl9IqUXvAHln0MpnbahzWNWVQUvBzPX82QPipWZBugFKuayE8C61ama8AkqwmXzv
    response = requests.get(url, data=[])
    app.logger.info(response.text)

    return response.text


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    app.logger.info(me)

    url = '/v2.5/' + me.data['id'] + '/photos'

    app.logger.info(url)
    app.logger.info(resp['access_token'])
    # facebook.request(path=url)

    app.logger.info(me.data['id'])
    # app.logger.info(facebook.request(path='/v2.5/10208654415267951/photos'))

    # r = requests.get('http://www.github.com')


    # "https://graph.facebook.com/oauth/access_token_info?client_id=" + FACEBOOK_APP_ID + "&access_token=" + session['oauth_token']

    access_token = session['oauth_token']
    app.logger.info(access_token)
    r = requests.get("https://graph.facebook.com//v2.5/10208654415267951/photos")
    url = "https://graph.facebook.com/oauth/access_token_info?client_id=" + FACEBOOK_APP_ID + "&access_token=" + access_token[0]
    # data = {"access_token": session['oauth_token']}
    response = requests.get(url, data=[])
    app.logger.info(response.text)


    url = "https://graph.facebook.com/v2.5/" + me.data['id'] + "/friendlists"
    data = {"access_token": session['oauth_token']}
    response = requests.get(url, data=data)
    app.logger.info(response.text)

    return 'Logged in as id=%s name=%s access_token=%s' % \
        (me.data['id'], me.data['name'], session['oauth_token'])



@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


if __name__ == '__main__':
    port = 8080
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(port=port)
