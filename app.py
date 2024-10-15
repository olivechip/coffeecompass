from flask import Flask, render_template, flash, redirect, request, jsonify, session, g
from forms import UserAddForm, UserLoginForm
from models import db, connect_db, User, Coffeeshop, UserCoffeeshopStatus
from dotenv import load_dotenv
import requests
import os
import subprocess

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL')

connect_db(app)
app.app_context().push()

CURR_USER_KEY = "curr_user"

# Render specific for database creation/seeding
# def run_seed_file():
#     """Runs the seed.py file to populate the database."""
#     try:
#         subprocess.run(['python', 'seed.py'], check=True)
#         print("Database seeded successfully!")
#     except subprocess.CalledProcessError as e:
#         print(f"Error seeding database: {e}")

# run_seed_file()  
# End 

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    user_id = session.get(CURR_USER_KEY)
    print(user_id)
    if user_id is not None:
        g.user = User.query.get(user_id)
        print(g.user)
        if g.user is None:
            print(f"No user found with ID: {user_id}") 
            do_logout() 
    else:
        g.user = None

def do_login(user):
    """Log in user."""
    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user."""
    session.pop(CURR_USER_KEY, None)

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

    api_key = os.getenv('YELP_API_KEY')
    headers = {"Authorization": f"Bearer {api_key}"}
    url = f"https://api.yelp.com/v3/businesses/search?term=coffee&location={location}&limit=12"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        businesses = data.get('businesses', [])

        for b in businesses:
            Coffeeshop.add_to_db(
                yelp_id=b["id"],
                name=b["name"],
                display_address=" ".join(b["location"]["display_address"]),
                display_phone=b.get("display_phone"),
                rating=b.get("rating"),
                review_count=b.get("review_count"),
                img_url=b.get("image_url")
            )
        
        return render_template('results.html', businesses=businesses, location=location)
    else:
        print("Error:", response.status_code)
        return render_template('404.html')

@app.route('/users/<username>')
def view_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    coffeeshops = UserCoffeeshopStatus.query.filter_by(user_id=user.id).all()
    coffeeshop_list = [Coffeeshop.query.get(coffeeshop.coffeeshop_id) for coffeeshop in coffeeshops]

    print(coffeeshop_list)
    return render_template('profile.html', user=user, coffeeshops=coffeeshop_list)


@app.route('/add_to_favorite/<yelp>', methods=['POST'])
def add_to_fav(yelp):
    if not g.user:
        flash("You must have an account to do this.")
        return redirect(request.referrer or '/')

    coffeeshop = Coffeeshop.query.filter_by(yelp_id=yelp).first()
    
    if not coffeeshop:
        flash("Coffeeshop not found.")
        return redirect(request.referrer or '/')
    
    existing_status = UserCoffeeshopStatus.query.filter_by(user_id=g.user.id, coffeeshop_id=coffeeshop.id).first()
    
    if existing_status:
        flash("This coffeeshop is already in your favorites.")
        return redirect(request.referrer or '/')
    
    uc_status = UserCoffeeshopStatus(user_id=g.user.id, coffeeshop_id=coffeeshop.id, status='favorite')
    
    db.session.add(uc_status)
    db.session.commit()
    
    flash("Coffeeshop added to favorites!")
    return redirect(request.referrer or '/')

@app.route('/remove_from_favorite/<yelp>', methods=['POST'])
def remove_from_fav(yelp):
    """Remove a coffeeshop from the user's favorites."""

    if not g.user:
        flash("You must have an account to do this.")
        return redirect(request.referrer or '/')

    coffeeshop = Coffeeshop.query.filter_by(yelp_id=yelp).first()
    if not coffeeshop:
        flash("Coffeeshop not found.")
        return redirect(request.referrer or '/')

    existing_status = UserCoffeeshopStatus.query.filter_by(
        user_id=g.user.id, coffeeshop_id=coffeeshop.id, status='favorite'
    ).first()

    if not existing_status:
        flash("This coffeeshop is not in your favorites.")
        return redirect(request.referrer or '/')

    db.session.delete(existing_status)
    db.session.commit()

    flash("Coffeeshop removed from favorites!")
    return redirect(request.referrer or '/')