import sys
import os

sys.path.insert(1, os.path.join(os.path.abspath('.'),  'venv/lib/python2.7/site-packages'))

from flask import Flask, render_template
from flask_jsglue import JSGlue

app = Flask(__name__, static_url_path = "", static_folder = "static")
jsglue = JSGlue(app)

@app.route("/")
def hello():
    return render_template('home.html')

@app.route("/userhome")
def userhome():
    cats = ["https://www.petfinder.com/wp-content/uploads/2012/11/140272627-grooming-needs-senior-cat-632x475.jpg","https://upload.wikimedia.org/wikipedia/commons/4/4d/Cat_March_2010-1.jpg","https://i.ytimg.com/vi/tntOCGkgt98/maxresdefault.jpg","http://catsrusrescue.org/wp-content/uploads/2013/03/cat2.jpg","https://www.petfinder.com/wp-content/uploads/2012/11/99059361-choose-cat-litter-632x475.jpg","https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQuPLnnp9jeUNhGVayXbnxyvE6GRUmvya5ytySi0tIGCjLzIVV3dA","http://cdn.playbuzz.com/cdn/8841f68c-493a-4a2a-8830-524e75cf9cbe/e2a9f148-1b3c-41d1-9149-3487ac3c057b.jpg","http://petsittersoflasvegas.com/wp-content/uploads/2015/01/o-CATS-KILL-BILLIONS-facebook.jpg"]
    catslist = ','.join(cats)
    return render_template('userhome.html', mylist = catslist)


if __name__ == "__main__":
    app.run()