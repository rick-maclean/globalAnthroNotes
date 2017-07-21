from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def template_test():
    mystr = "wheeeee hoooouuuuu"
    return render_template('template.html', my_string=mystr, my_list=[0,1,2,3,4,5, 32])


if __name__ == '__main__':
    app.run(debug=True)