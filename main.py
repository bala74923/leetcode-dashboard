from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import openpyxl
import data

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    file = request.files['file']
    contest_name = request.form['contest']
    column_name = request.form['column']

    # Read the Excel file using pandas
    df = pd.read_excel(file)

    global result_table
    global black_list
    # Process the data (e.g., extract usernames and fetch marks)
    result_table,black_list = process_data(df,id_column_name=column_name, contest_name=contest_name)



    return render_template('result.html', result_table=result_table,black_list=black_list)


@app.route('/result')
def result():
    global result_table  # Use the global variable
    global black_list
    if result_table is None or black_list is None:
        return redirect(url_for('index'))  # If result_table is not available, redirect to the index page

    return render_template('result.html', result_table=result_table,black_list=black_list)


# Route to display the form
@app.route('/')
def index():
    return render_template('index.html')

def process_data(df,id_column_name,contest_name):
    #black list -> un attended /invalid
    result_table ,black_list= [],[]
    print('process data is called')

    collected_data = data.get_data(contest_name)
    # Iterate over each row in the DataFrame
    for _, row in df.iterrows():
        username = str(row[id_column_name]).lower().strip()

        # Fetch marks from the third-party API based on the username
        if collected_data.get(username,None ) is not None:
            user_data = row.copy().to_dict()
            contest_user_data = collected_data.get(username)
            user_data['rank'] = contest_user_data['rank']
            user_data['solved'] = contest_user_data['solved']
            user_data['page_link'] = contest_user_data['page_link']
            result_table.append(user_data)
        else:
            black_list.append(row.copy().to_dict())
    print(df)

    #sort based on rank
    result_table.sort(key=lambda x:x['rank'])
    return result_table,black_list



if __name__ == '__main__':
    app.run(debug=True)
    #flask --app main run --debug
