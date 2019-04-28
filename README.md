# flask_server_experiments

Install python-flask before using any of these:
```
sudo apt install python-flask python3-flask
```

Current projects:
1) http_gallery --- Simple gallery for webm and mp4 videos.

2) tls12_gallery --- Gallery w/ TLS1.2 encryption.

3) tls12_gallery_auth --- Gallery w/ TLS1.2 encryption, custom working directory and password.

4) tls12_gallery_accounts --- Gallery w/ TLS1.2 encryption, custom working directory, accounts + passwords and logging.

Add a user:
```
$ printf "USERNAME:$(echo -n 'PASSWORD' | sha1sum | head -c 40)\n" >> access.txt
```

5) tls12_flask_DL_only_server --- A general purpose server with TLS1.2 and no indexing.

6) tls12_flask_upload_server --- A file upload server with indexing:

![alt text](https://raw.githubusercontent.com/ran-sama/flask_server_experiments/master/preview.png)

Add a cleanup routine on files older than 24 hours:
```
@hourly find /media/kingdian/up/* -mtime 1 -type f -not -name 'index.html' -delete
```

## What does the gallery look like?

![alt text](https://raw.githubusercontent.com/ran-sama/flask_server_experiments/master/gallery_example.png)

## License
Licensed under the WTFPL license.
