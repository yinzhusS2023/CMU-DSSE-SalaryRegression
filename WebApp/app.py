from flask import Flask, render_template, request

# from kejie import kejie_program_function
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form_data = {}
        form_data['sponsored_or_not'] = request.form['sponsored_or_not']
        form_data['in_US_or_not'] = request.form['in_US_or_not']
        form_data['company_size'] = request.form['company_size']
        form_data['company_industry'] = request.form['company_industry']
        form_data['company_type'] = request.form['company_type']
        form_data['employee_benefits'] = request.form['employee_benefits']
        form_data['employee_rating_benefits'] = request.form['employee_rating_benefits']
        form_data['ceo_approval_rating'] = request.form['ceo_approval_rating']
        form_data['recommend_to_friend_rating'] = request.form['recommend_to_friend_rating']
        form_data['company_overall_rating'] = request.form['company_overall_rating']
        form_data['job_level'] = request.form['job_level']
        form_data['job_category'] = request.form['job_category']
        form_data['reviews_pro'] = request.form['reviews_pro']
        form_data['reviews_con'] = request.form['reviews_con']
        form_data['job_description'] = request.form['job_description']

        print(form_data)
        return render_template('index.html', result=None)

    return render_template('index.html', result=None)


if __name__ == '__main__':
    app.run(debug=False)
