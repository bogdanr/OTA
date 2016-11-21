
# Import the Flask Framework, firebase and the local forms script which has WTforms
import pyrebase
from flask import Flask, request, render_template
from forms import FirePut
from streamfw import *

app = Flask(__name__)
app.secret_key = 's3cr3t'

config = {
  "apiKey": "apiKey",
  "authDomain": "projectId.firebaseapp.com",
  "databaseURL": "https://ota-rocks.firebaseio.com",
  "storageBucket": "ota-rocks.appspot.com"
}

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/testing')
def testing():
    return "This is a testing page"

@app.route('/firmware', methods=['GET', 'POST'])
def fwstuff():
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    if request.headers.get('User-Agent') != 'ESP8266-http-Update':
      form = FirePut()
      if form.validate_on_submit():
        putData = {'FWname' : form.fwname.data, 'Comment' : form.comment.data}
        db.child('devices').child(form.macaddr.data).set(putData)
        return render_template('api-put-result.html', form=form, putData=putData)
      return render_template('add-device.html', form=form)
    else:
      import time
      patchData = {'FW-current' : request.headers.get('x-ESP8266-version'), 'Comment' : 'added automagically', 'Last seen' : time.strftime("%c")}
      resp = db.child('devices').child(request.headers['x-ESP8266-STA-MAC']).update(patchData)
      FWupdate = db.child('devices').child(request.headers['x-ESP8266-STA-MAC']).child('FW-update').get()
      if FWupdate.val() and resp.get('FW-current', 'none') != FWupdate.val():
        return get_stream_fw(FWupdate)
      return Response(status=304)


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

