
# Import the Flask Framework, firebase and the local forms script which has WTforms
from firebase import firebase
from flask import Flask, request, render_template
from forms import FirePut
from streamfw import *

app = Flask(__name__)
app.secret_key = 's3cr3t'
firebase = firebase.FirebaseApplication('https://onecom-1.firebaseio.com', None)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/testing')
def testing():
    return "<h1>This is another testing page</h1>"

@app.route('/firmware', methods=['GET', 'POST'])
def fwstuff():
    if request.headers['User-Agent'] != "ESP8266-http-Update":
      form = FirePut()
      if form.validate_on_submit():
        putData = {'FWname' : form.fwname.data, 'Comment' : form.comment.data}
        firebase.put('/devices', form.macaddr.data, putData)
        return render_template('api-put-result.html', form=form, putData=putData)
      return render_template('add-device.html', form=form)
    else:
      import time
      patchData = {'FW-current' : request.headers.get('x-ESP8266-version'), 'Comment' : 'added automagically', 'Last seen' : time.strftime("%c")}
#     We are using patch instead of put because it doesn't delete data that we are not sending. Still, we need to make sure we don't send a key with a Null value.
      resp = firebase.patch('/devices/' + request.headers['x-ESP8266-STA-MAC'], patchData)
      FWupdate = firebase.get('/devices/' + request.headers['x-ESP8266-STA-MAC'], 'FW-update')
      if FWupdate and resp.get('FW-current', 'none') != FWupdate:
        return get_stream_fw(FWupdate)
      return request.headers['x-ESP8266-STA-MAC'] + "\n" 


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500


# We need this to be able to execute the webserver localy
if __name__ == '__main__':
    app.run(debug=True)

