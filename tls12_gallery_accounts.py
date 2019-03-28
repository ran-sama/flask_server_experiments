import ssl, os, hashlib, datetime
from flask import Flask, request, render_template, send_from_directory

sslcontext = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
sslcontext.options |= ssl.OP_NO_TLSv1
sslcontext.options |= ssl.OP_NO_TLSv1_1
sslcontext.protocol = ssl.PROTOCOL_TLSv1_2
sslcontext.set_ciphers("ECDHE-ECDSA-AES256-GCM-SHA384 ECDHE-ECDSA-CHACHA20-POLY1305")
sslcontext.set_ecdh_curve("secp384r1")
sslcontext.load_cert_chain("/home/pi/keys/fullchain.pem", "/home/pi/keys/privkey.pem")

WORK_DIR = '/media/kingdian/'
app = Flask(__name__)
app.root_path = os.path.dirname(WORK_DIR)

@app.route('/thumbnails/<filename>')
def send_image(filename):
    return send_from_directory("thumbnails", filename)

@app.route('/videos/<filename>')
def send_video(filename):
    return send_from_directory("videos", filename)

@app.route('/gallery', methods=['GET', 'POST'])
def get_gallery():
    if request.method == 'POST':
        my_login = request.form['login']
        my_pass = request.form['password']
        account = my_login + ":" + hashlib.sha1(my_pass.encode('utf-8')).hexdigest()
        with open("access.txt", 'r') as f1:
            for line in f1:
                if line.rstrip() == account:
                    with open('access.log', 'a') as log:
                        log.write(datetime.datetime.utcnow().isoformat() + \
                        " - " + request.remote_addr + " - " + my_login + "\n")
                    image_names = os.listdir(WORK_DIR + './videos')
                    image_names = [os.path.splitext(x)[0] for x in image_names]
                    with open("blacklist.txt", 'r') as f2:
                        blacklist = f2.readlines()
                        blacklist = [x.strip() for x in blacklist]
                        blacklist = [i.split('.', 1)[0] for i in blacklist]
                    image_names = sorted(list(set(image_names) - set(blacklist)))
                    return render_template("gallery.html", image_names=image_names)
    return """<!doctype html><title>Authentication required</title>
    <body bgcolor=#666666><center><h2>Authentication required</h2>
    <div style="text-align: center;">
    <div style="display: inline-block; text-align: left;">
    <form action="" method=post enctype=multipart/form-data>
    <label for="gallery_user">Username</label><br>
    <input type="text" name="login" value=""><br>
    <label for="gallery_pass">Password</label><br>
    <input type="password" name="password" value=""><p>
    <input type=submit value="Login">
    </div></div></form></center></body>"""

@app.route('/player/<filename>')
def get_videos(filename):
    video_names = filename
    return render_template("player.html", video_names=video_names)

if __name__ == "__main__":
    print(app.root_path)
    app.run(host='0.0.0.0', port=8443, ssl_context=sslcontext, threaded=True, debug=False)
