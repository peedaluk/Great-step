from flask import render_template

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/sample')
def sample():
    return render_template('sample.html')

@app.route('/tmes')
def tmes():
    return render_template('tmes.html')

@app.route('/great-step/events')
def events():
    return render_template('events.html')

@app.route('/great-step/events/competitions')
def competitions():
    return render_template('competitions.html')

@app.route('/great-step/events/workshops')
def workshops():
    return render_template('workshops.html')

@app.route('/great-step/events/panel-discussion')
def panel_discussion():
    return render_template('panel_discussion.html')

@app.route('/aboutus')
def about():
    return render_template('about.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/resetPassword')
def reset_password():
    return render_template('reset_password.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/great-step/events/competitions/QS')
def quiz_spiel():
    return render_template('quiz_spiel.html')

@app.route('/great-step/events/competitions/Enviro_CS')
def enviro_cs():
    return render_template('enviro_cs.html')

@app.route('/great-step/events/competitions/Petro_CS')
def petro_cs():
    return render_template('petro_cs.html')

@app.route('/great-step/events/competitions/Mine_CS')
def mine_cs():
    return render_template('mine_cs.html')

@app.route('/great-step/events/competitions/Safety_DA')
def safety_da():
    return render_template('safety_da.html')

@app.route('/great-step/events/competitions/Geobotics')
def geobotics():
    return render_template('geobotics.html')

@app.route('/great-step/events/competitions/Pitch_Perfect')
def pitch_perfect():
    return render_template('pitch_perfect.html')

@app.route('/great-step/events/competitions/code_ext')
def code_ext():
    return render_template('code_ext.html')

@app.route('/great-step/events/competitions/Mine_A_Thon')
def mine_a_thon():
    return render_template('mine_a_thon.html')

@app.route('/great-step/events/competitions/gth')
def gth():
    return render_template('gth.html')

@app.route('/great-step/events/competitions/MS')
def mine_shot():
    return render_template('mine_shot.html')

@app.route('/great-step/events/competitions/quiz')
def publi_quiz():
    return render_template('publi_quiz.html')

@app.route('/great-step/events/competitions/Indu_Design')
def indu_design():
    return render_template('indu_design.html')

@app.route('/great-step/events/competitions/Mineac')
def mineac():
    return render_template('mineac.html')

@app.route('/great-step/events/competitions/<comp_id>')
def competition(comp_id):
    return render_template('competition.html', comp_id=comp_id)

# Add more routes as needed
