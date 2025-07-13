from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load the pre-trained model
model = joblib.load('AI_Crime_Prediction_Model.joblib')

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get input values from the form
        state = request.form.get('state').strip().title()
        month = request.form.get('month').strip().title()
        crime_type = request.form.get('crime_type').strip().title()

        # Check if any field is empty
        if not all([state, month, crime_type]):
            return render_template('index1.html', prediction_result="Please fill in all fields.")

        try:
            # Prepare input data for the model
            user_input = pd.DataFrame({
                'State': [state],
                'Month': [month],
                'Crime_Type': [crime_type]
            })
            
            # Debugging: Print the input data
            print(f"User Input: {user_input}")

            # Make prediction using the loaded model
            crime_percentage_prediction = model.predict(user_input)[0]
            
            # Debugging: Print the prediction result
            print(f"Prediction Result: {crime_percentage_prediction}")

            # Format the result
            prediction_result = f"The predicted Crime Percentage for {crime_type} in {state} during {month} is: {crime_percentage_prediction:.2f}%"
            return render_template('index1.html', prediction_result=prediction_result)

        except Exception as e:
            # Handle errors such as unseen categories or model issues
            print(f"Error: {e}")
            return render_template('index1.html', prediction_result=f"Error: {str(e)}. Please check your inputs and try again.")

if __name__ == '__main__':
    app.run(debug=True)
