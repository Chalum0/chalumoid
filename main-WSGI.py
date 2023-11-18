from wsgiref.simple_server import make_server
from flask import Flask, render_template

def web_app(environment, response):
    status = "200 OK"
    headers = [("content-type", "text/html; charset=utf-8")]
    response(status, headers)
    return [render_template("index.html").encode("UTF-8")]


with make_server("", 5000, web_app) as server:
    print(
        "serving on port 5000...\nvisit http://127.0.0.1:5000\nTo exit press ctrl + c"
    )
    server.serve_forever()
