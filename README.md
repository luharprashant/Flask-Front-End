# Flask front end for process the uploaded video by the user

# Packages required
`flask`, `flask_login`, `flask_wtf`, `flask-sqlalchemy`, `flask-crypt`


# To get the server up and running :
1) For Linux:<br/>
   `$ export FLASK_APP=flask_blog.py`<br/>
   `$ flask run`<br/>
   For Windows:<br/>
   `> $env:FLASK_APP = "flask_blog.py"`<br/>
   `> flask run`<br/>
2) `$ python run.py`

# To generate database
1) Go to python shell
2) `>>> from flask_blog import db`
3) `>>> db.create_all()`

# To process the video
In flask_blog/routes.py use process_video() for actual processing of video after uploading.
