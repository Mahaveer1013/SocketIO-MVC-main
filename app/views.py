from flask import render_template, request, flash, redirect, url_for,jsonify
from app import app, db, socketio
from app.models import user,employee, late, leave,notification
#from flask_login import login_user, login_required, logout_user, current_user
import json
from sqlalchemy.sql import func
from flask_socketio import emit
from sqlalchemy import desc
import os
# Your route handlers and SocketIO events go here
import pandas as pd
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/late_form_page')
def late_form_page():
    return render_template('emp_late.html')


@app.route('/leave_form_page')
def leave_form_page():
    return render_template('emp_leave.html')


@socketio.on('connect')
def handle_connect():
    print('Client Connected')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')    

@app.route('/late_approve',methods=['POST','GET'])
def late_approve():
    user = json.loads(request.data)
    userID = user['userId']
    user = late.query.filter_by(emp_id=userID).first()
    print(" USER : ",user)
    current_user='hr'
    if current_user=='hr':
        user.hr_approval='Approved'
        user.status='Approved'
        db.session.commit()
        emit('late_hr_approval_update', {'userId': userID, 'hr_approval': user.hr_approval}, broadcast=True)

@app.route('/leave_approve',methods=['POST','GET'])
def leave_approve():
    user = json.loads(request.data)
    userID = user['userId']
    user = leave.query.filter_by(emp_id=userID).first()
    print(" USER : ",user)
    current_user='hr'
    if current_user=='hr':
        user.hr_approval='Approved'
        user.status='Approved'
        db.session.commit()
        emit('leave_hr_approval_update', {'userId': userID, 'hr_approval': user.hr_approval}, broadcast=True)

@app.route('/late_decline',methods=['POST','GET'])
def late_decline():
    user = json.loads(request.data)
    userID = user['userId']
    user = late.query.filter_by(emp_id=userID).first()
    print(" USER : ",user)
    current_user='hr'
    if current_user=='hr':
        user.hr_approval='Declined'
        user.status='Declined'
        db.session.commit()
        emit('late_hr_approval_update', {'userId': userID, 'hr_approval': user.hr_approval}, broadcast=True)

@app.route('/leave_decline',methods=['POST','GET'])
def leave_decline():
    user = json.loads(request.data)
    userID = user['userId']
    user = leave.query.filter_by(emp_id=userID).first()
    print(" USER : ",user)
    current_user='hr'
    if current_user=='hr':
        user.hr_approval='Declined'
        user.status='Declined'
        db.session.commit()
        emit('leave_hr_approval_update', {'userId': userID, 'hr_approval': user.hr_approval}, broadcast=True)

@socketio.on('late')
def handle_lateform_callback(lateDet):
    emp_id=lateDet['emp_id']
    emp_name=lateDet['emp_name']
    reason=lateDet['reason']
    from_time=lateDet['from_time']
    to_time=lateDet['to_time']
    status='Pending'
    hod_approval='Pending'
    approved_by='Hod Name'
    hr_approval='Pending'
    try:
        new_request=late(emp_id=emp_id,emp_name=emp_name,reason=reason,from_time=from_time,to_time=to_time,status=status,hod_approval=hod_approval,approved_by=approved_by,hr_approval=hr_approval)
        db.session.add(new_request)
        db.session.commit()
        all_latedata = {'emp_id':emp_id, 'emp_name':emp_name, 'reason':reason, 'from_time':from_time, 'to_time':to_time, 'status':status, 'hod_approval':hod_approval, 'approved_by':approved_by, 'hr_approval':hr_approval}

        emit('late', all_latedata, broadcast=True)


    except Exception as e:
        print(f"An error occurred: {str(e)}")



@app.route('/request_disp')
def request_disp():
    late_permission=late.query.order_by(late.date).all()
    leave_permission=leave.query.order_by(leave.date).all()
    return render_template('request_disp.html',late_permission=late_permission,leave_permission=leave_permission)

@socketio.on('leave')
def handle_leaveform_callback(leaveDet):
    emp_id=leaveDet['emp_id']
    emp_name=leaveDet['emp_name']
    reason=leaveDet['reason']
    from_date=leaveDet['from_date']
    to_date=leaveDet['to_date']
    status='Pending'
    hod_approval='Pending'
    approved_by='Hod Name'
    hr_approval='Pending'
    try:
        new_request=leave(emp_id=emp_id,emp_name=emp_name,reason=reason,from_date=from_date,to_date=to_date,status=status,hod_approval=hod_approval,approved_by=approved_by,hr_approval=hr_approval)
        db.session.add(new_request)
        db.session.commit()
        all_leaveData={'emp_id':emp_id,'emp_name':emp_name,'reason':reason,'from_date':from_date,'to_date':to_date,'status':status,'hod_approval':hod_approval,'approved_by':approved_by,'hr_approval':hr_approval}
        emit('leave', all_leaveData, broadcast=True)


    except Exception as e:
        print(f"An error occurred: {str(e)}")


@app.route('/add_leave_notification', methods=['POST'])
def add_leave_notification():
    try:
        message = request.json['message']
        print(message)
        new_notification = notification(message=message)
        db.session.add(new_notification)
        db.session.commit()

        return jsonify({'message': 'Notification added successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@app.route('/add_late_notification', methods=['POST'])
def add_late_notification():
    try:
        message = request.json['message']
        print(message)
        new_notification = notification(message=message)
        db.session.add(new_notification)
        db.session.commit()

        return jsonify({'message': 'Notification added successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/del_db',methods=['POST','GET'])
def del_db():
    db.session.query(late).delete()
    db.session.query(leave).delete()
    db.session.commit()
    return redirect(url_for('request_disp'))



@app.route('/excel_data',methods=['POST','GET'])
def excel_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app.config['EXCEL_FOLDER'] = os.path.join(script_dir, 'static', 'excel')
    file_path = os.path.join(app.config['EXCEL_FOLDER'], 'shift- sep 2023.xlsx')
    data = []
    rows_to_skip=[1,11,22,23,30,31,32]
    if os.path.exists(file_path):
        sheet_names = pd.ExcelFile(file_path).sheet_names

        for sheet_name in sheet_names:
            df = None
            if file_path.lower().endswith('.xlsx'):
                df = pd.read_excel(file_path, sheet_name, engine='openpyxl', skiprows=1)
            elif file_path.lower().endswith('.xls'):
                df = pd.read_excel(file_path, sheet_name, engine='xlrd', skiprows=1)
            else:
                print("Unsupported file format")
                return "Unsupported file format"  # Handle unsupported format
            
            df=df[~df.index.isin(rows_to_skip)]
            df.to_excel('modified_excel_file.xlsx',index=False)

            for index, row in df.iterrows():
                if index > 0:  # Skip the first row (header)
                    shift_data = {
                        'E.ID': row[ 1 ],  # Access data in the 4th column
                        'NAME': row[ 2 ],
                        ' 1 ' : row[ 3 ],
                        ' 2 ' : row[ 4 ],
                        ' 3 ' : row[ 5 ],
                        ' 4 ' : row[ 6 ],
                        ' 5 ' : row[ 7 ],
                        ' 6 ' : row[ 8 ],
                        ' 7 ' : row[ 9 ],
                        ' 8 ' : row[ 10 ],
                        ' 9 ' : row[ 11 ],
                        ' 10 ' : row[ 12 ],
                        ' 11 ' : row[ 13 ],
                        ' 12 ' : row[ 14 ],
                        ' 13 ' : row[ 15 ],
                        ' 14 ' : row[ 16 ],
                        ' 15 ' : row[ 17 ],
                        ' 16 ' : row[ 18 ],
                        ' 17 ' : row[ 19 ],
                        ' 18 ' : row[ 20 ],
                        ' 19 ' : row[ 21 ],
                        ' 20 ' : row[ 22 ],
                        ' 21 ' : row[ 23 ],
                        ' 22 ' : row[ 24 ],
                        ' 23 ' : row[ 25 ],
                        ' 24 ' : row[ 26 ],
                        ' 25 ' : row[ 27 ],
                        ' 26 ' : row[ 28 ],
                        ' 27 ' : row[ 29 ],
                        ' 28 ' : row[ 30 ],
                        ' 29 ' : row[ 31 ],
                        ' 30 ' : row[ 32 ],
                        ' 31 ' : row[ 33 ],                            
                    }
                    data.append(shift_data)
                    try:
                        new_request=user(emp_id=row[1],name=row[2],one=row[3],two=row[4],three=row[5],four=row[6],five=row[7],six=row[8],seven=row[9],eight=row[10],nine=row[11],ten=row[12],eleven=row[13],twelve=row[14],thirteen=row[15],fourteen=row[16],fifteen=row[17],sixteen=row[18],seventeen=row[19],eighteen=row[20],nineteen=row[21],twenty=row[22],tw_one=row[23],tw_two=row[24],tw_three=row[25],tw_four=row[26],tw_five=row[27],tw_six=row[28],tw_seven=row[29],tw_eight=row[30],tw_nine=row[31],thirty=row[32],th_one=row[33])
                        db.session.add(new_request)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        flash("Error: " + str(e), "error")

                

    else:
        print("File not found")
        return "File not found"

    return render_template('excel_data.html', data=data)
