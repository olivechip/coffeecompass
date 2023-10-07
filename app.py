from flask import Flask, render_template, flash, redirect, request, jsonify, session, g
from forms import UserAddForm, UserLoginForm
from models import db, connect_db, User, Coffeeshop, UserCoffeeshopStatus
import requests

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config["SECRET_KEY"] = 'its_a_secret'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///capstone2"

connect_db(app)
app.app_context().push()

db.create_all()

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = UserAddForm()

    if form.validate_on_submit():
        if not User.validate_username(form.username.data):
            flash("Username already taken.")
            return render_template('signup.html', form=form)
        else: 
            user = User.signup(
                    username=form.username.data,
                    password=form.password.data,
                    image_url=form.image_url.data or User.image_url.default.arg
                    )
            db.session.commit()
            do_login(user)
            return redirect('/')
    else:
        return render_template('signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = UserLoginForm()

    if form.validate_on_submit():
        if not User.authenticate(form.username.data, form.password.data):
            flash("Invalid credentials.")
            return render_template('login.html', form=form)
        else:
            flash("Successfully logged in.")
            user = User.query.filter_by(username=form.username.data).first()
            do_login(user)
            return redirect("/")
    else:
        return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    do_logout()
    flash('Successfully logged out.')
    return redirect('/')

@app.route('/search', methods=['GET'])
def search():
    location = request.args['search']
        
    api_key = "mIBPAqjUPzr0uCAvGVzm_nKPM4CwLKNIcjQ9YffWdaVxlGAV9kWXO1vZIxGLaSMrMAPf4yeMkDu4PagJs2VUChzEC-PWqyi9UXM7LoGVxE_tfwqrbqjjt_22agfpZHYx"
    headers = {"Authorization": f"Bearer {api_key}"}
    url = f"https://api.yelp.com/v3/businesses/search?term=coffee&location={location}&limit=12"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        businesses = data.get('businesses', [])
        print(businesses)
        for b in businesses:
            if not Coffeeshop.query.filter(Coffeeshop.yelp_id == b["id"]):
                Coffeeshop.add_to_db(
                name=b["name"], 
                yelp_id=b["id"], 
                address=b["location"]["display_address"]
                )
                db.session.commit()
        return render_template('results.html', businesses=businesses)
    else:
        print("Error:", response.status_code)
        return render_template('error_404.html')

    return render_template('index.html')

@app.route('/users/<user_id>')
def view_user(user_id):
    user = User.query.get_or_404(user_id)
    coffeeshops = UserCoffeeshopStatus.query.filter(User.id == UserCoffeeshopStatus.user_id).all()
    print(coffeeshops)
    return render_template('user.html', user=user, coffeeshops=coffeeshops)

@app.route('/add_to_favorite/<yelp>', methods=['POST'])
def add_to_fav(yelp):
    if not g.user:
        flash("You must have an account to do this.")
        return redirect('/')
        
    coffeeshop = Coffeeshop.query.filter_by(yelp_id = yelp).first()

    uc_status = UserCoffeeshopStatus(user_id=g.user.id, coffeeshop_id=coffeeshop.id, status='favorite')
    db.session.add(uc_status)
    db.session.commit()

