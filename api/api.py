import time
from flask import Flask, request
#from flask_restful import Api, resource
from wikimap import Wikimap

app = Flask(__name__)
wikimap = Wikimap("../../data.sqlite/data.sqlite")


@app.route('/path', methods=['GET'])
#handle get request for path between two ID's
def path():
    src_id = int(request.args.get('src-id'))
    dest_id = int(request.args.get('dest-id'))
    path = wikimap.determine_path(src_id, dest_id)
    #path = wikimap.determine_path(316, 101398)

    #path = [src_id, 22222, 33333, 44444, 55555, 66666, dest_id]
    #path = wikimap.test_func()

    return { 'path': path }
    #return (src_id, dest_id)
 
@app.route('/title', methods=['GET'])
#handle get request for page given page title
def title():
    title = request.args.get('title')
    page = wikimap.get_page(title)
    #page = (50000, title)
    return { 'page': page }

if __name__ == "__main__":
    app.run(debug=True)
