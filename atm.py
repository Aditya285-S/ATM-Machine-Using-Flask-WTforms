from db_table import User, db, Bank, ATM

class Login:
    def __init__(self):
        self.name = None
        self.email = None
        self.password = None
        self.new_password = None
        self.confirm_password = None



    def add(self, request):
        self.name = request.form.get('name')
        self.email = request.form.get('email')
        self.password = request.form.get('password')

        existing_user = User.query.filter_by(email=self.email).first()
        if existing_user:
            return False, "Email already registered!"
        
        
        data = User(name=self.name, email=self.email, password=self.password)
        db.session.add(data)
        db.session.commit()
        return True, 'Account created succesfully'



    def check_user(self, request):
        self.email = request.form.get('email')
        self.password = request.form.get('password')

        existing_user = User.query.filter_by(email = self.email).first()
        if existing_user:
            if existing_user.password == self.password:
                return True, "Successfully logged in"

            else:
                return False, 'Incorrect Password!'
        
        return False, 'Account is not created!'
    


    def check_email(self, request):
        self.email = request.form.get('email')

        existing_user = User.query.filter_by(email = self.email).first()
        if existing_user:
            user_data = {
                "email": existing_user.email,
            }
            return True, "Valid email", user_data
        
        return False, 'Account is not created!', None



    def reset_password(self, request, email):
        self.new_password = request.form.get('new_password')

        user = User.query.filter_by(email=email).first()

        if user:
            user.password = self.new_password
            db.session.add(user)
            db.session.commit()
            return True, "Password has been updated successfully!"
    
        return False, "Account not found."




class ATMBank:
    def __init__(self):
        self.lname = None
        self.fname = None
        self.account_number = None
        self.balance = 0
        self.pin = None
        self.id = None
        self.new_pin = None



    def add_account(self,request, id):
        self.fname = request.form.get('f_name')
        self.lname = request.form.get('l_name')
        self.account_number = request.form.get('Account_number')
        self.id = id

        existing_acc = Bank.query.filter_by(account_number = self.account_number).first()
        if existing_acc:
            return False, 'Bank account number already Existed!'
        
        new_account = Bank(fname=self.fname, lname=self.lname, account_number=self.account_number, user_id=self.id)
        db.session.add(new_account)
        db.session.commit()
        return True, 'Bank account succesfully created'
    


    def check_account(self, request):
        self.account_number = request.form.get('Account_number')

        existing_acc = Bank.query.filter_by(account_number = self.account_number).first()

        if existing_acc:
            user_data = {
                'acc_number': existing_acc.account_number,
                'pin' : existing_acc.acc_id,
                'fname': existing_acc.fname,
                'lname': existing_acc.lname
            }
            return True, 'Bank account number Existed', user_data
        
        return False, 'Bank account is not created!', None
    


    def create_pin(self, request, account, pin_id):
        self.pin = request.form.get('pin')
        self.balance = request.form.get('balance')

        if self.balance == '':
            self.balance = 0

        existing_acc = Bank.query.filter_by(account_number = account).first()

        if existing_acc != None:
            atm = ATM.query.filter_by(pin_id = pin_id).first()

            if atm == None:
                data = ATM(pin = self.pin, balance = self.balance, pin_id = pin_id)
                db.session.add(data)
                db.session.commit()
                return True, 'Pin created succesfully'
            
            else:
                return False, 'Pin already created!'

        return False, 'Account is not created!'
    


    def update_pin(self, request, account, pin_id):
        self.new_pin = request.form.get('new_pin')

        existing_acc = Bank.query.filter_by(account_number = account).first()

        if existing_acc != None:
            atm = ATM.query.filter_by(pin_id = pin_id).first()

            if atm != None:

                if int(atm.pin) == int(self.new_pin):
                    return False, 'New Pin should be different!'
                
                else:
                    atm.pin = self.new_pin
                    db.session.add(atm)
                    db.session.commit()
                    return True, 'Pin updated succesfully'
                
            return False, 'Pin is not created!'
                
        return False, 'Account is not created!'
    


    def check_balance(self, request):
        self.account_number = request.form.get('Account_number')
        self.pin = request.form.get('pin')

        existing_acc = Bank.query.filter_by(account_number = self.account_number).first()

        if existing_acc != None:
            atm = ATM.query.filter_by(pin_id = existing_acc.acc_id).first()

            if atm != None:
                if int(atm.pin) == int(self.pin):
                    self.balance = atm.balance
                    return True, "Balance fetched successfully", self.balance
                else:
                    return False, "Invalid PIN", None
            else:
                return False, "PIN is not created", None

        return False, "Account not found", None
    


    def check_details(self, request):
        self.account_number = request.form.get('Account_number')
        self.pin = request.form.get('pin')

        existing_acc = Bank.query.filter_by(account_number = self.account_number).first()

        if existing_acc != None:
            atm = ATM.query.filter_by(pin_id = existing_acc.acc_id).first()

            if atm != None:
                if int(atm.pin) == int(self.pin):
                    self.id = atm.pin_id
                    return True, "Balance fetched successfully", self.id
                else:
                    return False, "Invalid PIN", None
            else:
                return False, "PIN is not created", None

        return False, "Account not found", None
    


    def add_money(self, request, pin_id):
        self.balance = request.form.get('amount')

        atm = ATM.query.filter_by(pin_id = pin_id).first()

        if atm != None:
            atm.balance = atm.balance + int(self.balance)
            db.session.add(atm)
            db.session.commit()
            return True, 'Amount deposited to account'
        
        return False, 'User not found!'
    


    def withdraw(self, request, pin_id):
        self.balance = request.form.get('amount')
        self.balance = int(self.balance)

        atm = ATM.query.filter_by(pin_id = pin_id).first()

        if atm != None:
            if self.balance < 0:
                return False, 'Amount cannot be Negative!'
            elif self.balance > atm.balance:
                return False, 'Insufficient balance!'
            else:
                atm.balance = atm.balance - self.balance
                db.session.add(atm)
                db.session.commit()
                return True, f'{self.balance} amount is credited'
        
        return False, 'User not found!'
