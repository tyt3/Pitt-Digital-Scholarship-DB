"""Module for creating Flask App"""
from flask import Flask, render_template, request
#from views import views
#from auth import auth

app = Flask(__name__)

"""Set routes/endpoints"""
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        pass

    if request.method == 'POST':
        pass

    return render_template("index.html", title=
                           "Pitt Digital Scholarship Database")

if __name__ == "__main__":
    app.run(debug=True)
