from flask import Flask, render_template, request, redirect, flash
import contextlib

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

app = Flask(__name__)
app.secret_key = '9595299039'
def make_tiny(url):
    request_url = ('http://tinyurl.com/api-create.php?' + 
    urlencode({'url':url}))
    try:
        with contextlib.closing(urlopen(request_url)) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            flash('Please enter a URL', 'error')
        else:
            tiny_url = make_tiny(url)
            if tiny_url:
                flash(f'Shortened URL: {tiny_url}', 'success')
            else:
                flash('Invalid URL or API error', 'error')
        return redirect('/')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)