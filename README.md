### Purpose

This flask app provides a lightweight api for the easyborrow queue-based controller to query and update the easyborrow database.

### Notes

- This app assumes a project structure like:

        some_enclosing_directory
            ezb_dbprx
                config  # directory
                proxy_app.py
            env_ezb_dbprx


- This app ssumes an entry in our existing apache .conf file like:

        <Directory /path/to/ezb_dbprx>
          Order allow,deny
          Allow from all
        </Directory>
        WSGIScriptAlias /path/to/ezb_dbprx/config/wsgi.py

---
