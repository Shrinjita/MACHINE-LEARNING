from flask import Flask, render_template, url_for, request
app= Flask(__name__)

#main rout
@app.route("/")
def main():
    return render_template("index.html")

@app.route("/simple")
def simple():
    return render_template("simple.html")

@app.route("/calculate",methods=["post"])
def calculate():
    first_number=request.form["firstnumber"]
    operation = request.form["operation"]
    second_number= request.form["secondnumber"]
    return operation

if __name__=="__main__":
    app.run(debug=True)