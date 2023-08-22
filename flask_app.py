from flask import Flask, render_template, request
#import jinja2
app = Flask(__name__)

# Aggiungi jinja2.ext.do come estensione
#app.jinja_env.add_extension('jinja2.ext.do')
debug = 0
num_step = 1
score = []
level = []
comment = []
comments = []

#prefix = '/home/maxloria/mysite/config/'
prefix = '.\\config\\'
#prefix = '/app/config/'
quizzes_file = open(prefix + 'quizzes.txt', 'r')
quizzes = quizzes_file.readlines()
quizzes_file.close()

comments_file = open(prefix + 'comments.txt', 'r')
comments = comments_file.readlines()
comments_file.close()

@app.route("/")
def index():
    return render_template("index.html", quizzes=quizzes)

@app.route('/quiz/<int:quizID>', methods=['GET', 'POST'])
def quiz(quizID):
    global num_step
    global score
    global total_score
    global level
    questions = []
    opinions = []
    global comment

    if debug == 0:
        suff = '_complete'
    else:
        suff = '_short'

    category_file = open(prefix + 'categories' + str(quizID) + suff + '.txt', 'r')
    categories = category_file.readlines()
    category_file.close()

    if debug == 0:
        num_steps = len(categories)
    else:
        num_steps = 3

    for k in range(num_steps):
        questions_file = open(prefix + 'questions' + str(quizID) + '_' + str(k+1) + suff + '.txt', 'r')
        questions.append(questions_file.readlines())
        questions_file.close()

        opinions_file = open(prefix + 'opinions' + str(quizID) + '_' + str(k+1) + '.txt', 'r')
        opinions.append(opinions_file.readlines())
        opinions_file.close()

    if request.method == 'GET':
        # Carica il quiz
        return render_template('quiz.html', questions=questions[0], category=categories[0], quiz=quizzes[quizID-1])
    elif request.method == 'POST':
        # Calcola il punteggio del quiz
        single_score = 0
        if num_step == 1:
            score = []
            total_score = []
            level = []
            comment = []
            opinion = []
        for i in range(len(questions[num_step - 1])):
            single_score += int(request.form['question_'+str(i+1)])
        score.append(single_score)
        total_score.append(5 * len(questions[num_step - 1]))
        status_level = status(single_score,5 * len(questions[num_step - 1]))
        level.append(status_level)
        comment.append(comments[status_level])
        num_step += 1
        
        if num_step <= num_steps:
            return render_template('quiz.html', questions=questions[num_step-1], category=categories[num_step-1], quiz=quizzes[quizID-1])
        else:
            num_step = 1
            questions = []
            return render_template("result.html", numquiz=quizzes[quizID-1], score=score, total_score=total_score, \
                level=level, comment=comment, namequiz=quizzes[quizID-1], categories=categories, opinions=opinions)
            opinions = []
            
def status(score,total):
    if score/total < 0.3:
        return 0
    elif score/total < 0.5:
        return 1
    elif score/total < 0.7:
        return 2
    elif score/total < 0.9:
        return 3
    else:
        return 4

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)