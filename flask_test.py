from flask import Flask, render_template, url_for

app = Flask(__name__)



@app.route('/match/<int:match_id>')
def index(match_id):
    return render_template('match.html') 


if __name__ == "__main__":
    app.run(debug=True)