from flask import Flask, render_template, request, redirect
import os
from deta import Deta

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
    return round(required_marks/0.4,2)

def new_view():
    project_key = os.environ.get('DETA_PROJECT_KEY')
    if project_key is not None:
        deta = Deta(project_key)
        base = deta.Base('visitors')
        visitors = base.get('visitor_count')
        count = 0
        if type(visitors) is dict:
            count = visitors['value'] + 1
            base.put(count,key='visitor_count')
        else:
            count+=1
            base.put(count,key='visitor_count')
        return count
    else:
        return 0

@app.route('/',methods=['GET'])
def index():
    count = new_view()
    return render_template('calculator.html',data={'calculated':False, 'visitor_count': count})

@app.route('/calculate',methods=['GET'])
def calculate():
    count = new_view()
    name = request.args.get('name', 'Anonymous')
    try:
        quiz1 = float(request.args['quiz1'])
        quiz2 = float(request.args['quiz2'])
    except:
        return redirect('/')
    required_marks= marks_required(quiz1,quiz2)
    data = {
        'calculated' : True,
        'marks_required' : required_marks,
        'quiz1' : quiz1,
        'quiz2' : quiz2,
        'name' : name,
        'visitor_count' : count
    }
    return render_template('calculator.html',data=data)

if __name__=='__main__':
    app.run(debug=False,port=os.environ.get('PORT',5000))