from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import pandas as pd
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_url = StringField('Location Url', validators=[DataRequired(), URL()])
    opening_time = StringField('Open Time', validators=[DataRequired()])
    closing_time = StringField('Closing Time', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', choices=[(x+1)*"☕" for x in range(5)], validators=[DataRequired()])
    wifi_rating = SelectField('Wifi Strength Rating', choices=[(x+1)*"💪" for x in range(5)], validators=[DataRequired()])
    power_rating = SelectField('Power Socket Availability', choices=[(x+1)*"🔌" for x in range(5)], validators=[DataRequired()])
    submit = SubmitField('Submit')

def get_table():
    with open('cafe-data.csv', newline='', encoding='utf8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        df = pd.read_csv('cafe-data.csv')
        html_raw = df.to_html()
        with open('./templates/table.html', 'w', encoding='utf8') as write_data:
            write_data.write(html_raw)
        with open('./templates/table.html', 'r', encoding='utf8') as read_data:
            lines = read_data.readlines()
        with open('./templates/table.html', 'w', encoding='utf8') as write_data:
            for number, line in enumerate(lines):
                if number != 0:
                    write_data.write(line)


def update_table(update):
    with open('./templates/table.html', 'a', encoding='utf8') as append_data:
        append_data.write(update)


# Exercise: ##DONE##
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        update_table(f"{form.cafe.data},{form.location_url.data},{form.opening_time.data},{form.closing_time.data},{form.coffee_rating.data},{form.wifi_rating.data},{form.power_rating.data},\n")
        cafes()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    get_table()
    return render_template('cafes.html',)


if __name__ == '__main__':
    app.run(debug=True)
