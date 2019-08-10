from flask import Flask, render_template, request, escape
from vsearch import search4letters
from DBcm import UseDatabase

app = Flask(__name__)

app.my_config['dbconfig'] = "dbname=log user=postgres host=localhost password=1"


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
def view_the_log() -> 'html':
    contents = []
    with UseDatabase(app.config['dbconfig']) as cursor:
        __SQL = "SELECT * FROM log;"
        cursor.execute(__SQL)
        contents = cursor.fetchall()
        titles = ('Form Data', 'Remote_addr', 'User_agent', 'Results')
        return render_template('viewlog.html',
                               the_title='View Log',
                               the_row_titles=titles,
                               the_data=contents,)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',
                           the_title='Welcome to search4letters on the web!')


if __name__ == '__main__':
    app.run(debug=True)
