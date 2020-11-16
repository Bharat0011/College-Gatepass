from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from . models import gfm_signup
from student.models import stu_signup
import psycopg2
import datetime
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

def gfm_login(request):
    if request.method=='POST':
        gfm_email=request.POST.get('username')
        password=request.POST.get('password')

        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()

        cur.execute("select valid from gfm_gfm_signup where email='"+ gfm_email +"'")
        valid=cur.fetchall()
        
        if (any('Pending' in i for i in valid)):
            print('Pending')
            messages.info(request,'Plz contact HOD sir for validating your account')
            return redirect('gfm_login')
        else:
            if gfm_email is not None:
                cur.execute("select email,password from gfm_gfm_signup where email='"+ gfm_email +"'")
                rows=cur.fetchall()
                if rows==[]:
                    messages.info(request,'User not exists!')
                    return redirect("gfm_login")
                else:
                    for r in rows:
                        decrypt=''
                        pas=r[1]
                        for i in pas:
	                        posi=numalpha.find(i)
	                        newposi=(posi-key)%36
	                        decrypt=decrypt+numalpha[newposi]

                        if r[0]==gfm_email and decrypt==password :
                            print(r)
                            con.close()
                            user=auth.authenticate(username=gfm_email,password=password)
                            print(user)
                            if user is not None:
                                auth.login(request, user)
                                return redirect("gfm_validate_stu")
                            else:
                                return redirect("gfm_login")
                        else:         
                            print("out")
                            print(r)
                            messages.info(request,'Username or Password not matched!')
                            con.close()
                            return redirect("gfm_login")
            else:
                return render(request,'gfm_login.html')
            print(rows)
            con.close()
       
            print('approved')
            return redirect('gfm_validate_stu')
    else:
        return render(request,'gfm_login.html')

#************************************************************************************************************************************

def gfm_signup_form(request):
    if request.method=='POST':
        # gfm=request.POST.get('gfm')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        mobile_no=request.POST.get('mobile_no')
        icard_no=request.POST.get('icard_no')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')

        # if User.objects.filter(username=gfm).exists():
        #     messages.info(request,'User name taken')
        #     return redirect('gfm_signup_form')
        if User.objects.filter(email=email).exists():
            messages.info(request,'Email id already in use')
            return redirect('gfm_signup_form')
        elif password1!=password2:
            messages.info(request,'Password did not match')
            return redirect('gfm_signup_form')
        else:
            encrypt=''
            for i in password1:
	            pos=numalpha.find(i)
	            newpos=(pos+key)%36
	            encrypt=encrypt+numalpha[newpos]
            user= gfm_signup(gfm=email,first_name=first_name,last_name=last_name,password=encrypt,email=email,mobile_no=mobile_no,icard_no=icard_no,valid='Pending')
            user.save()
            # Authentication mate django user create kido
            user= User.objects.create_user(username=email,password=password1,email=email,first_name=first_name,last_name=last_name)
            user.save()
            print('registered')
            return redirect("gfm_login")
        return redirect('gfm_login')

    else:
        return render(request,'gfm_signup_form.html')
#************************************************************************************************************************************


def gfm_home(request):
    return render(request,'gfm_home.html')


#************************************************************************************************************************************
@login_required(login_url='../gfm/gfm_login')
def gfm_rejected_stu(request):
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
                cur.execute("update student_stu_signup set valid='accepted' where username='"+per+"'")
                con.commit()
            else:
                cur.execute("update student_stu_signup set valid='rejected' where username='"+per+"'")
                con.commit()
        con.close()
        return redirect('gfm_rejected_stu')
    else:
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        username=request.user.username
        print("/////////////////////////////")
        print(username)
        cur=con.cursor()
        cur.execute("select id,first_name,last_name,mobile_no,year,roll_no,gfm,username from student_stu_signup where valid='rejected' and gfm='"+username+"'")
        rows=cur.fetchall()
        if rows is not None:
            print(rows) 
            con.close()
            return render(request,'gfm_rejected_stu.html',{'data':rows})
        else:
            # return redirect('apply')
            return render(request,'gfm_rejected_stu.html')



#************************************************************************************************************************************
@login_required(login_url='../gfm/gfm_login')
def gfm_grant_permission(request):
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
        per , req_type = per.split(':',1)
        print(per,req_type)
        print(gen)
        username=request.user.username
        date=str(datetime.datetime.now())
        today_date = str(datetime.date.today())
        print(date)
        print(today_date)

        if per is not None:
            if gen == 'accept':
                # cur.execute("update student_in_req set status='accepted',req_accept_time = '"+ dt_string +"' where username='"+per+"'")
                cur.execute("update student_in_req set status='gfm_accepted',req_accept_time='"+date+"',req_acceped_by='"+username+"' where username='"+per+"'and req_date='"+today_date+"' and request_type='"+req_type+"' and status!='IN' and status!='OUT'")
                con.commit()
            else:
                # cur.execute("update student_in_req set status='rejected',req_accept_time='"+dt_string+"' where username='"+per+"'")
                cur.execute("update student_in_req set status='gfm_rejected',req_accept_time='"+date+"' ,req_acceped_by='"+username+"' where username='"+per+"'and req_date='"+today_date+"' and request_type='"+req_type+"' and status!='IN' and status!='OUT'")
                con.commit()
        con.close()
        return redirect('gfm_grant_permission')

        # return render(request,'gfm_grant_permission.html')
    else:
        print('Retriving records/data')
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")
        print('In hod home')
        # username=request.user.username
        # print(username)
        today_date = str(datetime.date.today())
        cur=con.cursor()
        cur.execute(f"select username,gmail,request_type,mobile_no,reason_des,apply_time,first_name,last_name from student_in_req where status='Pending' and req_date='{today_date}'")
        rows=cur.fetchall()
    
        print(rows)
        
        for i in range(0, len(rows)):
            print("///////////")
            rows[i] = rows[i] + (stu_signup.objects.get(username=rows[i][0]).user_img, ) 
          
        return render(request,'gfm_grant_permission.html',{'data':rows})
       





#************************************************************************************************************************************
@login_required(login_url='../gfm/gfm_login')
def gfm_validate_stu(request):
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
                cur.execute("update student_stu_signup set valid='accepted' where username='"+per+"'")
                con.commit()
            else:
                cur.execute("update student_stu_signup set valid='rejected' where username='"+per+"'")
                con.commit()
        con.close()
        return redirect('gfm_validate_stu')
    else:
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        username=request.user.username
        cur=con.cursor()
        cur.execute("select first_name,last_name,mobile_no,year,roll_no,gfm,username from student_stu_signup where valid='Pending' and gfm='"+username+"'")
        rows=cur.fetchall()

        new_row = list(rows)
        
        for i in range (0, len(rows)):
            new_row[i] = (i+1,) + new_row[i]
        if rows is not None:
            print(rows) 
            con.close()
            return render(request,'gfm_validate_stu.html',{'data':new_row})
        else:
            # return redirect('apply')
            return render(request,'gfm_validate_stu.html')


    # return render(request,'gfm_validate_stu.html')



#************************************************************************************************************************************

@login_required(login_url='../gfm/gfm_login')
def gfm_stu_report(request):
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

        username=request.user.username
        cur.execute("SELECT username from student_stu_signup where gfm='"+username+"'")
        r1 = cur.fetchall()
        print(r1)

        rows =[]
        for r in r1:
            print(r[0])
            cur.execute("select username,mobile_no,gmail,reason,reason_des,req_date,status,first_name,last_name from student_in_req where username= '"+r[0]+"' and req_date >= '"+ date_from+"' and req_date <= '"+date_to+"' and (status='IN' or status='OUT')")
            rows.append(cur.fetchall())

        new_row=[]
        for i in range (0, len(rows)):
            if len(rows[i]) == 0:
                print("null list")
            else:
                new_row.append(rows[i])
                print(len(rows[i]))
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        flat_list = [item for sublist in new_row for item in sublist]
        for i in range(len(flat_list)):
            flat_list[i] = (i+1, ) + flat_list[i]
        print(flat_list)
        if rows is not None:
            print(rows) 
            con.close()
            return render(request,'gfm_stu_report.html',{'data':flat_list})
        else:
            return render(request,'gfm_stu_report.html')
    else:
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")
        cur=con.cursor()

        username=request.user.username
        cur.execute("SELECT username from student_stu_signup where gfm='"+username+"'")
        r1 = cur.fetchall()
        print(r1)
        rows =[]
        for r in r1:
            print(r[0])
            cur.execute(f"select username,mobile_no,gmail,reason_des,req_acceped_by,req_date,status,first_name,last_name from student_in_req where username='{r[0]}' and (status='accepted' or status='IN' or status='OUT')")
            rows.append(cur.fetchall())

        print(rows)
        new_row=[]
        for i in range (0, len(rows)):
            if len(rows[i]) == 0:
                print("null list")
            else:
                new_row.append(rows[i])
                print(len(rows[i]))
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        flat_list = [item for sublist in new_row for item in sublist]
        for i in range(len(flat_list)):
            flat_list[i] = (i+1, ) + flat_list[i]
        print(flat_list)
        if rows is not None:
            print(rows) 
            con.close()
            return render(request,'gfm_stu_report.html',{'data':flat_list})
            # return render(request,'gfm_stu_report.html',{'data':rows})
        else:
            # return redirect('apply')
            return render(request,'gfm_stu_report.html')



#************************************************************************************************************************************

@login_required(login_url='../gfm/gfm_login')
def gfm_stu_profile(request):
    if request.method=='POST':
        username = request.POST.get('Submit')
        print(username)
        request.session['edit_prof_username'] = username
        return redirect('edit_myprof')
    else:
        username=request.user.username

        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()
        # SE,TE,BE DATA
        cur.execute(f"select first_name,last_name,roll_no,username from student_stu_signup where gfm='{username}' and (year='BE' or year='TE' or year='SE') and valid='accepted'")
        be = cur.fetchall()
        print(be)
        new_be = list(be)
        
        for i in range (0, len(be)):
            new_be[i] = (i+1,) + new_be[i]



        return render(request,'gfm_stu_profile.html',{'be':new_be})



#************************************************************************************************************************************


@login_required(login_url='../gfm/gfm_login')
def edit_myprof(request):
    if request.method=='POST':
        user = request.session['edit_prof_username']
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        mobile_no = request.POST.get('mobile_no')
        year = request.POST.get('year')
        branch = request.POST.get('branch')
        roll_no = request.POST.get('roll_no')
        gfm = request.POST.get('gfm')
        

        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")
        cur=con.cursor()
        cur.execute(f"update student_stu_signup set username='{username}',first_name='{first_name}',last_name='{last_name}',gender='{gender}',email='{email}',mobile_no='{int(mobile_no)}',year='{year}',branch='{branch}',roll_no='{int(roll_no)}',gfm='{gfm}' where username='{user}'")
        con.commit()

        cur.execute(f"update auth_user set username='{username}',first_name='{first_name}',last_name='{last_name}' where username='{user}'")
        con.commit()



        return redirect('gfm_stu_profile')
    else:
        user = request.session['edit_prof_username']
        print("in edit prof")
        print(user)

        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")
        cur=con.cursor()

        cur.execute(f"select user_img,icard_img,username,first_name,last_name,year,branch,gender,roll_no,email,mobile_no,gfm from student_stu_signup where username='{user}' and valid='accepted' and email_verify='accepted'")
        rows = cur.fetchall()
        cgfm = ''
        for r in rows:
            cgfm=r[11]
        cur.execute(f"select first_name,last_name from gfm_gfm_signup where gfm='{cgfm}'")
        cgfmd=cur.fetchone()
        cur.execute("select gfm,first_name,last_name from gfm_gfm_signup where valid='accepted'")
        gfm = cur.fetchall()

        cur.execute(f"select user_img,icard_img from student_stu_signup where username='{user}' and valid='accepted' and email_verify='accepted'")
        image = cur.fetchall()


        return render(request,'edit_myprof.html',{'data':rows,'gfm':gfm,'curr_gfm':cgfmd,'img':image})




#************************************************************************************************************************************


def forget_pass1(request):
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
        cur.execute("select email,mobile_no,valid from gfm_gfm_signup where email='" + email + "' and mobile_no="+mobile_no+"")
        rows=cur.fetchall()
        con.close()
        print(rows)
        if not rows ==[]:
            for r in rows:
                if not r[2]=='rejected':
                    print(r[1])
                    if email == r[0] and int(mobile_no)==r[1]:
                        return redirect('forget_pass')
                    else:
                        messages.info(request,'Email id and mobile number did not match!!!!!!!! ')
                        return render(request,'forget_pass1.html')
                else :
                    messages.info(request,'Your account has been rejected')
                    return render(request,'forget_pass1.html')
        else:
            return redirect('forget_pass1')
    else:
        return render(request,'forget_pass1.html')
    


#************************************************************************************************************************************




def forget_pass(request):
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
            encrypt=''
            for i in password1:
	            pos=numalpha.find(i)
	            newpos=(pos+key)%36
	            encrypt=encrypt+numalpha[newpos]

            u = User.objects.get(email=''+email+'')
            u.set_password(''+password1+'')
            u.save()
            
            cur.execute("update gfm_gfm_signup set password='"+ encrypt +"' where email='"+email+"'")
            con.commit()

            con.close()
            return redirect('gfm_login')
        else:
            messages.info(request,'password and confirm password did not match')
            return redirect('forget_pass2')
    else:
        return render(request,'forget_pass2.html')


#************************************************************************************************************************************
def logout(request):
    auth.logout(request)
    return redirect('/')