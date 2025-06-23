# main.py
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = '''
<!doctype html>
<title>Password Checker</title>
<h2>Password Strength Checker</h2>
<form method="POST">
  <input type="text" name="password" placeholder="Enter your password" required>
  <input type="submit" value="Check Strength">
</form>
{% if result %}
  <h3>{{ result }}</h3>
{% endif %}
'''

def password_strength(password):
    n = len(password)
    d = {'lower': False, 'upper': False, 'num': False, 'symb': False}
    for i in password:
        if 96 < ord(i) < 123:
            d['lower'] = True
        elif 64 < ord(i) < 91:
            d['upper'] = True
        elif 47 < ord(i) < 58:
            d['num'] = True
        else:
            d['symb'] = True

    time = 0
    if d['lower']:
        time += (26 ** n) / 1e9
    if d['upper']:
        time += (26 ** n) / 1e9
    if d['num']:
        time += (10 ** n) / 1e9
    if d['symb']:
        time += (33 ** n) / 1e9

    return convert_seconds(time)

def convert_seconds(seconds):
    if seconds < 60:
        return f"Your password is very weak, it takes {seconds:.2f} seconds to crack."
    elif seconds < 3600:
        return f"Your password is weak, it takes {seconds / 60:.2f} minutes to crack."
    elif seconds < 86400:
        return f"Your password is good, it takes {seconds / 3600:.2f} hours to crack."
    elif seconds < 31536000:
        return f"Your password is hard, it takes {seconds / 86400:.2f} days to crack."
    else:
        return f"Your password is very hard, it takes {seconds / 31536000:.2f} years to crack."

@app.route("/", methods=["GET", "POST"])
def check_password():
    result = None
    if request.method == "POST":
        password = request.form["password"]
        result = password_strength(password)
    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  
    app.run(host="0.0.0.0", port=port, ssl_context=('certificate.pem', 'private.pem'))