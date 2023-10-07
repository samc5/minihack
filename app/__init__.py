from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")       
def hello_world():
    """Return base page. Mostly so it doesn't crash"""
    return render_template('math.html')

if __name__ == "__main__":  # true if this file NOT imported
    app.debug = True        # enable auto-reload upon code change
    app.run()               # launch Flask