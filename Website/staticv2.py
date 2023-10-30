from flask import Flask, render_template, request, redirect, render_template_string 
from graphviz import Digraph
from IPython.display import Image
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

current_directory = os.path.dirname(os.path.abspath(__file__))
#print("current_directory", current_directory)

# SECTION 1 - EXCEL IMPORT FOR FIRST TAB
app = Flask(__name__)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            df = pd.read_excel(file)
            col1_list = df.iloc[:, 0].tolist()  # create list from first column
            col2_list = df.iloc[:, 1].tolist()  # create list from second column
            col3_list = df.iloc[:, 2].fillna('').apply(lambda x: x.split(',') if isinstance(x, str) else []).tolist()
            col3_list1 = [','.join(sublist) for sublist in col3_list]
            #print(col1_list)
            #print(col2_list)
            #print(col3_list1)
            message = "File uploaded successfully!"

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




            for name in duration.keys():
                duration[name] = int(duration[name])


                for name in duration.keys():
                    duration[name] = int(duration[name])




            
            #print(duration)
            #print(activities)       

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



            # Generate the HTML code
            html_code = ""
            for num, key, value in zip(numbers, keys_list, values_list3):
                html_code += f"""
                    <tr>
                        <td><input type="text" name="activity" value="{key}"></td>
                        <td><input type="number" name="duration" min="0" value="{num}"></td>
                        <td><input type="text" name="successor" value="{value}"></td>
                        <td><button type="button" class="remove-row">Remove</button></td>
                    </tr>
                """

            # Define the file path
            file_path = os.path.join(current_directory, 'templates', 'index.html')

            # Read in the index.html file
            with open(file_path, 'r') as f:
                index_html = f.read()

            # Find the start and end markers of the section to be replaced
            start_marker = '<!-- START GENERATED HTML CODE -->'
            end_marker = '<!-- END GENERATED HTML CODE -->'
            start_pos = index_html.find(start_marker)
            end_pos = index_html.find(end_marker) + len(end_marker)


            # Replace the section with the new HTML code
            new_index_html = index_html[:start_pos] +start_marker+ html_code +end_marker+ index_html[end_pos:]

            # Write the modified index.html file back out
            with open(file_path, 'w') as f:
                f.write(new_index_html)


            return render_template('index.html', message=message)
        else:
            message = """The selected file could not be read.
                         Please upload a valid file."""
            return render_template('index3.html', message=message)
    else:
        message = "Please upload an excel file ."
        return render_template('index3.html', message=message)
# SECTION 2 - FIRST TAB'S CODES
@app.route('/', methods=['GET', 'POST'])
def home():

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
        'C': 2, 
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




    for name in duration.keys():
        duration[name] = int(duration[name])


        for name in duration.keys():
            duration[name] = int(duration[name])




       
    #print(duration)
    #print(activities)       

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



    # Generate the HTML code
    html_code = ""
    for num, key, value in zip(numbers, keys_list, values_list3):
        html_code += f"""
            <tr>
                <td><input type="text" name="activity" value="{key}"></td>
                <td><input type="number" name="duration" min="0" value="{num}"></td>
                <td><input type="text" name="successor" value="{value}"></td>
                <td><button type="button" class="remove-row">Remove</button></td>
            </tr>
        """

    # Define the file path
    file_path = os.path.join(current_directory, 'templates', 'index.html')

    # Read in the index.html file
    with open(file_path, 'r') as f:
        index_html = f.read()

    # Find the start and end markers of the section to be replaced
    start_marker = '<!-- START GENERATED HTML CODE -->'
    end_marker = '<!-- END GENERATED HTML CODE -->'
    start_pos = index_html.find(start_marker)
    end_pos = index_html.find(end_marker) + len(end_marker)


    # Replace the section with the new HTML code
    new_index_html = index_html[:start_pos] +start_marker+ html_code +end_marker+ index_html[end_pos:]

    # Write the modified index.html file back out
    with open(file_path, 'w') as f:
        f.write(new_index_html)


    
    # last_item = None
    # for key, value in activities.items():
    #     if key not in value:
    #         last_item = key          

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

    
    #print("activities_list",activities_list)

    # Plot horizontal bars for each activity
    for i, (activity, start, end) in enumerate(activities_list):
        duration = end - start
        ax.broken_barh([(start, duration)], (i, 0.5), facecolors='blue')

    ax.set_title("Gantt Chart")    

        # Save the Gantt chart as a PNG file
    fig.savefig(os.path.join(current_directory, 'static', 'gantt.png'))

    # # Display the Gantt chart as an image
    # Image(filename='gantt.png')
 
    return render_template('index.html')
# SECTION 3 - EXCEL IMPORT FOR SECOND TAB

@app.route('/uploadsc', methods=['GET', 'POST'])
def upload_file_sc():
    if request.method == 'POST':
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
            #print(col1_list)
            #print(col2_list)
            #print(col3_list1)
            #print(col4_list)
            #print(col5_list)
            #print(col6_list)
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

        #     #print("checkbox",checkbox) 
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
            #print(distribution)
        #     #print('distribution_single',distribution_single)

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


            #print("mostlikelydur",most_likely_duration)
            #print("activities",activities)   
            #print("bestcase:",best_case_duration)   
            #print("worstcase:",worst_Case_Duration)  
            # num=int(num)
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





            #print("n",normal_list) 
            #print("u",uniform_list) 
            #print("asıl",distribution_single1) 
        
            # Generate the HTML code
            html_code = ""
            for num1, key, value,best,worst,selected,normal,uniform in zip(numbers, keys_list, values_list3,stdnumbers,worst_Case_Dur,distribution_single1,normal_list,uniform_list):
                html_code += f"""
                    <tr>
                        <td><input type="text" name="activity" value="{key}"></td>
                        <td><input type="number" name="duration" min="0" value="{num1}"></td>
                        <td><input type="text" name="successor" value="{value}"></td>
                        <td><input type="number" name="stddev" min="0" value="{best}"></td>
                        <td><input type="number" name="worst" min="0" value="{worst}"></td>
                        <td>                
                            <select id="distribution_single" name="distribution_single">                         
                    <option value="{selected}" selected>{selected}</option>
                    <option value="{normal}">{normal}</option>
                    <option value="{uniform}">{uniform}</option>
                            </select>
                        </td>
                        <td><button type="button" class="remove-row">Remove</button></td>
                        
                    </tr>
                """
            # #print(html_code)
            # Define the file path
            file_path = os.path.join(current_directory, 'templates', 'index2.html')

            # Read in the index.html file
            with open(file_path, 'r') as f:
                index_html = f.read()

            # Find the start and end markers of the section to be replaced
            start_marker = '<!-- START GENERATED HTML CODE -->'
            end_marker = '<!-- END GENERATED HTML CODE -->'
            start_pos = index_html.find(start_marker)
            end_pos = index_html.find(end_marker) + len(end_marker)


            # Replace the section with the new HTML code
            new_index_html = index_html[:start_pos] +start_marker+ html_code +end_marker+ index_html[end_pos:]

            # Write the modified index.html file back out
            with open(file_path, 'w') as f:
                f.write(new_index_html)

        


        # # Dropdown option

        # dropdowntext = ""
        # if distribution == 'triangular':
        #     dropdowntext = """                           
        #         <option value="triangular" selected>Triangular</option>
        #         <option value="normal">Normal</option>
        #         <option value="uniform">Uniform</option>"""
        # elif distribution == 'normal':
        #     dropdowntext = """     
        #         <option value="normal" selected>Normal</option>                      
        #         <option value="triangular">Triangular</option>
        #         <option value="uniform">Uniform</option>"""
        # elif distribution == 'uniform':
        #     dropdowntext = """  
        #         <option value="uniform" selected>Uniform</option>
        #         <option value="triangular">Triangular</option>
        #         <option value="normal">Normal</option>"""
        # # #print(dropdowntext)


        # # Define the file path
        # file_path = os.path.join(current_directory, 'templates', 'index2.html')

        # # Read in the index.html file
        # with open(file_path, 'r') as f:
        #     index_html = f.read()

        # # Find the start and end markers of the section to be replaced
        # start_marker = '<!-- START GENERATED DROPDOWN CODE -->'
        # end_marker = '<!-- END GENERATED DROPDOWN CODE -->'
        # start_pos = index_html.find(start_marker)
        # end_pos = index_html.find(end_marker) + len(end_marker)


        # # Replace the section with the new HTML code
        # new_index_html = index_html[:start_pos] +start_marker+ dropdowntext +end_marker+ index_html[end_pos:]

        # # Write the modified index.html file back out
        # with open(file_path, 'w') as f:
        #     f.write(new_index_html)



            return render_template('index2.html', message=message)
        else:
            message = """The selected file could not be read.
                         Please upload a valid file."""
            return render_template('index4.html', message=message)
    else:
        message = "Please upload an excel file ."
        return render_template('index4.html', message=message)
# SECTION 4 - SECOND TAB'S CODES
@app.route('/newtab', methods=['GET', 'POST'])
def newtab():
    # Define activities and their dependencies

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
  
    # Generate the HTML code
    html_code = ""
    for num1, key, value,best,worst,selected,normal,uniform in zip(numbers, keys_list, values_list3,stdnumbers,worst_Case_Dur,distribution_single1,normal_list,uniform_list):
        html_code += f"""
            <tr>
                <td><input type="text" name="activity" value="{key}"></td>
                <td><input type="number" name="duration" min="0" value="{num1}"></td>
                <td><input type="text" name="successor" value="{value}"></td>
                <td><input type="number" name="stddev" min="0" value="{best}"></td>
                <td><input type="number" name="worst" min="0" value="{worst}"></td>
                <td>                
                    <select id="distribution_single" name="distribution_single">                         
            <option value="{selected}" selected>{selected}</option>
            <option value="{normal}">{normal}</option>
            <option value="{uniform}">{uniform}</option>
                    </select>
                </td>
                <td><button type="button" class="remove-row">Remove</button></td>
                
            </tr>
        """
    # #print(html_code)
    # Define the file path
    file_path = os.path.join(current_directory, 'templates', 'index2.html')

    # Read in the index.html file
    with open(file_path, 'r') as f:
        index_html = f.read()

    # Find the start and end markers of the section to be replaced
    start_marker = '<!-- START GENERATED HTML CODE -->'
    end_marker = '<!-- END GENERATED HTML CODE -->'
    start_pos = index_html.find(start_marker)
    end_pos = index_html.find(end_marker) + len(end_marker)


    # Replace the section with the new HTML code
    new_index_html = index_html[:start_pos] +start_marker+ html_code +end_marker+ index_html[end_pos:]

    # Write the modified index.html file back out
    with open(file_path, 'w') as f:
        f.write(new_index_html)

    


    # Dropdown option

    dropdowntext = ""
    if distribution == 'triangular':
        dropdowntext = """                           
            <option value="triangular" selected>Triangular</option>
            <option value="normal">Normal</option>
            <option value="uniform">Uniform</option>"""
    elif distribution == 'normal':
        dropdowntext = """     
            <option value="normal" selected>Normal</option>                      
            <option value="triangular">Triangular</option>
            <option value="uniform">Uniform</option>"""
    elif distribution == 'uniform':
        dropdowntext = """  
            <option value="uniform" selected>Uniform</option>
            <option value="triangular">Triangular</option>
            <option value="normal">Normal</option>"""
    # #print(dropdowntext)


    # Define the file path
    file_path = os.path.join(current_directory, 'templates', 'index2.html')

    # Read in the index.html file
    with open(file_path, 'r') as f:
        index_html = f.read()

    # Find the start and end markers of the section to be replaced
    start_marker = '<!-- START GENERATED DROPDOWN CODE -->'
    end_marker = '<!-- END GENERATED DROPDOWN CODE -->'
    start_pos = index_html.find(start_marker)
    end_pos = index_html.find(end_marker) + len(end_marker)


    # Replace the section with the new HTML code
    new_index_html = index_html[:start_pos] +start_marker+ dropdowntext +end_marker+ index_html[end_pos:]

    # Write the modified index.html file back out
    with open(file_path, 'w') as f:
        f.write(new_index_html)




    
    # Simulation number option
    simnum = f"""<td><input type="number" name="num" min="0" value="{num}"></td>"""
    #print('simnum',simnum)

    # Define the file path
    file_path = os.path.join(current_directory, 'templates', 'index2.html')

    # Read in the index.html file
    with open(file_path, 'r') as f:
        index_html = f.read()

    # Find the start and end markers of the section to be replaced
    start_marker = '<!-- START GENERATED SIMNUM CODE -->'
    end_marker = '<!-- END GENERATED SIMNUM CODE -->'
    start_pos = index_html.find(start_marker)
    end_pos = index_html.find(end_marker) + len(end_marker)


    # Replace the section with the new HTML code
    new_index_html = index_html[:start_pos] +start_marker+ simnum +end_marker+ index_html[end_pos:]

    # Write the modified index.html file back out
    with open(file_path, 'w') as f:
        f.write(new_index_html)




    # CHECKBOX option

    if checkbox == 'yes':
        checkboxhtml = f"""
                <td><input type="checkbox" name="agree" value="yes" id="agree-checkbox">
                    <select id="distribution" name="distribution" disabled>"""
    else:
        checkboxhtml = f"""
                <td><input type="checkbox" name="agree" value="yes" id="agree-checkbox">
                    <select id="distribution" name="distribution" disabled>"""
    #print('checkboxhtml',checkboxhtml)
    # Define the file path
    file_path = os.path.join(current_directory, 'templates', 'index2.html')

    # Read in the index.html file
    with open(file_path, 'r') as f:
        index_html = f.read()

    # Find the start and end markers of the section to be replaced
    start_marker = '<!-- START GENERATED CHECK CODE -->'
    end_marker = '<!-- END GENERATED CHECK CODE -->'
    start_pos = index_html.find(start_marker)
    end_pos = index_html.find(end_marker) + len(end_marker)


    # Replace the section with the new HTML code
    new_index_html = index_html[:start_pos] +start_marker+ checkboxhtml +end_marker+ index_html[end_pos:]

    # Write the modified index.html file back out
    with open(file_path, 'w') as f:
        f.write(new_index_html)
                        
                

    

    # Define number of simulations
    num_simulations = num
    #print(num_simulations)
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

        
        # #print(critical_path)

        # #print(f"Simulation {i+1} (Critical Path: {'->'.join(critical_path)})")
        # #print("Activity\tES\tEF\tLS\tLF\tDur")
        for k in activities:
            # print(f"{k}\t\t{es[k]}\t{ef[k]}\t{ls[k]}\t{lf[k]}\t{durations[k]}")

            critical_paths.append(critical_path)  # add the critical path for this simulation to the list
    ##print("allpaths",critical_paths) 
    simulations.append(simulation_dict)         
    ##print("simulations",simulations)
    
    unique_list = []
    unique_indexes = []

    for i, sublst in enumerate(critical_paths):
        if sublst not in unique_list:
            unique_list.append(sublst)
            unique_indexes.append(i)

    ##print(f"Unique List: {unique_list}")
    ##print(f"Unique Indexes: {unique_indexes}")
    

    # formulas to get percentances of paths
    path_count =[]
    ##print("critical_paths",critical_paths)
    for index in unique_indexes:
        count = critical_paths.count(critical_paths[index])
        path_count.append(count)
        #print("Sublist at index", index, "appears", count, "times in the original list.")
    ##print("path_count",path_count)

    percentences=[]
    percentences=[(x/num)*100 for x in path_count]
    ##print("percentences",percentences)




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

    # Generate the HTML code
    PATHhtml_code = ""
    for i, paths in enumerate(unique_list1):
        PATHhtml_code += f"""
        <form>
            <input type="checkbox" id="checkbox{i+1}" onclick="toggleImage('simulation_{i}', 'checkbox{i+1}')">
            <label style="color: white;">{' - '.join(paths)}</label>
        </form>  

        <div style="position: relative;">
            <img class="image simulation_{i}" src="{{{{ url_for('static', filename='simulation_{i}.png') }}}}" alt="Graph" style="display:none;">
        </div>
        """

    ##print(PATHhtml_code)
    # Define the file path
    file_path = os.path.join(current_directory, 'templates', 'index2.html')

    # Read in the index.html file
    with open(file_path, 'r') as f:
        index_html = f.read()

    # Find the start and end markers of the section to be replaced
    start_marker = '<!-- START GENERATED PATH CODE -->'
    end_marker = '<!-- END GENERATED PATH CODE -->'
    start_pos = index_html.find(start_marker)
    end_pos = index_html.find(end_marker) + len(end_marker)


    # Replace the section with the new HTML code
    new_index_html = index_html[:start_pos] +start_marker+ PATHhtml_code +end_marker+ index_html[end_pos:]

    # Write the modified index.html file back out
    with open(file_path, 'w') as f:
        f.write(new_index_html)











    cumulative_probabilities = []
    for i in range(num_simulations):
        cumulative_probability = (i + 1) / num_simulations
        cumulative_probabilities.append(cumulative_probability)
        
    # Create a column chart of criticality index
    x_values1 = list(ci_dict.keys())
    y_values1 = list(ci_dict.values())
    # #print("x_values1",x_values1)
    # #print("y_values1",y_values1)
    x_values = list(set(x_values1) - set(['Start', 'End']))
    y_values= y_values1[:-2]
    # #print("x_values1",x_values)
    # #print("y_values1",y_values)
    
    """

    # the original version
    
    # problem is that dictionaries are not ordered,
    # thus there is no determined 5th element etc
    # 
    # problems can occur with the kezs and values
    # being retrieved in a different order
    # or the last two elements not being the desired ones

    # Create a column chart of criticality index
    x_values1 = list(ci_dict.keys())
    y_values1 = list(ci_dict.values())
    x_values = x_values1[:-2]
    y_values= y_values1[:-2]
    """

    # if os.path.exists('C:/Users/MONSTER/OneDrive/Masaüstü/test/folder/static/c1.png'):
    #     os.remove('C:/Users/MONSTER/OneDrive/Masaüstü/test/folder/static/c1.png')


    lf_list_sorted = sorted(lf_list)

    # #print(lf_list_sorted)
    # #print(cumulative_probabilities)
    # #print(x_values)
    # #print(y_values)

    # if os.path.exists('C:/Users/MONSTER/OneDrive/Masaüstü/test/folder/static/c2.png'):
    #     os.remove('C:/Users/MONSTER/OneDrive/Masaüstü/test/folder/static/c2.png')



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


    return render_template('index2.html')


if __name__ == '__main__':
    app.run(debug=True)


