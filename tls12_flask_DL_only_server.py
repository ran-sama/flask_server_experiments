import ssl, os
from flask import Flask, request, redirect, url_for, send_from_directory, Response

sslcontext = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
sslcontext.options |= ssl.OP_NO_TLSv1
sslcontext.options |= ssl.OP_NO_TLSv1_1
sslcontext.protocol = ssl.PROTOCOL_TLSv1_2
sslcontext.set_ciphers("ECDHE-ECDSA-AES256-GCM-SHA384 ECDHE-ECDSA-CHACHA20-POLY1305")
sslcontext.set_ecdh_curve("secp384r1")
sslcontext.load_cert_chain("/home/pi/keys/fullchain.pem", "/home/pi/keys/privkey.pem")

app = Flask(__name__, static_url_path=None, static_folder='/media/kingdian/')

@app.route('/')
def root():
    response = app.send_static_file('index.html')
    response.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubdomains; preload'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'no-referrer'
    return response

@app.route('/<path:path>')
def catch_all(path):
    if os.path.isdir("/media/kingdian/" + path) == True:#os.path.isfile("/media/kingdian/" + path)
        response_dir = app.send_static_file(path + 'index.html')
        response_dir.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubdomains; preload'
        response_dir.headers['Content-Security-Policy'] = "default-src 'self'"
        response_dir.headers['X-Content-Type-Options'] = 'nosniff'
        response_dir.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response_dir.headers['X-XSS-Protection'] = '1; mode=block'
        response_dir.headers['Referrer-Policy'] = 'no-referrer'
        return response_dir
    response_file = app.send_static_file(path)
    response_file.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubdomains; preload'
    response_file.headers['Content-Security-Policy'] = "default-src 'self'"
    response_file.headers['X-Content-Type-Options'] = 'nosniff'
    response_file.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response_file.headers['X-XSS-Protection'] = '1; mode=block'
    response_file.headers['Referrer-Policy'] = 'no-referrer'
    return response_file

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=443, ssl_context=sslcontext, threaded=True, debug=False)
