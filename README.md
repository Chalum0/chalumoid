# This is the code for the [chalumoid](chalumoid.fr) website

## File structure :

In this python webserver, files are stored in special places to be used by Flask.

HTML files are stored in the "templates" file. Style files and script files are stored
in the "static" file. Images are also stored there. Databases and json files are saved in the
"files\server-files" file.

## Running the project :

### Dependencies :
To run the project, you need python 3.9 or more. You also need to install the following modules
using pip:
- flask
- flask-cors
- sqlite3

```pip install flask flask-cors sqlit3```

### Running the project :
To run the project, you need to run ```main-flask.py```. for that, you can simply execute it on windows or run
```python main-flask.py``` in a command prompt in the directory of the file. On linux, you must execute the following
command on a command prompt ```sudo python3 main-flask.py```.