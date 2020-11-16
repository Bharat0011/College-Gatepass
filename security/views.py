from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from . models import security_data
from student.models import stu_signup
import psycopg2
import datetime

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


def security_login(request):
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
            cur.execute("select username,password from security_security_data where username='"+ username +"'")
            rows=cur.fetchall()
            if rows==[]:
                messages.info(request,'User not exists!')
                return redirect("security_login")
            else:
                for r in rows:
                    if r[0]==username and r[1]==password :
                        print(r)
                        con.close()
                        user=auth.authenticate(username=username,password=password)
                        print(user)
                        if user is not None:
                            auth.login(request, user)
                            return redirect("security_in")
                        else:
                            return redirect("security_login")
                    else:         
                        print("out")
                        print(r)
                        messages.info(request,'Username or Password not matched!')
                        con.close()
                        return redirect("security_login")
        else:
            return render(request,'security_login.html')
        
        return render(request,'security_in.html')
    else:
        # user=security_data(username=username,password=password)
        # user.save()
        # user1= User.objects.create_user(username=username,password=password)
        # user1.save()
        return render(request,'security_login.html')





#************************************************************************************************************************************
@login_required(login_url='../security/security_login')
def security_in(request):
    if request.method=='POST':
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()
        # gen=request.POST.get('verify')
        per=request.POST.get('Submit')
        print("HEllo")
        print(per)

        now=datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        if per is not None:
            cur.execute("update student_in_req set in_time = '"+ dt_string +"',status='IN' where username='"+per+"' and (status='accepted' or status='hod_accepted') and request_type='IN Request'")
            con.commit()
        con.close()

        return redirect('security_in')
    else:
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")
        print('In student home')
        username=request.user.username
        print(username)
        today_date = str(datetime.date.today())
        cur=con.cursor()
        cur.execute(f"select username , req_accept_time , status from student_in_req where (status='accepted' or status='rejected' or status='gfm_rejected' or status='hod_rejected' or status='hod_accepted') and request_type='IN Request' and req_date='{today_date}'")
        rows=cur.fetchall()
        
        # for generating  id number e.g 1,2,3,4 depend on rows
        new_row = list(rows)
        for i in range (0, len(rows)):
            new_row[i] = (i+1,) + new_row[i]

        for i in range(0, len(new_row)):
            print("///////////")
            new_row[i] = new_row[i] + (stu_signup.objects.get(username=new_row[i][1]).user_img, )

        for i in range(0, len(new_row)):
            print("///////////")
            new_row[i] = new_row[i] + (stu_signup.objects.get(username=new_row[i][1]).icard_img, )

        if rows is not None:
            # print(new_row) 
            con.close()
            return render(request,'security_in.html',{'data':new_row,})
        else:
            # return redirect('apply')
            return render(request,'security_in.html')


#************************************************************************************************************************************



@login_required(login_url='../security/security_login')
def security_out(request):
    if request.method=='POST':
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()
        # gen=request.POST.get('verify')
        per=request.POST.get('Submit')
        print("HEllo")
        print(per)

        now=datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        if per is not None:
            cur.execute("update student_in_req set out_time = '"+ dt_string +"',status='OUT' where username='"+per+"' and (status='accepted' or status='hod_accepted') and request_type='Out Request'")
            con.commit()
        con.close()

        return redirect('security_out')
    else:
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")
        print('In security out pg')
        username=request.user.username
        print(username)
        cur=con.cursor()
        today_date = str(datetime.date.today())
        cur.execute(f"select username,req_accept_time,status from student_in_req where (status='accepted' or status='rejected' or status='gfm_rejected' or status='hod_rejected' or status='hod_accepted') and request_type='Out Request' and req_date='{today_date}'")
        rows=cur.fetchall()
        
        # for generating  id number e.g 1,2,3,4 depend on rows
        new_row = list(rows)
        print(rows)
        for i in range (0, len(rows)):
            new_row[i] = (i+1,) + new_row[i]

        for i in range(0, len(new_row)):
            print("///////////")
            new_row[i] = new_row[i] + (stu_signup.objects.get(username=new_row[i][1]).user_img, )

        for i in range(0, len(new_row)):
            print("///////////")
            new_row[i] = new_row[i] + (stu_signup.objects.get(username=new_row[i][1]).icard_img, )

        if rows is not None:
            # print(new_row) 
            con.close()
            return render(request,'security_out.html',{'data':new_row})
        else:
            # return redirect('apply')
            return render(request,'security_out.html')
    


    # return render(request,'security_out.html')

#************************************************************************************************************************************
@login_required(login_url='../security/security_login')
def security_home(request):
    return render(request,'security_home.html')




#************************************************************************************************************************************



#************************************************************************************************************************************
def logout(request):
    auth.logout(request)
    return redirect('/')



#************************************************************************************************************************************



def test(request):
    if request.method == 'POST':
        return render(request,'test.html')
    else:
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()
        cur.execute("SELECT COUNT(status) FROM student_in_req WHERE branch='computer' and year='BE' and status='IN'")
        # cur.execute("select COUNT(status) from student_in_req WHERE (req_date BETWEEN '2019-12-12' AND '2019-12-15')")
        rows=cur.fetchall()
        l = []
        print(rows)
        for i in rows:
            for a in i:
                l.append(a)
                
        print(l)

        cur=con.cursor()
        cur.execute("SELECT COUNT(status) FROM student_in_req WHERE branch='computer' and year='BE' and status='OUT'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                l.append(a)
        print(l)   

        
        cur.execute("SELECT COUNT(status) FROM student_in_req WHERE branch='computer' and year='TE' and status='IN'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                l.append(a)
                
        print(l)

        cur=con.cursor()
        cur.execute("SELECT COUNT(status) FROM student_in_req WHERE branch='computer' and year='TE' and status='OUT'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                l.append(a)
        print(l)   

        cur.execute("SELECT COUNT(status) FROM student_in_req WHERE branch='computer' and year='SE' and status='IN'")
       
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                l.append(a)
                
        print(l)

        cur=con.cursor()
        cur.execute("SELECT COUNT(status) FROM student_in_req WHERE branch='computer' and year='SE' and status='OUT'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                l.append(a)
        print(l)   


        cur.execute("SELECT COUNT(status) FROM student_in_req WHERE branch='computer' and year='FE' and status='IN'")
       
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                l.append(a)
                
        print(l)

        cur=con.cursor()
        cur.execute("SELECT COUNT(status) FROM student_in_req WHERE branch='computer' and year='FE' and status='OUT'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                l.append(a)
        print(l)   


        return render(request,'test.html',{'data':l})