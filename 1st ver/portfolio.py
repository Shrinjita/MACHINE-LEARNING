from flask import Flask, render_template, send_file

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('port.html')

@app.route('/send-message', methods=['POST'])
def send_message():
    # Handle sending message here
    return 'Message sent successfully!'

@app.route('/download-resume')
def download_resume():
    resume_path = 'resume.pdf'
    return send_file(resume_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
