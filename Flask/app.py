import flask
import logging

from flask import request, session, url_for, redirect

app = flask.Flask("__main__")
# TODO Use a secure way to set this
app.secret_key = 'aijdfAJKFJq234kjkdfsa]adfsdfasadfjjq4rjjJHJHjhakgj'


@app.route('/formTest')
def formTest():
    return flask.render_template('formTest.html')


def logInfo(val=session):
    logging.debug("-" * 40)
    for key in val:
        logging.debug("%s: %s" % (key, val[key]))
    logging.debug("-" * 40)


@app.route('/form1validation', methods=['POST'])
def form1validation():
    # TODO don't trust user input, check if we can make this more secure
    # TODO use a iterator
    # TOOD maintain config details separately
    session['department'] = request.form['department']
    session['major'] = request.form['major']
    session['minor'] = request.form['minor']
    session['gradYear'] = request.form['gradYear']
    session['CulminatingExp'] = request.form['CulminatingExp']

    logInfo()
    return redirect(url_for('form2'))


@app.route('/form2validation', methods=['POST'])
def form2validation():
    # TODO don't trust user input, check if we can make this more secure
    # TODO use a iterator
    # TOOD maintain config details separately
    session['OS'] = request.form.get('OS', 0)
    session['DS'] = request.form.get('DS', 0)
    session['OOPS'] = request.form.get('OOPS', 0)
    logInfo()
    return redirect(url_for('form3'))


@app.route('/form3validation', methods=['POST'])
def form3validation():
    # TODO don't trust user input, check if we can make this more secure
    # TODO use a iterator
    # TOOD maintain config details separately
    session['a'] = request.form.get('a', 0)
    session['b'] = request.form.get('b', 0)
    session['c'] = request.form.get('c', 0)
    session['d'] = request.form.get('d', 0)
    session['e'] = request.form.get('e', 0)
    session['f'] = request.form.get('f', 0)
    session['g'] = request.form.get('g', 0)
    logInfo()
    return redirect(url_for('courseSuggetion'))


@app.route('/feedbackvalidation', methods=['POST'])
def feedbackvalidation():
    # TODO don't trust user input, check if we can make this more secure
    # TODO use a iterator
    # TOOD maintain config details separately
    feedback = {}
    feedback['courses'] = request.form['courses']
    feedback['tagid'] = request.form['tagid']
    feedback['book'] = request.form['book']
    feedback['review'] = request.form['review']
    feedback['level'] = request.form['level']
    feedback['grades'] = request.form['grades']
    logInfo(feedback)
    return flask.render_template('thankyou.html')


@app.route('/form1')
def form1():
    # TODO get data from a DB for the from
    # Have hard coded it for now, since we are have limited data
    return flask.render_template('form1.html')


@app.route('/form2')
def form2():
    # TODO use template inheritance to avoid duplicaiton of code
    return flask.render_template('form2.html')


@app.route('/form3')
def form3():
    # TODO use template inheritance to avoid duplicaiton of code

    # TODO get interests from DB
    entries = [{'name': 'a'},
               {'name': 'b'},
               {'name': 'c'},
               {'name': 'd'},
               {'name': 'e'},
               {'name': 'f'},
               {'name': 'g'}]
    return flask.render_template('form3.html', entries=entries)


@app.route('/courseSuggetion')
def courseSuggetion():
    return "TODO"
    # return flask.render_template('courseSuggetion.html')


@app.route('/feedback')
def feedback():
    return flask.render_template('feedback.html')


@app.route('/')
def landingPage():
    return flask.render_template('landingPage.html')


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(host="0.0.0.0", debug=True, port=5992)
