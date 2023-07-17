from __future__ import absolute_import

from flask import Flask, request, render_template
from static import app as static_app

app = Flask(__name__)
app.register_blueprint(static_app)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        return render_template('index.html', user_input=user_input+'です')
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
