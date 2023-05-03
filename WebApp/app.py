import os
import sys

# Add the parent directory to the Python path
parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_directory)

from flask import Flask, render_template, request, jsonify
from dataloader.dataloader_s import DataLoaderSimple
from Predict import Predictor

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', result=None)


@app.route('/submit_form', methods=['POST'])
def submit_form():
    # if request.method == 'POST':
    print('Predict button is clicked')
    dictionary = {}
    dictionary['sponsored_or_not'] = request.json['sponsored_or_not']
    dictionary['in_US_or_not'] = request.json['in_US_or_not']
    dictionary['company_size'] = request.json['company_size']
    dictionary['company_industry'] = request.json['company_industry']
    dictionary['company_type'] = request.json['company_type']
    dictionary['employee_benefits'] = request.json['employee_benefits']
    dictionary['employee_rating_benefits'] = request.json['employee_rating_benefits']
    dictionary['ceo_approval_rating'] = request.json['ceo_approval_rating']
    dictionary['recommend_to_friend_rating'] = request.json['recommend_to_friend_rating']
    dictionary['company_overall_rating'] = request.json['company_overall_rating']
    dictionary['job_level'] = request.json['job_level']
    dictionary['job_category'] = request.json['job_category']
    dictionary['reviews_pro'] = request.json['reviews_pro']
    dictionary['reviews_con'] = request.json['reviews_con']
    dictionary['job_description'] = request.json['job_description']

    print('Dictionary is ')
    print(dictionary)

    # 1. Call an API  to send the dictionary to another python file, then the API will return a Numpy Array called cleaned_data
    # 2. Call another API to send the cleaned_data to another python file, then I will get an integer called predicted_salary
    # 3. Finally, show the predicted_salary to the HTML

    # Call the clean_data function from data_cleaner.py
    dataloader = DataLoaderSimple()
    cleaned_data = dataloader.fit_transform(dictionary)

    # Call the predict_salary function from model_predictor.py
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    predictor = Predictor(os.path.join(root_path, 'result/best.model'), os.path.join(root_path, 'result/best.genes'))
    predicted_salary = predictor.predict(cleaned_data)

    # Return the predicted salary to the client
    # return jsonify(result=predicted_salary)
    return jsonify(result=predicted_salary)


if __name__ == '__main__':
    app.run(debug=False)
