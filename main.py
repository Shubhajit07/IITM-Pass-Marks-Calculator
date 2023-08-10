from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def marks_required(quiz1:float,quiz2:float):
    weighted_quiz1 = 0.2 * quiz1
    weighted_quiz2 = 0.3 * quiz2
    total_weighted_marks = weighted_quiz1 + weighted_quiz2
    if quiz2 > quiz1:
        weighted_quiz2 = 0.2 * quiz2
    else:
        weighted_quiz1 = 0.2 * quiz1
    required_marks = 40 - total_weighted_marks
    return required_marks

@app.route('/',methods=['GET'])
def index():
    return render_template('calculator.html',data={'calculated':False})

@app.route('/calculate',methods=['GET'])
def calculate():
    name:str = request.args.get('name', 'Anonymous')
    try:
        quiz1 = float(request.args['quiz1'])
        quiz2 = float(request.args['quiz2'])
    except:
        return redirect('/')
    required_marks= marks_required(quiz1,quiz2)
    data = {
        'calculated' : True,
        'marks_required' : round(required_marks/4,2),
        'quiz1' : quiz1,
        'quiz2' : quiz2,
        'name' : name
    }
    return render_template('calculator.html',data=data)

if __name__=='__main__':
    app.run(debug=False)