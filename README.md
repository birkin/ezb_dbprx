### Purpose

Test project...

Experiment: this flask app would create a lightweight api to a database.

This would allow another experimental project to run queries and updates more generically than being tied to direct db calls.


### Notes

- This app assumes a project structure like:

        some_enclosing_directory/
            ezb_dbprx/
                config/
                proxy_app.py
            env_ezb_dbprx/


- This app ssumes an entry in our existing apache .conf file like:

        <Directory /path/to/ezb_dbprx>
          Order allow,deny
          Allow from all
        </Directory>
        WSGIScriptAlias /path/to/ezb_dbprx/config/wsgi.py

---
