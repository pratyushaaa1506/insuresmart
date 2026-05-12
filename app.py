from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

import joblib

app = Flask(__name__)

# ---------------- APP CONFIG ---------------- #

app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)

# ---------------- LOGIN MANAGER ---------------- #

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ---------------- USER MODEL ---------------- #

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(100), unique=True)

    password = db.Column(db.String(300))

# ---------------- LOAD USER ---------------- #

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))

# ---------------- LOAD ML MODEL ---------------- #

model = joblib.load('model.pkl')

# ---------------- LOGIN PAGE ---------------- #

@app.route('/', methods=['GET', 'POST'])

def login():

    if request.method == 'POST':

        email = request.form['email']

        password = request.form['password']

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            return redirect(url_for('dashboard'))

    return render_template('login.html')

# ---------------- REGISTER PAGE ---------------- #

@app.route('/register', methods=['GET', 'POST'])

def register():

    if request.method == 'POST':

        email = request.form['email']

        password = request.form['password']

        hashed_password = generate_password_hash(password)

        new_user = User(
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)

        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

# ---------------- DASHBOARD ---------------- #

@app.route('/dashboard')

@login_required

def dashboard():

    return render_template('dashboard.html')

# ---------------- INSURANCE PLANS PAGE ---------------- #

@app.route('/plans')

@login_required

def plans():

    insurance_plans = [

        {
            "name": "Star Health Young Star",
            "price": "₹12,000",
            "coverage": "₹5 Lakhs",
            "rating": "4.5",
            "logo": "https://upload.wikimedia.org/wikipedia/commons/8/8f/Star_Health_Logo.png",
            "website": "https://www.starhealth.in"
        },

        {
            "name": "ACKO Platinum Health",
            "price": "₹10,000",
            "coverage": "₹5 Lakhs",
            "rating": "4.4",
            "logo": "https://upload.wikimedia.org/wikipedia/commons/5/58/Acko_Logo.png",
            "website": "https://www.acko.com"
        },

        {
            "name": "Care Supreme",
            "price": "₹15,000",
            "coverage": "₹10 Lakhs",
            "rating": "4.7",
            "logo": "https://www.careinsurance.com/images/care_logo.svg",
            "website": "https://www.careinsurance.com"
        },

        {
            "name": "HDFC Ergo Optima",
            "price": "₹22,000",
            "coverage": "₹20 Lakhs",
            "rating": "4.8",
            "logo": "https://www.hdfcergo.com/images/logo.svg",
            "website": "https://www.hdfcergo.com"
        }

    ]

    return render_template(
        'plans.html',
        plans=insurance_plans
    )

# ---------------- PROFILE PAGE ---------------- #

@app.route('/profile')

@login_required

def profile():

    return render_template(
        'profile.html',
        user=current_user
    )
#analytics
@app.route('/analytics')

@login_required

def analytics():

    return render_template('analytics.html')
# ---------------- PREDICTION ---------------- #

@app.route('/predict', methods=['POST'])

@login_required

def predict():

    age = int(request.form['age'])

    height = float(request.form['height'])

    weight = float(request.form['weight'])

    children = int(request.form['children'])

    disease = int(request.form['disease'])

    state = int(request.form['state'])

    coverage = request.form['coverage']

    # ---------------- BMI CALCULATION ---------------- #

    bmi = weight / ((height / 100) ** 2)

    # ---------------- PREMIUM CALCULATION ---------------- #

    base_price = 5000

    # AGE FACTOR
    age_risk = age * 200

    # BMI FACTOR
    bmi_risk = 0

    if bmi > 25:
        bmi_risk = 3000

    # DISEASE FACTOR
    disease_risk = 0

    if disease != 0:
        disease_risk = 5000

    # CHILDREN FACTOR
    children_risk = children * 2000

    # STATE FACTOR
    state_risk = state * 1000

    # COVERAGE FACTOR
    coverage_risk = 0

    if coverage == "₹10 Lakhs":
        coverage_risk = 4000

    elif coverage == "₹25 Lakhs":
        coverage_risk = 8000

    # FINAL PREMIUM

    prediction = (
        base_price
        + age_risk
        + bmi_risk
        + disease_risk
        + children_risk
        + state_risk
        + coverage_risk
    )

    # ---------------- INSURANCE PLANS ---------------- #

    plans = [

        # ---------------- NORMAL PLANS ---------------- #

        {
            "name": "ACKO Basic Health",
            "type": "normal",
            "price": 8000,
            "coverage": "₹3 Lakhs",
            "rating": "4.2",
            "website": "https://www.acko.com"
        },

        {
            "name": "Star Health Family Optima",
            "type": "normal",
            "price": 10000,
            "coverage": "₹5 Lakhs",
            "rating": "4.4",
            "website": "https://www.starhealth.in"
        },

        {
            "name": "Care Freedom",
            "type": "normal",
            "price": 12000,
            "coverage": "₹5 Lakhs",
            "rating": "4.5",
            "website": "https://www.careinsurance.com"
        },

        {
            "name": "Niva Bupa Health Companion",
            "type": "normal",
            "price": 14000,
            "coverage": "₹5 Lakhs",
            "rating": "4.6",
            "website": "https://www.nivabupa.com"
        },

        {
            "name": "HDFC Ergo Optima Secure",
            "type": "normal",
            "price": 18000,
            "coverage": "₹10 Lakhs",
            "rating": "4.7",
            "website": "https://www.hdfcergo.com"
        },

        {
            "name": "ICICI Lombard Complete Health",
            "type": "normal",
            "price": 20000,
            "coverage": "₹10 Lakhs",
            "rating": "4.6",
            "website": "https://www.icicilombard.com"
        },

        {
            "name": "ManipalCigna ProHealth",
            "type": "normal",
            "price": 22000,
            "coverage": "₹15 Lakhs",
            "rating": "4.5",
            "website": "https://www.manipalcigna.com"
        },

        {
            "name": "Bajaj Allianz Health Guard",
            "type": "normal",
            "price": 24000,
            "coverage": "₹15 Lakhs",
            "rating": "4.5",
            "website": "https://www.bajajallianz.com"
        },

        {
            "name": "Aditya Birla Activ Health",
            "type": "normal",
            "price": 28000,
            "coverage": "₹20 Lakhs",
            "rating": "4.7",
            "website": "https://www.adityabirlacapital.com"
        },

        {
            "name": "Tata AIG MediCare Premier",
            "type": "normal",
            "price": 32000,
            "coverage": "₹25 Lakhs",
            "rating": "4.8",
            "website": "https://www.tataaig.com"
        },

        {
            "name": "Max Bupa ReAssure Plus",
            "type": "normal",
            "price": 36000,
            "coverage": "₹30 Lakhs",
            "rating": "4.8",
            "website": "https://www.nivabupa.com"
        },

        {
            "name": "Reliance Health Infinity",
            "type": "normal",
            "price": 40000,
            "coverage": "₹50 Lakhs",
            "rating": "4.6",
            "website": "https://www.reliancegeneral.co.in"
        },

        # ---------------- SENIOR CITIZEN PLANS ---------------- #

        {
            "name": "Star Health Senior Citizen Red Carpet",
            "type": "senior",
            "price": 45000,
            "coverage": "₹10 Lakhs",
            "rating": "4.4",
            "website": "https://www.starhealth.in"
        },

        {
            "name": "Care Senior Health Advantage",
            "type": "senior",
            "price": 50000,
            "coverage": "₹15 Lakhs",
            "rating": "4.5",
            "website": "https://www.careinsurance.com"
        },

        {
            "name": "HDFC Ergo Critical Illness",
            "type": "senior",
            "price": 60000,
            "coverage": "₹50 Lakhs",
            "rating": "4.8",
            "website": "https://www.hdfcergo.com"
        }

    ]

    # ---------------- RECOMMENDATION ENGINE ---------------- #

    recommended = []

    for plan in plans:

        if abs(plan["price"] - prediction) <= 15000:

            recommended.append(plan)

    # ---------------- RESULT PAGE ---------------- #

    return render_template(
        'result.html',
        prediction=prediction,
        recommendations=recommended,

        base_price=base_price,
        age_risk=age_risk,
        bmi_risk=bmi_risk,
        disease_risk=disease_risk,
        children_risk=children_risk,
        state_risk=state_risk,
        coverage_risk=coverage_risk
    )

# ---------------- LOGOUT ---------------- #

@app.route('/logout')

@login_required

def logout():

    logout_user()

    return redirect(url_for('login'))

# ---------------- MAIN ---------------- #

if __name__ == '__main__':

    with app.app_context():

        db.create_all()

    app.run(debug=True)