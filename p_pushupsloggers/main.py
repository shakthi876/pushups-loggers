from locale import currency
from flask import Blueprint, flash, render_template, request, url_for,redirect
from flask_login import current_user, login_required
from . import db
from .models import Workout,User

main = Blueprint('main',__name__)



@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile/')
@login_required
def profile():
    print('current user id is',current_user.id)
    #Finding sum of workouts
    result_sum = Workout.query.with_entities(db.func.sum(Workout.pushups).label('sum')).filter(Workout.user_id ==current_user.id).first()
   


    #finding day which has maximum workouts
    result_max =  Workout.query.with_entities(db.func.max(Workout.pushups).label('sum')).filter(Workout.user_id ==current_user.id).first()
    string = str(result_max) #convert it to string
    new_string = ''.join(char for char in string if char.isalnum()) #removing special characters in string
   
    if new_string != 'None':
        print('haii')
        new_string = int(new_string) #convert it to integer to filter 

    result_max_date = Workout.query.filter_by(pushups =new_string).first()
    print('tst',result_max_date)
    if result_max_date is not None:
        result_max_date = result_max_date.date_posted

    #finding no of days did push-ups
    result_count = Workout.query.with_entities(db.func.count(Workout.pushups).label('sum')).filter(Workout.user_id ==current_user.id).first()
    print('result_count',result_count)

    return render_template('profile.html',name=current_user.name,result=result_sum,result2=result_max_date,max_day_count=new_string,result_count=result_count)


@main.route('/new/')
@login_required
def workout():
    return render_template('createworkout.html')

@main.route('/new/',methods=['POST'])
@login_required
def workout_post():
    pushups = request.form.get('pushups')
    comment = request.form.get('comment')

    workout = Workout(pushups=pushups,comment=comment,author=current_user)
    db.session.add(workout)
    db.session.commit()

    

    return redirect(url_for('main.user_workouts'))


@main.route('/all/')
@login_required
def user_workouts():
    page = request.args.get('page',1,type=int) # url/?page=1 to get the 1
    print('page is... ',page)
    user= User.query.filter_by(email=current_user.email).first_or_404()
    # workouts=user.workouts nd workouts=Workout.query.filter_by(author=user) are same

    workouts = Workout.query.filter_by(author=user).paginate(page=page,per_page=3)

    print(workouts.items)
    return render_template('allworkouts.html',workouts=workouts,user=user,page=page,per_page=3)


@main.route('/workout/<int:workout_id>/update',methods=['POST','GET'])
@login_required
def update_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    if request.method =='POST':
        workout.pushups = request.form['pushups']
        workout.comment = request.form['comment']
        db.session.commit()
        flash('updated successfully!!',"success")
        return redirect('/all')


    return render_template('updateworkout.html',workout=workout)


@main.route('/workout/<int:workout_id>/delete',methods=['POST','GET'])
@login_required
def delete_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    db.session.delete(workout)
    db.session.commit()
    flash('Deleted successfully!!',"success")
    return redirect('/all')


@main.route('/developer/')
def developer():
    return render_template('developer.html')