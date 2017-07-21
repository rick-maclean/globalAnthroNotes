from flask import Flask, render_template, request
# create an object that is an instance of the flask framework
app = Flask(__name__)

# app routing: to trigger the function backend languages....???
# when the user goes to the url / it will run the index function
@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        age = request.form['agefrm']

        return render_template('age_t3.html', ageRender=age)

    return render_template('shaan3.html')

# we want to run the app
if __name__ == "__main__":
    app.run(debug=True)