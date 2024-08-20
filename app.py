from flask import render_template, make_response, request, url_for, flash, redirect, session, json, jsonify
from db_table import app
from forms import SignupForms, LoginForms, EmailCheck, ResetPassForms, Create_account, Create_pin, Check_account, Update_pin, Check_details, Add_money, Withdraw
from atm import Login, ATMBank
from db_table import User, Bank


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')



@app.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForms()
    if form.validate_on_submit():
        data = Login()
        success, message= data.check_user(request)
        if not success:
            flash(message, 'danger')
        
        else:
            response = make_response()
            response.set_cookie('email', data.email, max_age=3600)
            flash(message, 'success')

            next_url = request.args.get('next') or url_for('home')
            response.headers['Location'] = next_url
            response.status_code = 302

            return response

    return render_template('login.html', form = form)



@app.route('/logout')
def logout():
    if request.cookies.get('email') != None:
        response = make_response()
        response.set_cookie('email', '', expires=0)
        response.headers['Location'] = url_for('home')
        response.status_code = 302
        flash('Logged out succesfully', 'success')
        return response
    
    return render_template('home.html')



@app.route('/signup', methods = ['GET','POST'])
def sign_up():
    form = SignupForms()
    if form.validate_on_submit():
        data = Login()
        success, message = data.add(request)

        if not success:
            flash(message, 'danger')
        
        else:
            flash(message, 'success')
            response = make_response()
            response.set_cookie('email', data.email, max_age=3600)

            next_url = request.args.get('next') or url_for('home')
            response.headers['Location'] = next_url
            response.status_code = 302
            return response
    
    return render_template('sign_up.html', form = form)



@app.route('/forget_password', methods = ['GET','POST'])
def forget_password():
    form = EmailCheck()
    if form.validate_on_submit():
        data = Login()
        success, message, user_data = data.check_email(request)

        if not success:
            flash(message, 'danger')
        
        else:
            session['user_data'] = user_data
            return redirect(url_for('reset_password'))
    
    return render_template('check_email.html', form = form)



@app.route('/reset_password',methods = ['GET','POST'])
def reset_password():
    form = ResetPassForms()
    user_data = session.get('user_data')

    if not user_data:
        flash("Session expired or invalid request.", "danger")
        return redirect(url_for('forget_password'))
    
    if form.validate_on_submit():
        data = Login()
        success, message = data.reset_password(request, user_data['email'])

        if success:
            flash(message, 'success')
            session.pop('user_data', None)
            return redirect(url_for('login'))
        
        else:
            flash(message,'danger')

    return render_template('reset_password.html', form=form)



@app.route('/create_user',methods = ['GET','POST'])
def create_user():
    form = Create_account()
    email = request.cookies.get('email')
    if email is None:
        flash('Login required!', 'danger')
        return redirect(url_for('login', next = request.url))
    
    user = User.query.filter_by(email = email).first()

    if form.validate_on_submit():
        acc = ATMBank()
        success, message = acc.add_account(request, user.id)

        if not success:
            flash(message, 'danger')
        else:
            flash(message, 'success')
            return redirect(url_for('home'))
    
    return render_template('create_account.html', form = form)



@app.route('/check_account',methods = ['GET','POST'])
def check_account():
    form = Check_account()
    email = request.cookies.get('email')

    if email is None:
        flash('Login required!', 'danger')
        return redirect(url_for('login', next = request.url))
    
    if form.validate_on_submit():
        acc = ATMBank()
        success, message, user_data = acc.check_account(request)

        if not success:
            flash(message, 'danger')
        else:
            session['user_data'] = user_data
            action = request.args.get('action')

            if action == 'add_pin':
                return redirect(url_for('create_pin'))
            elif action == 'update_pin':
                return redirect(url_for('update_pin'))
            elif action == 'user_details':
                return redirect(url_for('user_details'))
            
    return render_template('check_account.html', form = form)



@app.route('/create_pin',methods = ['GET','POST'])
def create_pin():
    form = Create_pin()
    user_data = session.get('user_data')

    if not user_data:
        flash("Session expired or invalid request.", "danger")
        return redirect(url_for('home'))
    
    if form.validate_on_submit():
        acc = ATMBank()
        success, message = acc.create_pin(request, user_data['Account No'], user_data['ID'])

        if not success:
            flash(message, 'danger')

        else:
            session.pop('user_data', None)
            flash(message, 'success')
            return redirect(url_for('home'))

    return render_template('create_pin.html', form = form)



@app.route('/update_pin',methods = ['GET','POST'])
def update_pin():
    form = Update_pin()
    user_data = session.get('user_data')

    if not user_data:
        flash("Session expired or invalid request.", "danger")
        return redirect(url_for('home'))

    if form.validate_on_submit():
        acc = ATMBank()
        success, message = acc.update_pin(request, user_data['Account No'], user_data['ID'])

        if not success:
            flash(message, 'danger')
        
        else:
            session.pop('user_data', None)
            flash(message, 'success')
            return redirect(url_for('home'))
        
    return render_template('update_pin.html', form = form)



@app.route('/check_balance',methods = ['GET','POST'])
def check_balance():
    form = Check_details()

    if form.validate_on_submit():
        acc = ATMBank()
        success, message, balance = acc.check_balance(request)

        if not success:
            flash(message, 'danger')
        
        else:
            flash(f'Your balance is: {balance}', 'balance')

    return render_template('check_details.html', form=form, title = 'Check Balance')
    


@app.route('/checkdetails',methods = ['GET','POST'])
def checkdetails():
    form = Check_details()
    email = request.cookies.get('email')

    if email is None:
        flash('Login required!', 'danger')
        return redirect(url_for('login', next = request.url))
    
    if form.validate_on_submit():
        acc = ATMBank()
        success, message, pin_id = acc.check_details(request)

        if not success:
            flash(message, 'danger')

        else:
            session['id'] = pin_id
            action = request.args.get('action')

            if action == 'add_money':
                return redirect(url_for('add_amount'))
            elif action == 'withdraw':
                return redirect(url_for('withdraw'))
        
    return render_template('check_details.html', form = form,title = 'Check Details')



@app.route('/add_amount',methods = ['GET','POST'])
def add_amount():
    form = Add_money()
    pin_id = session.get('id')

    if form.validate_on_submit():
        acc = ATMBank()
        success, message = acc.add_money(request, pin_id)

        if not success:
            flash(message, 'danger')
        
        else:
            session.pop('user_data', None)
            flash(message, 'success')
            return redirect(url_for('home'))
        
    return render_template('amount.html', form = form, title = 'Add Money')



@app.route('/withdraw',methods = ['GET','POST'])
def withdraw():
    form = Withdraw()
    pin_id = session.get('id')

    if form.validate_on_submit():
        acc = ATMBank()
        success, message = acc.withdraw(request, pin_id)

        if not success:
            flash(message, 'danger')
        
        else:
            session.pop('user_data', None)
            flash(message, 'balance')
        
    return render_template('amount.html', form = form, title = 'Withdraw Money')



@app.route('/user_details',methods = ['GET'])
def user_details():
    user_data = session.get('user_data')
    
    if not user_data:
        flash("Session expired or invalid request.", "danger")
        return redirect(url_for('home'))
    
    new_data = {
        'Account No' : user_data['Account No'],
        'First Name': user_data['First Name'],
        'Last Name': user_data['Last Name']
    }
    
    session.pop('user_data', None)
    return render_template('user_details.html', data = new_data)
        

if __name__ == "__main__":
    app.run(debug=True, port = 0.0.0.0 port=8000)
