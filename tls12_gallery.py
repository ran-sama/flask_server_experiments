import ssl, os
from flask import Flask, request, render_template, send_from_directory

sslcontext = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
sslcontext.options |= ssl.OP_NO_TLSv1
sslcontext.options |= ssl.OP_NO_TLSv1_1
sslcontext.protocol = ssl.PROTOCOL_TLSv1_2
sslcontext.set_ciphers("ECDHE-ECDSA-AES256-GCM-SHA384 ECDHE-ECDSA-CHACHA20-POLY1305")
sslcontext.set_ecdh_curve("secp384r1")
sslcontext.load_cert_chain("/home/pi/keys/fullchain.pem", "/home/pi/keys/privkey.pem")

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
#app = Flask(__name__, static_url_path=None, static_folder='/media/kingdian/')

@app.route('/thumbnails/<filename>')
def send_image(filename):
    return send_from_directory("thumbnails", filename)

@app.route('/videos/<filename>')
def send_video(filename):
    return send_from_directory("videos", filename)

@app.route('/gallery')
def get_gallery():
    image_names = os.listdir('./thumbnails')
    image_names = [os.path.splitext(x)[0] for x in image_names]
    with open("blacklist.txt", 'r') as f:
        blacklist = f.readlines()
        blacklist = [x.strip() for x in blacklist]
        blacklist = [i.split('.', 1)[0] for i in blacklist]
    image_names = sorted(list(set(image_names) - set(blacklist)))
    return render_template("gallery.html", image_names=image_names)

@app.route('/player/<filename>')
def get_videos(filename):
    video_names = filename
    return render_template("player.html", video_names=video_names)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8443, ssl_context=sslcontext, threaded=True, debug=False)
