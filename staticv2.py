from flask import Flask, render_template, request, jsonify,session,redirect,url_for,flash

from graphviz import Digraph
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import pandas as pd
from openai import OpenAI
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

current_directory = os.path.dirname(os.path.abspath(__file__))
#print("current_directory", current_directory)

# SECTION 1 - EXCEL IMPORT FOR FIRST TAB
app = Flask(__name__)
app.secret_key = 'KEY'






@app.route('/upload', methods=['GET', 'POST'])
def upload_file():


     # Check if user is logged in
    if 'username' not in session:
        # User is not logged in, render a template with a warning message
        flash("Please log in to access this feature.")
        return redirect(url_for('home'))

    else:
        if request.method == 'POST':
            try:
                file = request.files['file']
                if 'username' in session:
                    username = session.get('username')
                    print("username", username)
                else:
                    username = ""

                if file:
                    df = pd.read_excel(file)
                    col1_list = df.iloc[:, 0].tolist()  # create list from first column
                    col2_list = df.iloc[:, 1].tolist()  # create list from second column
                    col3_list = df.iloc[:, 2].fillna('').apply(lambda x: x.split(',') if isinstance(x, str) else []).tolist()
                    col3_list1 = [','.join(sublist) for sublist in col3_list]
                    ##print(col1_list)
                    ##print(col2_list)
                    ##print(col3_list1)


                    activities = {}
                    duration = {}
                    successors = {}

                                # Add 'Start' node with no successors
                    for name, dur, successor in zip(col1_list, col2_list, col3_list1):
                        successor_set = set(successor.split(',')) if successor else set()
                        if not successor_set:
                            successor_set = {'End'}
                        activities[name] = successor_set
                        duration[name] = int(dur)
                        successors[name] = successor_set
                    # ##print("orj", activities)
                    # Set 'End' node with no successors and zero duration
                    activities['End'] = set()
                    duration['End'] = '0'
                    activities['Start'] = set()
                    duration['Start'] = '0'

                    # Get activities that do not exist in the successors list
                    activities_not_in_successors = set(activities.keys()) - set.union(*successors.values())

                    # Remove 'Start' from the activities_not_in_successors set
                    activities_not_in_successors.discard('Start')

                    # Set activities_not_in_successors as successors of 'Start' and add them to the activities dictionary
                    activities['Start'] = activities_not_in_successors
                    successors['Start'] = activities_not_in_successors
                    # duration['Start'] = 0

                    ##print("Activities not in successors list:", activities_not_in_successors)




                    for name in duration.keys():
                        duration[name] = int(duration[name])


                        for name in duration.keys():
                            duration[name] = int(duration[name])





                    ##print(duration)
                    ##print(activities)

                    # Extract the numbers from the dictionary using dictionary comprehension
                    anumbers = [value for value in duration.values() if isinstance(value, int)]
                    numbers=anumbers[:-2]
                    ##print('numbers',numbers)

                    activities_html = activities.copy()
                    if 'End' in activities_html:
                        del activities_html['End']
                    if 'Start' in activities_html:
                        del activities_html['Start']


                    keys_list = list(activities_html.keys())
                    values_list = [set(v) for v in activities_html.values()]
                    values_list2=[s if s != {'End'} else '' for s in values_list]
                    values_list2=[s if s != {' '} else '' for s in values_list]
                    values_list3 = [','.join(s) if s else '' for s in values_list2]
                    values_list3 = [s.replace("'", "").replace("{", "").replace("}", "") for s in values_list3]
                    values_list3=[s.replace('End', "") for s in values_list3]
                    # ##print the two lists
                    ##print("Keys list:", keys_list)
                    # ##print("Values list:", values_list2)
                    ##print("Values list2:", values_list3)

                    rows = []

                    print("rows", rows)
                    for num, key, value in zip(numbers, keys_list, values_list3):
                        #print("value", value)
                        row = {'activity': key, 'duration': num, 'successor': value}
                        rows.append(row)




                    message = "File uploaded successfully! Please click on calculate"
                    return render_template('index.html', message=message,rows=rows,username=username)


                else:
                    message = """The selected file could not be read.
                                Please upload a valid file."""
                    return render_template('index3.html', message=message)
            except Exception as e:
                message = f"An error occurred: {str(e)}. Please upload a valid file "
                return render_template('index3.html', message=message)
        else:
            message = "Please upload an excel file ."
            return render_template('index3.html', message=message)


# Configure Flask-Mail to use Gmail
app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'okul05419561@hotmail.com'  # Use environment variables instead
app.config['MAIL_PASSWORD'] = 'ugur8487'  # Use environment variables instead
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)


# Example using Flask-SQLAlchemy




app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# New Feedback model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feedback_text = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Optional: Add a foreign key to link feedback to a user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('feedbacks', lazy=True))

    def __repr__(self):
        return f'<Feedback {self.id}>'

# Create tables
with app.app_context():
    db.create_all()


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()  # Use this method to get JSON data
    print(data)

    if not data:
        return jsonify(success=False, error="No data received"), 400

    # Now you can use the data as a regular dictionary
    username = data.get('newUsername')
    email = data.get('email')
    password = data.get('newPassword')  # Make sure to handle passwords securely

    print(username, email, password)  # Inspect the values

    # Check if user already exists
    user = User.query.filter_by(username=username).first()
    if user:
        print("var")
        return jsonify(success=False, error="Username already taken"), 409



    # Create new user and set password
    new_user = User(username=username, email=email)
    new_user.set_password(password)

    # Add new user to the database
    db.session.add(new_user)
    db.session.commit()

    # Send a welcome email
    # Make sure the Mail instance is configured and the server is running
    try:
        msg = Message('Welcome to CPM (AON) Generator',
                      sender='okul05419561@hotmail.com',
                      recipients=[email])
        msg.body = f'Thank you for signing up, {username}!'
        mail.send(msg)
        return jsonify(success=True)
    except Exception as e:
        print(e)
        return jsonify(success=False, error=str(e)), 500


@app.route('/delete_user', methods=['GET'])
def delete_user():
    # Find the user in the database
    username = session.get('username')
    user = User.query.filter_by(username=username).first()

    # If the user is not found, return an error
    if not user:
        return jsonify(success=False, error="User not found"), 404

    # Delete the user from the database
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('logout')) # Redirect to the home page or login page


@app.route('/login', methods=['POST'])
def login():

    if not request.is_json:
        return jsonify(success=False, error="Missing JSON in request"), 400

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Input validation (basic example)
    if not username or not password:
        return jsonify(success=False, error="Username and password are required"), 400


    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        # Login successful
        session['user_id'] = user.id
        session['username'] = user.username # Store the user's ID in the session
        return jsonify(success=True, username=user.username )
    else:
        # Login failed
        return jsonify(success=False, error="Invalid username or password"), 401

@app.route('/admin/users')
def list_users():
    users = User.query.all()  # Get all users from the database
    return render_template('admin_users.html', users=users)

@app.route('/logout')
def logout():
    # Remove 'user_id' and 'username' from session
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('home')) # Redirect to the home page or login page


# SECTION 2 - FIRST TAB'S CODES
@app.route('/', methods=['GET', 'POST'])
def home():
    try:
            # Define the default inputs
        activities = {

            'A': {'B', 'C'},
            'B': {'D'},
            'C': {'F', 'E'},
            'D': {'G'},
            'E': {'G'},
            'F': {'H'},
            'G': {'H'},
            'H': {'End'},
            'End': {},
            'Start': {'A'},
            }
        duration = {

            'A': 3,
            'B': 4,
            'C': 12,
            'D': 5,
            'E': 1,
            'F': 2,
            'G': 4,
            'H': 6,
            'End': 0,
            'Start': 0,
            }



        if request.method == 'POST':
            activities = {}
            duration = {}
            successors = {}
            activity_names = request.form.getlist('activity')

            activity_durations = request.form.getlist('duration')

            activity_successors = request.form.getlist('successor')


            #print("activity_names",activity_names)
            #print("activity_durations",activity_durations)
            #print("activity_successors",activity_successors)

            # Add 'Start' node with no successors
            for name, dur, successor in zip(activity_names, activity_durations, activity_successors):
                successor_set = set(successor.split(',')) if successor else set()
                if not successor_set:
                    successor_set = {'End'}
                activities[name] = successor_set
                duration[name] = int(dur)
                successors[name] = successor_set
            # #print("orj", activities)
            # Set 'End' node with no successors and zero duration
            activities['End'] = set()
            duration['End'] = '0'
            activities['Start'] = set()
            duration['Start'] = '0'

            # Get activities that do not exist in the successors list
            activities_not_in_successors = set(activities.keys()) - set.union(*successors.values())

            # Remove 'Start' from the activities_not_in_successors set
            activities_not_in_successors.discard('Start')

            # Set activities_not_in_successors as successors of 'Start' and add them to the activities dictionary
            activities['Start'] = activities_not_in_successors
            successors['Start'] = activities_not_in_successors
            # duration['Start'] = 0

            #print("Activities not in successors list:", activities_not_in_successors)
            print("activity_names", activity_names)
            print("activity_durations", activity_durations)
            print("activity_successors", activity_successors)




        for name in duration.keys():
            duration[name] = int(duration[name])


            for name in duration.keys():
                duration[name] = int(duration[name])





        # print(duration)
        # print(activities)

        # Extract the numbers from the dictionary using dictionary comprehension
        anumbers = [value for value in duration.values() if isinstance(value, int)]
        numbers=anumbers[:-2]
        #print('numbers',numbers)

        activities_html = activities.copy()
        if 'End' in activities_html:
            del activities_html['End']
        if 'Start' in activities_html:
            del activities_html['Start']


        keys_list = list(activities_html.keys())
        values_list = [set(v) for v in activities_html.values()]
        values_list2=[s if s != {'End'} else '' for s in values_list]
        values_list2=[s if s != {' '} else '' for s in values_list]
        values_list3 = [','.join(s) if s else '' for s in values_list2]
        values_list3 = [s.replace("'", "").replace("{", "").replace("}", "") for s in values_list3]
        values_list3=[s.replace('End', "") for s in values_list3]
        # #print the two lists
        print("Keys list:", keys_list)
        print("Values list:", values_list2)
        print("Values list2:", values_list3)


        if 'numbers1' in session and 'keys_list1' in session and 'activity_successors1' in session:
            numbers=session['numbers1']
            keys_list=session['keys_list1']
            values_list3=session['activity_successors1']
            del session['numbers1']
            del session['keys_list1']
            del session['activity_successors1']
        else:
            session['numbers'] = numbers
            session['keys_list'] = keys_list
            session['activity_successors'] = values_list3


        rows = []
        # print("rows", rows)
        for num, key, value in zip(numbers, keys_list, values_list3):
            #print("value", value)
            row = {'activity': key, 'duration': num, 'successor': value}
            rows.append(row)

        print("rows", rows)




        # Calculate earliest start, earliest finish, latest start, and latest finish times
        es = {k: 0 for k in activities}
        ef = {k: duration[k] for k in activities}

        for k, v in activities.items():
            for dep in v:
                es[dep] = max(es[dep], ef[k])
                ef[dep] = es[dep] + duration[dep]

        lf = {k: ef['End'] for k in activities}
        ls = {k: lf[k] - duration[k] for k in activities}

        for k in reversed(list(activities.keys())):
            for dep in activities[k]:
                lf[k] = min(lf[k], ls[dep])
            ls[k] = lf[k] - duration[k]



        ls['End'] = es['End']
        lf['End'] = ef['End']

        ls['Start'] = es['Start']
        lf['Start']= ef['Start']

        # Find critical path
        critical_path = []
        for k, v in activities.items():
            if ef[k] == lf[k]:
                critical_path.append(k)

        #print("deneme")
        #print(ls)
        #print(ef)
        #print(duration)
        # Create graph
        dot = Digraph(graph_attr={'rankdir': 'LR','labelloc': 't'})

        # Set the title of the graph
        dot.attr(label="CPM Diagram", fontsize='15')

        #print("activities",activities)

        for k, v in activities.items():
            label = f"{k}\n{duration[k]}\n{es[k]}/{ef[k]}\n{ls[k]}/{lf[k]}"
            dot.node(k, label=label, shape='rectangle')
            if k in critical_path:
                dot.node(k, style='filled', color='tomato')

        for k, v in activities.items():
            for dep in v:
                dot.edge(k, dep)


        # Render the graph to a file
        dot.render(os.path.join(current_directory, 'static', 'test'), format='png', cleanup=True)


        # GANTT CHART


        # Create list of activities and their start and end times
        activities_list = [(k, es[k], ef[k]) for k in activities]
        #print(activities_list)

        activities_list = [activity for activity in activities_list if activity[0] not in ['Start', 'End']]

        # Sort activities by their earliest start time
        activities_list.sort(key=lambda x: x[1])



        # Create figure and axis objects
        fig, ax = plt.subplots()

        # Set y-axis limits
        ax.set_ylim(0, len(activities_list))

        # Sort activities by their earliest start time and reverse the order
        activities_list.sort(key=lambda x: x[1], reverse=True)

        # Set y-axis ticks and labels
        ax.set_yticks(range(len(activities_list)))
        ax.set_yticklabels([x[0] for x in activities_list])

        # Set x-axis limits
        ax.set_xlim(0, max(lf.values()))

        # Set x-axis label
        ax.set_xlabel('Time')


        print("activities_list",activities_list)

        # Plot horizontal bars for each activity
        for i, (activity, start, end) in enumerate(activities_list):
            duration = end - start
            ax.broken_barh([(start, duration)], (i, 0.5), facecolors='blue')

        ax.set_title("Gantt Chart")

            # Save the Gantt chart as a PNG file
        fig.savefig(os.path.join(current_directory, 'static', 'gantt.png'))

        if 'username' in session:
            username = session.get('username')
        else:
            username = ""

        # session.pop('activity_names', None)  # Removes 'activity_names' if it exists, does nothing if it doesn't
        # session.pop('activity_durations', None)  # Same for 'activity_durations'
        # session.pop('activity_successors', None)  # And 'activity_successors'



        # # Display the Gantt chart as an image
        # Image(filename='gantt.png')
        return render_template('index.html',rows=rows,username=username)

    except Exception as e:
        message = f"An error occurred: {str(e)}. Please check your inputs."
        return render_template('index.html', rows=rows,message=message,username=username)


# SECTION 3 - EXCEL IMPORT FOR SECOND TAB
@app.route('/uploadsc', methods=['GET', 'POST'])
def upload_file_sc():
    if request.method == 'POST':
        try:
            # num = request.form.__getitem__('num')
            file = request.files['file']
            if file:
                df = pd.read_excel(file)
                col1_list = df.iloc[:, 0].tolist()  # create list from first column
                col2_list = df.iloc[:, 1].tolist()  # create list from second column
                col3_list = df.iloc[:, 2].fillna('').apply(lambda x: x.split(',') if isinstance(x, str) else []).tolist()
                col3_list1 = [','.join(sublist) for sublist in col3_list]
                col4_list = df.iloc[:, 3].tolist()  # create list from first column
                col5_list = df.iloc[:, 4].tolist()  # create list from second column
                col6_list = df.iloc[:, 5].tolist()  # create list from second column
                ##print(col1_list)
                ##print(col2_list)
                ##print(col3_list1)
                ##print(col4_list)
                ##print(col5_list)
                ##print(col6_list)
                message = "File uploaded successfully!"

                activities = {}
                most_likely_duration = {}
                successors = {}
                best_case_duration = {}
                worst_Case_Duration = {}
                num = {100}
                distribution=col6_list

                checkbox=request.form.get('agree')
            #     activity_names = request.form.getlist('activity')
            #     activity_durations = request.form.getlist('duration')
            #     activity_successors = request.form.getlist('successor')
            #     user_stddev = request.form.getlist('stddev')
            #     worst_dur = request.form.getlist('worst')

            #     ##print("checkbox",checkbox)
            #     if checkbox == 'yes':
            #         distribution = request.form['distribution']
            #     else:
            #         distribution_single = request.form.getlist('distribution_single')

                for name, dur, successor, sdev,worst in zip(col1_list, col2_list, col3_list1, col4_list,col5_list):
                    successor_set = set(successor.split(',')) if successor else set()
                    if not successor_set:
                        successor_set = {'End'}
                    activities[name] = successor_set
                    most_likely_duration[name] = int(dur)
                    successors[name] = successor_set
                    best_case_duration[name]= int(sdev)
                    worst_Case_Duration[name]= int(worst)
                ##print(distribution)
            #     ##print('distribution_single',distribution_single)

                # Set 'End' node with no successors and zero duration
                activities['End'] = set()
                most_likely_duration['End'] = '0'
                best_case_duration['End'] = 0
                activities['Start'] = set()
                most_likely_duration['Start'] = '0'
                best_case_duration['Start'] = 0
                worst_Case_Duration['Start'] = 0
                worst_Case_Duration['End'] = 0

                # Get activities that do not exist in the successors list
                activities_not_in_successors = set(activities.keys()) - set.union(*successors.values())

                # Remove 'Start' from the activities_not_in_successors set
                activities_not_in_successors.discard('Start')

                # Set activities_not_in_successors as successors of 'Start' and add them to the activities dictionary
                activities['Start'] = activities_not_in_successors
                successors['Start'] = activities_not_in_successors
                most_likely_duration['Start'] = 0

                for name in most_likely_duration.keys():
                    most_likely_duration[name] = int(most_likely_duration[name])

                    for name in most_likely_duration.keys():
                        most_likely_duration[name] = int(most_likely_duration[name])


                ##print("mostlikelydur",most_likely_duration)
                ##print("activities",activities)
                ##print("bestcase:",best_case_duration)
                ##print("worstcase:",worst_Case_Duration)
                # num=int(num)
                ##print("simnum",num)




                # Extract the numbers from the dictionary using dictionary comprehension
                anumbers = [value for value in most_likely_duration.values() if isinstance(value, int)]
                numbers=anumbers[:-2]
                ##print(numbers)

                # Extract the numbers from the dictionary using dictionary comprehension
                astddev = [value for value in best_case_duration.values() if isinstance(value, int)]
                stdnumbers=astddev[:-2]
                ##print("std:",stdnumbers)

                # Extract the numbers from the dictionary using dictionary comprehension
                worstcase = [value for value in worst_Case_Duration.values() if isinstance(value, int)]
                worst_Case_Dur=worstcase[:-2]
                ##print("worst:",worst_Case_Dur)

                activities_html = activities.copy()
                if 'End' in activities_html:
                    del activities_html['End']
                if 'Start' in activities_html:
                    del activities_html['Start']

                keys_list = list(activities_html.keys())
                values_list = [set(v) for v in activities_html.values()]
                values_list2=[s if s != {'End'} else '' for s in values_list]
                values_list2=[s if s != {' '} else '' for s in values_list]
                values_list3 = [','.join(s) if s else '' for s in values_list2]
                values_list3 = [s.replace("'", "").replace("{", "").replace("}", "") for s in values_list3]
                values_list3=[s.replace('End', "") for s in values_list3]
                # ##print the two lists
                ##print("Keys list:", keys_list)
                ##print("Values list:", values_list2)
                ##print("Values list2:", values_list3)



                normal_list = []
                uniform_list = []
                distribution_single1 = []


                for distribution_type, key in zip(distribution, keys_list):
                    if distribution_type == 'triangular':
                        normal_list.append('normal')
                        uniform_list.append('uniform')
                        distribution_single1.append('triangular')
                    elif distribution_type == 'normal':
                        normal_list.append('triangular')
                        uniform_list.append('uniform')
                        distribution_single1.append('normal')
                    elif distribution_type == 'uniform':
                        normal_list.append('normal')
                        uniform_list.append('triangular')
                        distribution_single1.append('uniform')





                ##print("n",normal_list)
                ##print("u",uniform_list)
                ##print("asıl",distribution_single1)


                rows1 = []
                # #print("rows", rows)
                for num1, key, value,best,worst,selected,normal,uniform in zip(numbers, keys_list, values_list3,stdnumbers,worst_Case_Dur,distribution_single1,normal_list,uniform_list):
                    row = {'activity': key, 'duration': num1, 'successor': value, "stddev": best,"worst":worst,   "optionvalue1":selected,"optionvalue2":normal,"optionvalue3":uniform }
                    rows1.append(row)

                # print('optionvalue1', rows1[-1]['optionvalue1'])
                #print("rows1", rows1)

                # print("distrubition",distribution)


                # Dropdown option
                dropdowntext= f"""
                <option value="triangular" {'selected' if distribution == 'triangular' else ''}>Triangular</option>
                <option value="normal" {'selected' if distribution == 'normal' else ''}>Normal</option>
                <option value="uniform" {'selected' if distribution == 'uniform' else ''}>Uniform</option>
            """
                # print("dropdowntext", dropdowntext)


                return render_template('index2.html', message=message,rows1 =rows1, dropdowntext=dropdowntext,num=100)
            else:
                message = """The selected file could not be read.
                            Please upload a valid file."""
                return render_template('index4.html', message=message)
        except Exception as e:
            message = f"An error occurred: {str(e)}. Please upload a valid file "
            return render_template('index4.html', message=message)
    else:
        message = "Please upload an excel file ."
        return render_template('index4.html', message=message)



# SECTION 4 - SECOND TAB'S CODES
@app.route('/newtab', methods=['GET', 'POST'])
def newtab():
        # Define activities and their dependencies
    try:
               # Define the default inputs
        activities = {

            'A': {'B', 'C'},
            'B': {'D'},
            'C': {'F', 'E'},
            'D': {'G'},
            'E': {'G'},
            'F': {'H'},
            'G': {'H'},
            'H': {'End'},
            'Start': {'A'},
            'End': {}
            }
        most_likely_duration = {

            'A': 3,
            'B': 4,
            'C': 8,
            'D': 5,
            'E': 7,
            'F': 8,
            'G': 4,
            'H': 6,
            'End':0,
            'Start': 0
            }

        best_case_duration = {

            'A': 1,
            'B': 1,
            'C': 5,
            'D': 1,
            'E': 5,
            'F': 6,
            'G': 1,
            'H': 1,
            'End': 0,
            'Start': 0
        }

        worst_Case_Duration = {

            'A': 10,
            'B': 10,
            'C': 50,
            'D': 10,
            'E': 50,
            'F': 60,
            'G': 10,
            'H': 10,
            'End': 0,
            'Start': 0
        }

        num = 100
        distribution="triangular"
        distribution_single=['triangular', 'triangular', 'triangular', 'triangular', 'triangular', 'triangular', 'triangular', 'triangular']
        checkbox = True



        if request.method == 'POST':
            activities = {}
            most_likely_duration = {}
            successors = {}
            best_case_duration = {}
            worst_Case_Duration = {}
            num = {}

            checkbox=request.form.get('agree')
            activity_names = request.form.getlist('activity')
            activity_durations = request.form.getlist('duration')
            activity_successors = request.form.getlist('successor')
            user_stddev = request.form.getlist('stddev')
            worst_dur = request.form.getlist('worst')
            num = request.form.__getitem__('num')
            #print("checkbox",checkbox)
            if checkbox == 'yes':
                distribution = request.form['distribution']
            else:
                distribution_single = request.form.getlist('distribution_single')
            for name, dur, successor, sdev,worst in zip(activity_names, activity_durations, activity_successors, user_stddev,worst_dur):
                successor_set = set(successor.split(',')) if successor else set()
                if not successor_set:
                    successor_set = {'End'}
                activities[name] = successor_set
                most_likely_duration[name] = int(dur)
                successors[name] = successor_set
                best_case_duration[name]= int(sdev)
                worst_Case_Duration[name]= int(worst)
            #print(distribution)
            #print('distribution_single',distribution_single)

            # Set 'End' node with no successors and zero duration
            activities['End'] = set()
            most_likely_duration['End'] = '0'
            best_case_duration['End'] = 0
            activities['Start'] = set()
            most_likely_duration['Start'] = '0'
            best_case_duration['Start'] = 0
            worst_Case_Duration['Start'] = 0
            worst_Case_Duration['End'] = 0

            # Get activities that do not exist in the successors list
            activities_not_in_successors = set(activities.keys()) - set.union(*successors.values())

            # Remove 'Start' from the activities_not_in_successors set
            activities_not_in_successors.discard('Start')

            # Set activities_not_in_successors as successors of 'Start' and add them to the activities dictionary
            activities['Start'] = activities_not_in_successors
            successors['Start'] = activities_not_in_successors
            most_likely_duration['Start'] = 0

            for name in most_likely_duration.keys():
                most_likely_duration[name] = int(most_likely_duration[name])

                # for name in most_likely_duration.keys():
                #     most_likely_duration[name] = int(most_likely_duration[name])


            #print("mostlikelydur",most_likely_duration)
            #print("activities",activities)
            #print("bestcase:",best_case_duration)
            #print("worstcase:",worst_Case_Duration)
            num=int(num)
            #print("simnum",num)




        # Extract the numbers from the dictionary using dictionary comprehension
        anumbers = [value for value in most_likely_duration.values() if isinstance(value, int)]
        numbers=anumbers[:-2]
        #print(numbers)

        # Extract the numbers from the dictionary using dictionary comprehension
        astddev = [value for value in best_case_duration.values() if isinstance(value, int)]
        stdnumbers=astddev[:-2]
        #print("std:",stdnumbers)

        # Extract the numbers from the dictionary using dictionary comprehension
        worstcase = [value for value in worst_Case_Duration.values() if isinstance(value, int)]
        worst_Case_Dur=worstcase[:-2]
        #print("worst:",worst_Case_Dur)

        activities_html = activities.copy()
        if 'End' in activities_html:
            del activities_html['End']
        if 'Start' in activities_html:
            del activities_html['Start']

        keys_list = list(activities_html.keys())
        values_list = [set(v) for v in activities_html.values()]
        values_list2=[s if s != {'End'} else '' for s in values_list]
        values_list2=[s if s != {' '} else '' for s in values_list]
        values_list3 = [','.join(s) if s else '' for s in values_list2]
        values_list3 = [s.replace("'", "").replace("{", "").replace("}", "") for s in values_list3]
        values_list3=[s.replace('End', "") for s in values_list3]
        # #print the two lists
        #print("Keys list:", keys_list)
        #print("Values list:", values_list2)
        #print("Values list2:", values_list3)



        normal_list = []
        uniform_list = []
        distribution_single1 = []


        if checkbox == 'yes':
            for i in keys_list:
                if distribution == 'triangular':
                    normal_list.append('normal')
                    uniform_list.append('uniform')
                    distribution_single1.append('triangular')
                elif distribution == 'normal':
                    normal_list.append('triangular')
                    uniform_list.append('uniform')
                    distribution_single1.append('normal')
                elif distribution == 'uniform':
                    normal_list.append('normal')
                    uniform_list.append('triangular')
                    distribution_single1.append('uniform')

        else:
            for distribution_type in distribution_single:
                if distribution_type == 'triangular':
                    normal_list.append('normal')
                    uniform_list.append('uniform')
                    distribution_single1.append('triangular')
                elif distribution_type == 'normal':
                    normal_list.append('triangular')
                    uniform_list.append('uniform')
                    distribution_single1.append('normal')
                elif distribution_type == 'uniform':
                    normal_list.append('normal')
                    uniform_list.append('triangular')
                    distribution_single1.append('uniform')

        #print("n",normal_list)
        #print("u",uniform_list)
        #print("asıl",distribution_single1)
        print("dur",numbers)
        print("key",keys_list)
        print("values_list3",values_list3)



        if 'numbers' in session and 'keys_list' in session and 'activity_successors' in session:
            numbers=session['numbers']
            keys_list=session['keys_list']
            values_list3=session['activity_successors']

            del session['numbers']
            del session['keys_list']
            del session['activity_successors']
        else:
            session['numbers1'] = numbers
            session['keys_list1'] = keys_list
            session['activity_successors1'] = values_list3



        rows1 = []
        # #print("rows", rows)
        for num1, key, value,best,worst,selected,normal,uniform in zip(numbers, keys_list, values_list3,stdnumbers,worst_Case_Dur,distribution_single1,normal_list,uniform_list):
            row = {'activity': key, 'duration': num1, 'successor': value, "stddev": best,"worst":worst,   "optionvalue1":selected,"optionvalue2":normal,"optionvalue3":uniform }
            rows1.append(row)






        # Dropdown option
        dropdowntext= f"""
        <option value="triangular" {'selected' if distribution == 'triangular' else ''}>Triangular</option>
        <option value="normal" {'selected' if distribution == 'normal' else ''}>Normal</option>
        <option value="uniform" {'selected' if distribution == 'uniform' else ''}>Uniform</option>
        """







        # Define number of simulations
        num_simulations = num


        # Define an empty dictionary to store criticality indices
        ci_dict = {k: 0 for k in activities}
        # Define an empty list to store the last activity's LF time for each simulation
        lf_list = []
        # Calculate earliest start, earliest finish, latest start, and latest finish times using Monte-Carlo simulation



        distribution_single1.append('normal')
        distribution_single1.append('normal')
        #print(distribution_single1)

        simulations = []
        critical_paths = []

        #print("num_simulations", num_simulations)
        for i in range(num_simulations):
            random.seed(i)  # set random seed for reproducibility
            durations = {}
            for idx, activity in enumerate(most_likely_duration):
                distribution2 = distribution_single1[idx]
                if distribution2 == 'triangular':
                    durations[activity] = round(random.triangular(best_case_duration[activity], most_likely_duration[activity], worst_Case_Duration[activity]), 2)
                    # #print('triangular')
                elif distribution2 == 'normal':
                    while True:
                        duration = round(random.normalvariate(most_likely_duration[activity], (worst_Case_Duration[activity]-best_case_duration[activity])/6), 2)
                        if duration >= best_case_duration[activity] and duration <= worst_Case_Duration[activity]:
                            durations[activity] = duration
                            break
                elif distribution2 == 'uniform':
                    durations[activity] = round(random.uniform(best_case_duration[activity], worst_Case_Duration[activity]), 2)
                    # #print('uniform')
            #print('dur',durations)



            es = {k: 0 for k in activities}
            ef = {k: durations[k] for k in activities}

            for k, v in activities.items():
                for dep in v:
                    es[dep] = max(es[dep], ef[k])
                    ef[dep] = es[dep] + durations[dep]

            lf = {k: ef['End'] for k in activities}
            ls = {k: lf[k] - durations[k] for k in activities}

            for k in reversed(list(activities.keys())):
                for dep in activities[k]:
                    lf[k] = min(lf[k], ls[dep])
                ls[k] = lf[k] - durations[k]

            lf_list.append(lf['End'])

            ls['End'] = es['End']
            lf['End'] = ef['End']

            ls['Start'] = es['Start']
            lf['Start']= ef['Start']

            for k in activities:
                es[k] = round(es[k], 2)
                ef[k] = round(ef[k], 2)
                ls[k] = round(ls[k], 2)
                lf[k] = round(lf[k], 2)



            # Define an empty dictionary to store the es times

            simulation_dict = {}
            for k in activities:
                es[k] = round(es[k], 2)
                ef[k] = round(ef[k], 2)
                ls[k] = round(ls[k], 2)
                lf[k] = round(lf[k], 2)
                simulation_dict[k] = {'ES': es[k], 'EF': ef[k], 'LS': ls[k], 'LF': lf[k], 'Duration': durations[k]}
            simulations.append(simulation_dict)


            critical_path = []
            for k in activities:
                if es[k] == ls[k]:
                    ci_dict[k] += 1
                    critical_path.append(k)


            # print("critical_path",critical_path)

            # print(f"Simulation {i+1} (Critical Path: {'->'.join(critical_path)})")
            # print("Activity\tES\tEF\tLS\tLF\tDur")

            critical_paths.append(critical_path)

            #for k in activities:
                #print(f"{k}\t\t{es[k]}\t{ef[k]}\t{ls[k]}\t{lf[k]}\t{durations[k]}")
                 # add the critical path for this simulation to the list
        #print("allpaths",critical_paths)
        #print("num.of.sim",len(critical_paths))
        simulations.append(simulation_dict)
        ##print("simulations",simulations)

        unique_list = []
        unique_indexes = []


        for i, sublst in enumerate(critical_paths):
            if sublst not in unique_list:
                unique_list.append(sublst)
                unique_indexes.append(i)

        #print(f"Unique List: {unique_list}")
        #print(f"Unique Indexes: {unique_indexes}")


        # formulas to get percentances of paths
        path_count =[]
        # print("critical_paths",critical_paths)
        for index in unique_indexes:
            count = critical_paths.count(critical_paths[index])
            path_count.append(count)
            #print("Sublist at index", index, "appears", count, "times in the original list.")
        #("path_count",path_count)
        #print("num",num)
        percentences=[]
        percentences=[(x/num)*100 for x in path_count]
        #print("percentences",percentences)



        #print("unique_indexes", unique_indexes)
        #CREATING GRAPH FOR CRITICAL PATHS
        for i, index in enumerate(unique_indexes):

            deneme= simulations[index]
            ##print("deneme",deneme)

            # create a new dictionary with required values
            duration = {}
            ef = {}
            lf = {}
            es = {}
            ls = {}
            for key, val in deneme.items():
                duration[key] = val['Duration']
                ef[key] = val['EF']
                lf[key] = val['LF']
                es[key] = val['ES']
                ls[key] = val['LS']

            # #print("es,ls")
            # #print(es)
            # #print(ef)
            # #print(ls)
            # #print(lf)
            # #print(duration)
            # # #print the new dictionaries
            # #print('duration:', duration)
            # #print('ef:', ef)
            # #print('lf:', lf)


            # Find critical path
            critical_path = []
            for k, v in activities.items():
                if ef[k] == lf[k]:
                    critical_path.append(k)

            # Create graph
            dot = Digraph(graph_attr={'rankdir': 'LR'})

            for k, v in activities.items():
                label = f"{index}.{k}\n{duration[k]}\n{es[k]}/{ef[k]}\n{ls[k]}/{lf[k]}"
                dot.node(f"{index}.{k}", label=label, shape='rectangle')
                if k in critical_path:
                    dot.node(f"{index}.{k}", style='filled', color='tomato')

            for k, v in activities.items():
                for dep in v:
                    dot.edge(f"{index}.{k}", f"{index}.{dep}")

            folder_path = os.path.join(current_directory, 'static')
            file_path1 = os.path.join(folder_path, f'simulation_{i}')


            # Render the graph to a file
            dot.render(file_path1, format='png', cleanup=True)

        for sublist in unique_list:
            sublist.remove('End')
            sublist.remove('Start')

        ##print("aaa",unique_list)


        unique_list1 = []

        for i, sublist in enumerate(unique_list):
            new_sublist = ['%' + str(percentences[i])] + sublist
            unique_list1.append(new_sublist)

        ##print(unique_list1)


        formatted_strings = [
        {
            'simn': ' - '.join(subgroup),
            'checkboxnum': f'checkbox{i+1}',
            'simnum': f'simulation_{i}'
        }
        for i, subgroup in enumerate(unique_list1)]



        cumulative_probabilities = []
        for i in range(num_simulations):
            cumulative_probability = (i + 1) / num_simulations
            cumulative_probabilities.append(cumulative_probability)

        # Create a column chart of criticality index
        x_values1 = list(ci_dict.keys())
        y_values1 = list(ci_dict.values())
        # #print("x_values1",x_values1)
        # #print("y_values1",y_values1)
        x_values = x_values1[:-2]
        y_values= y_values1[:-2]
        # #print("x_values1",x_values)
        # #print("y_values1",y_values)



        lf_list_sorted = sorted(lf_list)

        # #print(lf_list_sorted)
        # #print(cumulative_probabilities)
        # #print(x_values)
        # #print(y_values)



        # Create a line chart of the S-curve
        plt.figure()
        plt.plot(lf_list_sorted,cumulative_probabilities)
        plt.ylabel('Cumulative Probability')
        plt.xlabel('Duration')
        plt.title('S-curve')
        plt.savefig(os.path.join(current_directory, 'static', 'c1.png'), format='png')


        plt.figure()
        plt.bar(x_values, y_values, align='center')
        plt.xticks(range(len(ci_dict)-2), x_values)
        plt.ylabel('Criticality Index')
        plt.xlabel('Activity')
        plt.title('Criticality Index Chart')
        plt.savefig(os.path.join(current_directory, 'static', 'c2.png'), format='png')


        if 'username' in session:
            username = session.get('username')
        else:
            username = ""



        return render_template('index2.html',rows1=rows1,dropdowntext=dropdowntext,num=num,formatted_strings=formatted_strings,username =username )
    except Exception as e:
        message = f"An error occurred: {str(e)}. Please check your inputs."
        return render_template('index2.html',message = message, rows1=rows1,dropdowntext=dropdowntext,num=num)


client = OpenAI(api_key="YOUR KEY")

@app.route('/gpt')
def gpt():

    if 'username' in session:
        username = session.get('username')
    else:
        username = ""
    return render_template('index5.html',username =username )

@app.route('/chat', methods=['POST'])
def chat():


    memory = [
        {"role": "system", "content": "You are a chatbot for a project management website specializing in network diagrams and critical path method (CPM) analysis.The website allows users to upload Excel files with project activities, durations, and dependencies.It calculates earliest and latest start and finish times, identifies critical paths, generates CPM diagrams and Gantt charts, and performs Monte Carlo simulations for project scheduling.After running the Monte Carlo simulation in your website's application, you will receive:Critical Path for Each Simulation: Identification of the critical path for each simulated scenario.Criticality Indices: A measure of how often each activity appears on the critical path across simulations.S-Curve Chart: A plot showing the cumulative probability distribution of project completion times across all simulations.Criticality Index Chart: A bar chart visualizing the criticality index for each activity, indicating their importance in the project timeline.Visualizations of Critical Paths: Graphical representations (like Gantt charts or network diagrams) for each unique critical path identified in the simulations.The chatbot should assist users in understanding how to use the site, interpret results, and provide guidance on project management concepts. "},
        {"role": "system", "content": "If the user says to you something like 'I have activities A, B, C and D with durations of 2,9,4,3. The successor of activity A is B and C. Successor of activity B is C and D. C and D are the last activityies. Could you put them in order.' you will put them in order like this in python format:  activity_names= ['A', 'B', 'C', 'D']. activity_durations= ['2', '9', '4', '3'] activity_successors.= ['B,C', 'C,D', '', '']"},
        {"role": "system", "content": "If the user says to you something like 'In this project definition, various activities have been identified, including 'A,' 'B,' 'C,' 'D,' 'E,' 'F,' 'G,' 'H,' The dependencies among these activities are outlined, such as 'A' depending on both 'B' and 'C,' 'B' relying on 'D,' and 'C' having dependencies on both 'F' and 'E.' Further dependencies include 'D' depending on 'G' and 'E' depending on 'G.' 'F' is contingent on 'H,' and both 'G' and 'H' are dependent on reaching the endpoint. Each activity is assigned a specific duration, with 'A' taking 3 units of time, 'B' taking 4, 'C' taking 12, 'D' taking 5, 'E' taking 1, 'F' taking 2, 'G' taking 4, 'H' taking 6.The proper resPonse for that kind of input is: activity_names= ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],activity_durations =[3, 4, 12, 5, 1, 2, 4, 6],activity_successors= ['B,C', 'D', 'F,E', 'G','G', 'H', 'H', ''] "},
        {"role": "user", "content": "I have activities for my construction. Wall's duration is 6 days and after Wall Plumber will start work and it will take 5 days. Plumber's successors are Floor and Plaster. Floor will take 2 days and Plaster will take 3 days. After Plaster Painting will start and will take 1 day. When all those steps finishes Cleaning will start and will take 2 days. Could you put them in order for this website ? "},
        {"role": "assistant", "content":"I prepared your activities for website: activity_names= ['Wall','Plumber','Floor','Plaster','Painting','Cleaning']. activity_durations= ['6','5','2','3','1','2']. activity_successors = ['Plumber','Floor,Plaster','Cleaning','Painting','Cleaning','']"}

    ]

    if 'messages' in session:
        memory=session['messages']



    user_message = request.json['message']
    memory.append({"role": "user", "content": user_message})


    print("memory", memory)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=memory,
        temperature=0.1,  # Adjust as needed
    )   # Adjust as needed)
    reply = response.choices[0].message.content
    memory.append({"role": "assistant", "content": reply})


        # Function to extract list from text
    def extract_list(text, list_name):
        start = text.find(list_name) + len(list_name) + 2  # 3 for " = "
        end = text.find("]", start) + 1
        list_str = text[start:end]
        return eval(list_str)
    if "activity_names" in reply:
        # Extract each list
        activity_names = extract_list(reply, "activity_names")
        activity_durations = extract_list(reply, "activity_durations")
        activity_successors = extract_list(reply, "activity_successors")


        session['activity_names'] = activity_names
        session['activity_durations'] = activity_durations
        session['activity_successors'] = activity_successors


        show_button = True
        return jsonify({"reply": reply, "showButton": show_button})

    else:
        session['messages'] =memory

        show_button = False
        return jsonify({"reply": reply, "showButton": show_button})


@app.route('/GPTinput', methods=['GET', 'POST'])
def uploadgpt():
                # Check if the information exists in the session
        if 'activity_names' in session and 'activity_durations' in session and 'activity_successors' in session:

            activities = {}
            duration = {}
            successors = {}


            activity_names = session['activity_names']
            print("activity_names", activity_names)
            activity_durations = session['activity_durations']
            print("activity_durations", activity_durations)
            activity_successors = session['activity_successors']
            print("activity_successors", activity_successors)

            # Add 'Start' node with no successors
            for name, dur, successor in zip(activity_names, activity_durations, activity_successors):
                successor_set = set(successor.split(',')) if successor else set()
                print("successor_set", successor_set)
                if not successor_set:
                    successor_set = {'End'}
                activities[name] = successor_set
                duration[name] = int(dur)
                successors[name] = successor_set
            # #print("orj", activities)
            # Set 'End' node with no successors and zero duration
            activities['End'] = set()
            duration['End'] = '0'
            activities['Start'] = set()
            duration['Start'] = '0'

            # Get activities that do not exist in the successors list
            activities_not_in_successors = set(activities.keys()) - set.union(*successors.values())

            # Remove 'Start' from the activities_not_in_successors set
            activities_not_in_successors.discard('Start')

            # Set activities_not_in_successors as successors of 'Start' and add them to the activities dictionary
            activities['Start'] = activities_not_in_successors
            successors['Start'] = activities_not_in_successors
            # duration['Start'] = 0

            #print("Activities not in successors list:", activities_not_in_successors)
            print("asdaasdasdsdactivity_names", activity_names)
            print("activity_durations", activity_durations)
            print("activity_successors", activity_successors)




        for name in duration.keys():
            duration[name] = int(duration[name])


            for name in duration.keys():
                duration[name] = int(duration[name])





        # print(duration)
        # print(activities)

        # Extract the numbers from the dictionary using dictionary comprehension
        anumbers = [value for value in duration.values() if isinstance(value, int)]
        numbers=anumbers[:-2]
        #print('numbers',numbers)

        activities_html = activities.copy()
        if 'End' in activities_html:
            del activities_html['End']
        if 'Start' in activities_html:
            del activities_html['Start']


        keys_list = list(activities_html.keys())
        values_list = [set(v) for v in activities_html.values()]
        values_list2=[s if s != {'End'} else '' for s in values_list]
        values_list2=[s if s != {' '} else '' for s in values_list]
        values_list3 = [','.join(s) if s else '' for s in values_list2]
        values_list3 = [s.replace("'", "").replace("{", "").replace("}", "") for s in values_list3]
        values_list3=[s.replace('End', "") for s in values_list3]
        # #print the two lists
        #print("Keys list:", keys_list)
        # #print("Values list:", values_list2)
        #print("Values list2:", values_list3)




        rows = []
        # print("rows", rows)
        for num, key, value in zip(numbers, keys_list, values_list3):
            #print("value", value)
            row = {'activity': key, 'duration': num, 'successor': value}
            rows.append(row)

        if 'username' in session:
            username = session.get('username')
        else:
            username = ""

        message = "Message uploaded successfully! Please check the inputs and click on calculate"
        return render_template('index.html', message=message,rows=rows,username=username)


@app.route('/GPTinput2', methods=['GET', 'POST'])
def uploadgpt2():

        activities = {

            'A': {'B', 'C'},
            'B': {'D'},
            'C': {'F', 'E'},
            'D': {'G'},
            'E': {'G'},
            'F': {'H'},
            'G': {'H'},
            'H': {'End'},
            'Start': {'A'},
            'End': {}
            }
        most_likely_duration = {

            'A': 3,
            'B': 4,
            'C': 8,
            'D': 5,
            'E': 7,
            'F': 8,
            'G': 4,
            'H': 6,
            'End':0,
            'Start': 0
            }

        best_case_duration = {

            'A': 1,
            'B': 1,
            'C': 5,
            'D': 1,
            'E': 5,
            'F': 6,
            'G': 1,
            'H': 1,
            'End': 0,
            'Start': 0
        }

        worst_Case_Duration = {

            'A': 10,
            'B': 10,
            'C': 50,
            'D': 10,
            'E': 50,
            'F': 60,
            'G': 10,
            'H': 10,
            'End': 0,
            'Start': 0
        }

        num = 100
        distribution="triangular"
        distribution_single=['triangular', 'triangular', 'triangular', 'triangular', 'triangular', 'triangular', 'triangular', 'triangular']
        checkbox = True
        # Extract the numbers from the dictionary using dictionary comprehension
        anumbers = [value for value in most_likely_duration.values() if isinstance(value, int)]
        numbers=anumbers[:-2]
        #print(numbers)

        # Extract the numbers from the dictionary using dictionary comprehension
        astddev = [value for value in best_case_duration.values() if isinstance(value, int)]
        stdnumbers=astddev[:-2]
        #print("std:",stdnumbers)

        # Extract the numbers from the dictionary using dictionary comprehension
        worstcase = [value for value in worst_Case_Duration.values() if isinstance(value, int)]
        worst_Case_Dur=worstcase[:-2]
        #print("worst:",worst_Case_Dur)

        activities_html = activities.copy()
        if 'End' in activities_html:
            del activities_html['End']
        if 'Start' in activities_html:
            del activities_html['Start']

        keys_list = list(activities_html.keys())
        values_list = [set(v) for v in activities_html.values()]
        values_list2=[s if s != {'End'} else '' for s in values_list]
        values_list2=[s if s != {' '} else '' for s in values_list]
        values_list3 = [','.join(s) if s else '' for s in values_list2]
        values_list3 = [s.replace("'", "").replace("{", "").replace("}", "") for s in values_list3]
        values_list3=[s.replace('End', "") for s in values_list3]
        # #print the two lists
        #print("Keys list:", keys_list)
        #print("Values list:", values_list2)
        #print("Values list2:", values_list3)



        normal_list = []
        uniform_list = []
        distribution_single1 = []


        if checkbox == 'yes':
            for i in keys_list:
                if distribution == 'triangular':
                    normal_list.append('normal')
                    uniform_list.append('uniform')
                    distribution_single1.append('triangular')
                elif distribution == 'normal':
                    normal_list.append('triangular')
                    uniform_list.append('uniform')
                    distribution_single1.append('normal')
                elif distribution == 'uniform':
                    normal_list.append('normal')
                    uniform_list.append('triangular')
                    distribution_single1.append('uniform')

        else:
            for distribution_type in distribution_single:
                if distribution_type == 'triangular':
                    normal_list.append('normal')
                    uniform_list.append('uniform')
                    distribution_single1.append('triangular')
                elif distribution_type == 'normal':
                    normal_list.append('triangular')
                    uniform_list.append('uniform')
                    distribution_single1.append('normal')
                elif distribution_type == 'uniform':
                    normal_list.append('normal')
                    uniform_list.append('triangular')
                    distribution_single1.append('uniform')

        #print("n",normal_list)
        #print("u",uniform_list)
        #print("asıl",distribution_single1)
        print("dur",numbers)
        print("key",keys_list)
        print("values_list3",values_list3)

                # Check if the information exists in the session
        if 'activity_names' in session and 'activity_durations' in session and 'activity_successors' in session:



            keys_list = session['activity_names']

            numbers= session['activity_durations']

            values_list3 = session['activity_successors']
        else:
            session['numbers1'] = numbers
            session['keys_list1'] = keys_list
            session['activity_successors1'] = values_list3






        rows1 = []
        # #print("rows", rows)
        for num1, key, value,best,worst,selected,normal,uniform in zip(numbers, keys_list, values_list3,stdnumbers,worst_Case_Dur,distribution_single1,normal_list,uniform_list):
            row = {'activity': key, 'duration': num1, 'successor': value, "stddev": best,"worst":worst,   "optionvalue1":selected,"optionvalue2":normal,"optionvalue3":uniform }
            rows1.append(row)

        if 'username' in session:
            username = session.get('username')
        else:
            username = ""

        num = 100
        distribution="triangular"


        dropdowntext= f"""
        <option value="triangular" {'selected' if distribution == 'triangular' else ''}>Triangular</option>
        <option value="normal" {'selected' if distribution == 'normal' else ''}>Normal</option>
        <option value="uniform" {'selected' if distribution == 'uniform' else ''}>Uniform</option>
        """

        message = "Message uploaded successfully! Please check the inputs and click on calculate"
        print("message", message)
        return render_template('index2.html',rows1=rows1,dropdowntext=dropdowntext,num=num,username =username )


@app.route('/submit_idea', methods=['POST'])
def submit_idea():
    # Extract the 'idea' from the request JSON, which matches the form data
    idea_content = request.json['idea']
    # Use 'feedback_text' to match the field name in the Feedback model
    new_feedback = Feedback(feedback_text=idea_content)
    db.session.add(new_feedback)
    db.session.commit()
    return jsonify({'message': 'Thank you for your feedback!'})



@app.route('/admin/feedback')
def view_feedback():
    session.clear()
    feedbacks = Feedback.query.all()
    feedback_data = [{'id': feedback.id, 'text': feedback.feedback_text, 'timestamp': feedback.timestamp} for feedback in feedbacks]
    return jsonify(feedback_data)




if __name__ == '__main__':
    app.run(debug=True)
