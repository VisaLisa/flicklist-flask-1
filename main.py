from flask import Flask, request, redirect

import cgi

app = Flask(__name__)

page_header = """

<!DOCTYPE html>
<html>
    <head>
        <title>FlickList</title>
    </head>
    <body>
        <h1>Flicklist</h1>
"""
page_footer = """
    </body>
</html>
"""

add_form = """
    <form action="/add" method="POST">
        <label for="new-movie">I want to add
        <input type="text" id="new-movie" name="new-movie">
        to my watchlist.
        </label>
        <input type="submit" value="Belly" >
    </form>
"""

current_movies = [
    "Star Wars",
    "My Favorite Martian",
    "The Avengers",
    "The Hitchhikder's Guide To The Galaxy"
]
def get_current_movies():
    crossoff_options = ''
    for movie in current_movies:
        crossoff_options += '<option value="{0}">{0}</option>'.format(movie)
    return current_movies

crossoff_options = ''
for movie in get_current_movies():
    crossoff_options += '<option value="{0}">{0}</option>'.format(movie)

crossoff_form = """
    <form action="/crossoff" method="POST">
        <label>
            I want to cross off
            <select name="crossed-off-movie"/>
                {0}
            </select>
        </label>
        <input type="submit" value="Cross It Off"/>

    </form>
""".format(crossoff_options)

@app.route("/crossoff", methods=['POST'])
def crossoff_movie():
    crossed_off_movie = request.form['crossed-off-movie']

    # Don't allow movies not in the list
    if crossed_off_movie not in get_current_movies():
        error_msg = "'{0}' is not in the watchlist. Have a nice day!".format(crossed_off_movie)
        return redirect('/?error={0}'.format(error_msg))

    crossed_off_movie_element = "<strike>" + crossed_off_movie + "</strike>"
    confirmation = crossed_off_movie_element + " has been crossed off your WatchList."
    content = page_header + "<p>" + confirmation + "</p>" + page_footer

    return content


@app.route('/add', methods=['POST'])
def add_movie():
    new_movie = request.form['new-movie']
    if type(new_movie) is not str or new_movie == '':
        error_msg = "'{0}' is not in a valid movie. Check IMDB".format(new_movie)
        return redirect('/?error={0}'.format(error_msg))

    # build response content
    new_movie_element = "<strong>" + cgi.escape(new_movie) + "</strong>"
    sentence = new_movie_element + " has been added to the watchlist"
    content = page_header + "<p>" + sentence + "</p>" + page_footer

    return content

@app.route("/")
def index():
    edit_header = '<h2>Edit My WatchList</h2>'

    error = request.args.get('error')
    if error:
        esc_error = cgi.escape(error, quote=True)
        error_element = '<p class="error">{0}</p>'.format(esc_error)
    else:
        error_element = ''

    # build the response string
    content = page_header + edit_header + error_element + add_form + crossoff_form + page_footer
    #content = page_header + edit_header + error_element + add_form  + crossoff_form + page_footer
    return content


app.run(debug=True)
