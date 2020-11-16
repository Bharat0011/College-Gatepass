from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from . models import hod_data
from student.models import stu_signup
import psycopg2
import datetime
from datetime import date
import os
from django.core.mail import send_mail
numalpha='abcdefghijklmnopqrstuvwxyz0123456789'
key=5


# Create your views here.
def index(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('/')
    else:
        auth.logout(request)
        return redirect('/')

#************************************************************************************************************************************

def about_us(request):
    if request.method == 'POST':
        return render(request,'about_us.html') 
    else:
        return render(request,'about_us.html')

#************************************************************************************************************************************

def hod_login(request):
    if request.method == 'POST':
        username=request.POST.get("username")
        password=request.POST.get("password")
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")
        
        cur=con.cursor()
        if username is not None:
            cur.execute("select username,password from hod_hod_data where username='"+ username +"'")
            rows=cur.fetchall()
            if rows==[]:
                messages.info(request,'User not exists!')
                return redirect("hod_login")
            else:
                for r in rows:
                    if r[0]==username and r[1]==password :
                        print(r)
                        con.close()
                        user=auth.authenticate(username=username,password=password)
                        print(user)
                        if user is not None:
                            auth.login(request, user)
                            return redirect("hod_accept")
                        else:
                            return redirect("hod_login")
                    else:         
                        print("out")
                        print(r)
                        messages.info(request,'Username or Password not matched!')
                        con.close()
                        return redirect("hod_login")
        else:
            return render(request,'hod_login.html')
        
        return render(request,'hod_login.html')
        
    else:
        return render(request,'hod_login.html')

    





#************************************************************************************************************************************
@login_required(login_url='../hod/hod_login')
def hod_accept(request):
    if request.method=='POST':
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()
        gen=request.POST.get('verify')
        per=request.POST.get('Submit')
        username=request.user.username
        print("HEllo")
        per , req_type = per.split(':',1)
        print(per)
        print(gen)
        
        date=str(datetime.datetime.now())
        today_date = str(datetime.date.today())
        print(date)
        print(today_date)
        # ,req_accept_time='"+date+"'
        if per is not None:
            if gen == 'accept':
                print("test")
                cur.execute("update student_in_req set status='accepted',req_accept_time='"+date+"',req_acceped_by='"+username+"' where username='"+per+"' and request_type='"+req_type+"' and req_date='"+today_date+"' and status!='IN' and status!='OUT'")
                # cur.execute("update student_in_req set req_accept_time='"+date+"' where username='"+per+"'")  
                con.commit()
                print("commited accept")
            else:
                cur.execute("update student_in_req set status='hod_rejected',req_accept_time='"+date+"',req_acceped_by='"+username+"' where username='"+per+"' and request_type='"+req_type+"' and req_date='"+today_date+"' and status!='IN' and status!='OUT'")
                # cur.execute("update student_in_req set req_accept_time='"+date+"' where username='"+per+"'")
                con.commit()
        con.close()
        return redirect('hod_accept')
        # return render(request,'hod_accept.html')
    else:
        print('Retriving records/data')
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")
        print('In hod home'+str(datetime.date.today()))
        # username=request.user.username
        # print(username)

        today_date = str(datetime.date.today())
        cur=con.cursor()
        cur.execute(f"select username,gmail,request_type,mobile_no,reason_des,apply_time,first_name,last_name from student_in_req where (status='Pending' or status='gfm_accepted') and req_date='{today_date}'")
        rows=cur.fetchall()
    
        print(rows)
        
        for i in range(0, len(rows)):
            print("///////////")
            rows[i] = rows[i] + (stu_signup.objects.get(username=rows[i][0]).user_img, ) 
          
        return render(request,'hod_accept.html',{'data':rows})



#************************************************************************************************************************************

@login_required(login_url='../hod/hod_login')
def hod_rejected_stu_application(request):
    if request.method=='POST':
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()
        gen=request.POST.get('verify')
        per=request.POST.get('Submit')
        username=request.user.username
        per , req_type = per.split(':',1)
        print("HEllo")
        print(per)
        print(gen)
        
        date=str(datetime.datetime.now())
        today_date = str(datetime.date.today())
        print(date)
        print(today_date)
        # ,req_accept_time='"+date+"'
        if per is not None:
            if gen == 'accept':
                print("test")
                cur.execute("update student_in_req set status='accepted',req_accept_time='"+date+"',req_acceped_by='"+username+"' where username='"+per+"'and request_type='"+req_type+"' and req_date='"+today_date+"' and status!='IN' and status!='OUT'")
                # cur.execute("update student_in_req set req_accept_time='"+date+"' where username='"+per+"'")  
                con.commit()
                print("commited accept")
            else:
                cur.execute("update student_in_req set status='hod_rejected',req_accept_time='"+date+"',req_acceped_by='"+username+"' where username='"+per+"'and request_type='"+req_type+"' and req_date='"+today_date+"' and status!='IN' and status!='OUT'")
                # cur.execute("update student_in_req set req_accept_time='"+date+"' where username='"+per+"'")
                con.commit()
        con.close()
        return redirect('hod_rejected_stu_application')
    else:
        print('Retriving records/data')
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")
        print('In hod home'+str(datetime.date.today()))
        # username=request.user.username
        # print(username)

        today_date = str(datetime.date.today())
        cur=con.cursor()
        cur.execute(f"select username,gmail,request_type,mobile_no,reason_des,apply_time,first_name,last_name from student_in_req where status='gfm_rejected' and req_date='{today_date}'")
        rows=cur.fetchall()
    
        print(rows)
        
        for i in range(0, len(rows)):
            print("///////////")
            rows[i] = rows[i] + (stu_signup.objects.get(username=rows[i][0]).user_img, ) 
          
        return render(request,'hod_rejected_stu_application.html',{'data':rows})




#************************************************************************************************************************************
@login_required(login_url='../hod/hod_login')
def hod_validate_gfm(request):
    if request.method=='POST':

        con=psycopg2.connect(
        host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()
        gen=request.POST.get('verify')
        per=request.POST.get('Submit')
        print("HEllo")
        print(per)
        print(gen)

        if per is not None:
            if gen == 'accept':
                cur.execute("update gfm_gfm_signup set valid='accepted' where email='"+per+"'")
                con.commit()
            else:
                cur.execute("update gfm_gfm_signup set valid='rejected' where email='"+per+"'")
                con.commit()
        con.close()
        return redirect('hod_validate_gfm')
    else:
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()
        cur.execute("select first_name,mobile_no,email,icard_no,last_name from gfm_gfm_signup where valid='Pending'")
        rows=cur.fetchall()

        # for generating  id number e.g 1,2,3,4 depend on rows
        new_row = list(rows)
        for i in range (0, len(rows)):
            new_row[i] = (i+1,) + new_row[i]

        if rows is not None:
            print(rows) 
            con.close()
            return render(request,'hod_validate_gfm.html',{'data':new_row})
        else:
            # return redirect('apply')
            return render(request,'hod_validate_gfm.html')

#************************************************************************************************************************************

def hod_stu_report(request):
    if request.method=='POST':    
        date_from=request.POST.get('date_from')
        date_to=request.POST.get('date_to')
        print('///////////////')
        print(date_from,date_to)

        if date_from=='' and date_to =='':
            messages.info(request,'Plz enter the dates')
            return render(request,'hod_stu_report.html')

        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()
        cur.execute("select username,mobile_no,gmail,reason,reason_des,req_date,status,first_name,last_name from student_in_req where req_date >= '"+ date_from+"' and req_date <= '"+date_to+"' and (status='IN' or status='OUT')")
        rows=cur.fetchall()
        print(rows)

        new_row = list(rows)
        for i in range (0, len(rows)):
            new_row[i] = (i+1,) + new_row[i]

        if rows is not None:
            print(rows) 
            con.close()
            return render(request,'hod_stu_report.html',{'data':new_row})
        else:
            return render(request,'hod_stu_report.html')
    else:
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()
        cur.execute("select username,mobile_no,gmail,reason_des,req_acceped_by,req_date,status,first_name,last_name from student_in_req where status='accepted' or status='IN' or status='OUT'")
        rows=cur.fetchall()

        new_row = list(rows)
        for i in range (0, len(rows)):
            new_row[i] = (i+1,) + new_row[i]

        if rows is not None:
            print(rows) 
            con.close()
            return render(request,'hod_stu_report.html',{'data':new_row})
        else:
            # return redirect('apply')
            return render(request,'hod_stu_report.html')

#************************************************************************************************************************************


def forget_pass1h(request):
    if request.method == 'POST':
        email=request.POST.get("email")
        mobile_no=request.POST.get("mobile_no")
        print(email,mobile_no)

        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()
        cur.execute("select email,mobile_no from hod_hod_data where email='" + email + "' and mobile_no="+mobile_no+"")
        rows=cur.fetchall()
        con.close()
        print(rows)
        if not rows ==[]:
            for r in rows:
                    if email == r[0] and int(mobile_no)==r[1]:
                        return redirect('forget_pass2h')
                    else:
                        messages.info(request,'Email id and mobile number did not match!!!!!!!!')
                        return render(request,'forget_pass1.html')
        # else:
        #     messages.info(request,'Email id and mobile number didn''t match ')
        #     return render(request,'forget_pass1.html')
    else:
        return render(request,'forget_pass1.html')
    

#************************************************************************************************************************************




def forget_pass2h(request):
    print('lol')
    if request.method == 'POST':
        email=request.POST.get("email")
        password1=request.POST.get("password1")
        password2=request.POST.get("password2")
        
        print(email,password1,password2)
        
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()
        
        print(len(password1),len(password2))
        
        if len(password1) == len(password2) and password1 == password2:
            print('inside update')
            # encrypt=''
            # for i in password1:
	        #     pos=numalpha.find(i)
	        #     newpos=(pos+key)%36
	        #     encrypt=encrypt+numalpha[newpos]
            #saving pass in auth_user
            u = User.objects.get(email=''+email+'')
            u.set_password(''+password1+'')
            u.save()

            print('//////////////  changed pass in AUTH-USER //////////////')
            print(u)

            cur.execute("update hod_hod_data set password='"+ password1 +"' where email='"+email+"'")
            con.commit()
            con.close()
            return redirect('hod_home')
        else:
            messages.info(request,'password and confirm password did not match')
            return redirect('forget_pass2h')
    else:
        return render(request,'forget_pass2.html')    
#************************************************************************************************************************************

@login_required(login_url='../hod/hod_login')
def hod_home(request):
    return render(request,'hod_home.html')





#************************************************************************************************************************************
def logout(request):
    auth.logout(request)
    return redirect('hod_login')