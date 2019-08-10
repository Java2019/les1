from flask import Flask, render_template, request, escape, session
from vsearch import search4letters
from DBcm import UseDatabase
from checker import check_logged_in
from DBcm import ConnectionError

app = Flask(__name__)

app.config['dbconfig'] = "dbname=log user=postgres host=localhost password=1"
app.secret_key = 'my_secret_key'

def log_request(req: 'flask_request', res: str) -> None:
    with UseDatabase(app.config['dbconfig']) as cursor:
        __SQL = "CREATE TABLE if not exists log (id serial PRIMARY KEY, " \
                "phrase text, letters text, ip text, browser_string text, results text);"
        cursor.execute(__SQL)
        __SQL = "INSERT INTO log (phrase, letters, ip, browser_string, results) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(__SQL, (req.form['phrase'],
                               req.form['letters'],
                               req.remote_addr,
                               req.user_agent.string,
                               res, ))


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = str(search4letters(phrase, letters))
    log_request(request, results)
    return render_template('results.html',
                           the_title=title,
                           the_phrase=phrase,
                           the_letters=letters,
                           the_results=results,)


@app.route('/viewlog')
@check_logged_in
def view_the_log() -> 'html':
    contents = []
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            __SQL = "SELECT * FROM log;"
            cursor.execute(__SQL)
            contents = cursor.fetchall()
            titles = ('Form Data', 'Remote_addr', 'User_agent', 'Results')
            return render_template('viewlog.html',
                                   the_title='View Log',
                                   the_row_titles=titles,
                                   the_data=contents,)
    except ConnectionError as err:
        print('Is your database switched on? Error:', str(err))
    except Exception as err:
        print('Something went wrong:', str(err))
    return 'Error'


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',
                           the_title='Welcome to search4letters on the web!')

@app.route('/login')
def do_logon() -> str:
    session['logged_in'] = True
    return 'You are now logged in'


@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')
    return 'You are now logged out'


@app.route('/status')
def check_status() -> str:
    if 'logged_in' in session:
        return 'You are currently logged in'
    return 'You are NOT logged in'


if __name__ == '__main__':
    app.run(debug=True)
