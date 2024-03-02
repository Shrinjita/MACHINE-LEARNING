from flask import Flask, render_template, request
app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/job')
def explore_jobs():
    return render_template('job.html')

@app.route('/job_details.html')
def job_details():
    job_title = request.args.get('job', default='', type=str)
    return render_template('job_details.html', job_title=job_title)

@app.route('/rec')
def find_talent():
    return render_template('rec.html')

@app.route('/job_posting.html')
def job_posting():
    return render_template('job_posting.html')

@app.route('/business_account.html')
def business_account():
    return render_template('business_account.html')

@app.route('/search_candidates.html')
def search_candidates():
    return render_template('search_candidates.html')

if __name__ == '__main__':
    app.run(debug=True)