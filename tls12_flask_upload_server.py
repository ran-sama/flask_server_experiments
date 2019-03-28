import os, ssl, secrets
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename

UPLOAD_FOLDER = '/media/kingdian/up/'

certfile = "/home/ubuntu/keys/fullchain.pem"
keyfile = "/home/ubuntu/keys/privkey.pem"
ecdh_curve = "secp384r1"
cipherlist = "ECDHE-ECDSA-AES256-GCM-SHA384 ECDHE-ECDSA-CHACHA20-POLY1305"

sslcontext = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
sslcontext.options |= ssl.OP_NO_TLSv1
sslcontext.options |= ssl.OP_NO_TLSv1_1
sslcontext.protocol = ssl.PROTOCOL_TLSv1_2
sslcontext.set_ciphers(cipherlist)
sslcontext.set_ecdh_curve(ecdh_curve)
sslcontext.load_cert_chain(certfile, keyfile)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        my_data = request.files.getlist('file')
        my_pass = request.form['password']
        if my_data and my_pass == 'SUPERSECRET123':
            for file in my_data:
                my_handler(file)
            return redirect(url_for('index'))
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file multiple name=file>
         <input type="password" name="password" value="">
         <input type=submit value=Upload>
    </form>
    <p><br>https://mysecretserver.noip.me/%s</p>
    """ % "<br>https://mysecretserver.noip.me/up/".join(sorted(filter(os.path.isfile, os.listdir('.')), key=os.path.getmtime, reverse=True))
#    """ % "<br>https://mysecretserver.noip.me/".join(sorted(os.listdir(app.config['UPLOAD_FOLDER'],)))

def my_handler(f):
    filename = secure_filename(f.filename)
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], secrets.token_hex(4) + "." + filename.rsplit('.',1)[1]))
#    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, ssl_context=sslcontext, threaded=True, debug=False)
