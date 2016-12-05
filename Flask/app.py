import flask
import logging
import json
import pprint

from feedbackAnalyser import analyse
from recommender.recommend import *

from flask import request, session, url_for, redirect

app = flask.Flask("__main__")
# TODO Use a secure way to set this
app.secret_key = 'aijdfAJKFJq234kjkdfsa]adfsdfasadfjjq4rjjJHJHjhakgj'

with open('recommender/tech_list.json') as fp:
    tech_list = json.load(fp)
tech_list = [str(tech) for tech in tech_list]


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
    session['culminatingExp'] = request.form['CulminatingExp']

    logInfo()
    return redirect(url_for('form2'))


@app.route('/form2validation', methods=['POST'])
def form2validation():
    preReqs = getPreReqs(session['department'])
    session['preReqs'] = []
    for preReq in preReqs:
        if request.form.get(preReq['id'], 0):
            session['preReqs'].append(preReq)
    logInfo()
    return redirect(url_for('form3'))


@app.route('/form3validation', methods=['POST'])
def form3validation():
    global tech_list
    techLiking = []
    for tech in tech_list:
        if bool(request.form.get(tech, False)):
            techLiking.append(tech)
    session['techLiking'] = techLiking
    logInfo()
    return redirect(url_for('courseSuggetion'))


@app.route('/feedbackvalidation', methods=['POST'])
def feedbackvalidation():
    feedback = {}
    feedback['course'] = request.form.get('course', None)
    feedback['tagid'] = request.form.get('tagid', None)
    feedback['book'] = request.form.get('book', None)
    feedback['review'] = request.form.get('review', None)
    feedback['level'] = request.form.get('level', None)
    feedback['grades'] = request.form.get('grades', None)
    feedback['professor'] = request.form.get('professor', None)
    logInfo(feedback)

    # TODO run on a separate thread
    analyse(feedback)
    return flask.render_template('thankyou.html')


@app.route('/form1')
def form1():
    # TODO get data from a DB for the from
    # Have hard coded it for now, since we have limited data
    return flask.render_template('form1.html')


@app.route('/form2')
def form2():
    # TODO use template inheritance to avoid duplicaiton of code
    return flask.render_template('form2.html',
                                 preReqs=getPreReqs(session['department']))


@app.route('/form3')
def form3():
    # TODO use template inheritance to avoid duplicaiton of code
    global tech_list
    return flask.render_template('form3.html', entries=tech_list)


@app.route('/courseSuggetion')
def courseSuggetion():
    something = {}
    something['techLiking'] = session['techLiking']
    something['preReqs'] = session['preReqs']
    something['coreSubjects'] = recommendCoreSubjects(session['department'],
                                                      session['techLiking'])
    something['culmExpCourses'] = getCulmExpCourses(session['department'],
                                                    session['culminatingExp'])
    something['majorSubjects'] = recommendMajorSubjets(session['major'],
                                                       session['techLiking'])
    something['minorSubjects'] = [recommendMinorSubjet(session['major'],
                                                       session['techLiking'])
                                  ]
    something['electives'] = recommendElectives(session['techLiking'], count=3,
                                                exp=something['coreSubjects'] +
                                                something['culmExpCourses'] +
                                                something['majorSubjects'] +
                                                something['minorSubjects'])
    # return courses
    # return flask.render_template('courseSuggetion.html')
    logging.debug(pprint.pformat(something))
    return "work in progress"


@app.route('/feedback')
def feedback():
    # TODO get courses from DB
    courses = ["cmpe273", "cmpe202", "cmpe272", "cmpe281", "cmpe283"]
    # TODO get proffersors from DB
    professors = ["Prof A", "Prof B", "Prof C", "Prof D"]
    return flask.render_template('feedback.html',
                                 courses=courses,
                                 professors=professors)


@app.route('/')
def landingPage():
    return flask.render_template('landingPage.html')

@app.route('/about')
def about():
    # TODO get data from a DB for the from
    # Have hard coded it for now, since we are have limited data
    return flask.render_template('about.html')

@app.route('/forms')
def plan():
    # TODO get data from a DB for the from
    # Have hard coded it for now, since we are have limited data
    sampleCourses = [['CMPE202','CMPE272','CMPE273'],
                     ['CMPE281','CMPE275','CMPE239'],
		     ['CMPE287','CMPE295','CMPE294'],
		     ['CMPE283','CMPE297','CMPE226']
                    ]
    return flask.render_template('forms.html', courses=sampleCourses)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(host="0.0.0.0", debug=True, port=5992, threaded=True)
