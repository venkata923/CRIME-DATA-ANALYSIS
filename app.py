from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the dataset
data = pd.read_csv('data_crime.csv')

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get input values from the form
    state = request.form['state'].strip()
    month = request.form['month'].strip()
    crime_type = request.form['crime_type'].strip()

    # Ensure input data matches the format of the dataset (capitalize first letter of each word)
    state = state.title()
    month = month.title()
    crime_type = crime_type.title()

    # Debugging: Print the input data
    print(f"Received Input: State: {state}, Month: {month}, Crime Type: {crime_type}")

    # Check if the input matches any row in the dataset
    match = data[
        (data['State'] == state) & 
        (data['Month'] == month) & 
        (data['Crime_Type'] == crime_type)
    ]

    # If a match is found, extract the crime percentage
    if not match.empty:
        crime_percentage = match['Crime_Percentage'].values[0]
        result = f"Crime Percentage for {crime_type} in {state} during {month} is: {crime_percentage:.2f}%"
    else:
        result = "No matching data found for the inputs provided."

    # Return the result to the template
    return render_template('index1.html', prediction_result=result)

if __name__ == '__main__':
    app.run(debug=True)
