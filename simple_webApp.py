from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'YouWillNeverGuessMySecretKey'


@app.route('/login')
def do_logon() -> str:
    session['logged_in'] = True
    return 'You are now logged in'


@app.route('/logout')
def do_logout()-> str:
    session.pop('logged_in')
    return 'You are now logged out'


@app.route('/status')
def check_status() -> str:
    if 'logged_in' in session:
        return 'You are currently logged in'
    return 'You are NOT logged in'


if __name__ == '__main__':
    app.run(debug=True)