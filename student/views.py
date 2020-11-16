from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from student.models import stu_signup,in_req,email_verifiction
import psycopg2
import math, random
import datetime
from datetime import date
import os
from django.conf import settings
from django.core.mail import send_mail


numalpha='abcdefghijklmnopqrstuvwxyz0123456789'
key=5


# Create your views here.


#************************************************************************************************************************************
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

def student_login(request):
    if request.method == 'POST':
        username=request.POST.get("username")
        password=request.POST.get("password")
    
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()
        

# verify account is valid or not
        cur.execute(f"select valid from student_stu_signup where username='{username}'")
        valid=cur.fetchall()
        print(valid)

        if (any('Pending' in i for i in valid)):
            print('Pending')
            messages.info(request,'Plz contact your respective GFM for validating your account')
            return redirect('student_login')

        elif (any('rejected' in i for i in valid)):
            print('rejected')
            messages.info(request,'Your account has been rejected')
            return redirect('student_login')

        else:
            if username is not None:
                cur.execute("select username,password from student_stu_signup where username='"+ username +"'")
                rows=cur.fetchall()
                if rows==[]:
                    messages.info(request,'User not exists!')
                    return redirect("student_login")
                else:
                    for r in rows:
                        decrypt=''
                        pas=r[1]
                        for i in pas:
	                        posi=numalpha.find(i)
	                        newposi=(posi-key)%36
	                        decrypt=decrypt+numalpha[newposi]

                        if r[0]==username and decrypt==password :
                            print(r)
                            # con.close()
                            # user=auth.authenticate(username=username,password=password)
                            user = authenticate(request, username=username, password=password)
                            print(user)
                            if user is not None:
                                auth.login(request, user)
                                return redirect("stu_home")
                            else:
                                return redirect("student_login")
                        else:         
                            print("out")
                            print(r)
                            messages.info(request,'Username or Password not matched!')
                            con.close()
                            return redirect("student_login")
            else:
                return render(request,'stu_login.html')
            print(rows)
            con.close()
            return redirect('student_login') 
    else:
        return render(request,'stu_login.html')



#************************************************************************************************************************************


def email_verify(request):
    if request.method=='POST':
        otp=request.POST.get("otp")
        email = request.session["email1"]
        data = request.session["data"]
        print(email)
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()
        cur.execute(f"select otp from student_email_verifiction where email='{email}'")
        rows = cur.fetchall()

        for r in rows:
            if r[0]==otp:
                cur.execute(f"update student_stu_signup set email_verify='accepted' where email='{email}'")
                con.commit()
                user= stu_signup(username=data['username'],first_name=data['first_name'],last_name=data['last_name'],gender=data['gender'],password=data['encrypt'],email=data['email'],mobile_no=int(data['mobile_no']),year=data['year'],branch=data['branch'],roll_no=int(data['roll_no']),gfm=data['gfm'],icard_img=data['p'],user_img=data['p1'],valid='Pending',email_verify='accepted')
                user.save()
                # Authentication mate django user create kido
                user= User.objects.create_user(username=data['username'],password=data['password1'],email=data['email'],first_name=data['first_name'],last_name=data['last_name'])
                user.save()
                del request.session['email1']
                return redirect('student_login')      
            else:
                messages.info(request,'OTP did not match !!!!!!')
                return redirect('email_verify')
        
        return render(request,'email_verify.html')
    else:
        email = request.session["email1"]
        print(email)
        data = request.session.get("data",None)
        # print(data)
        print(data['username'])
        return render(request,'email_verify.html')








#************************************************************************************************************************************


def signup_form(request):
    if request.method=='POST':
        username=request.POST.get('username')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        gender=request.POST.get('gender')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        email=request.POST.get('email')
        mobile_no=request.POST.get('mobile_no')
        year=request.POST.get('year')
        branch=request.POST.get('branch')
        roll_no=request.POST.get('roll_no')
        gfm=request.POST.get('gfm')
        
        
        icard_img = request.POST.get("b64-value1")
        print("-----------------Testing p tag-----------------")
        user_img=request.POST.get('b64-value2')

        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        # cur=con.cursor()
        # cur.execute("select username from park_signup where username='" + username + "'")
        # rows=cur.fetchall()
        
        if User.objects.filter(username=username).exists():
            messages.info(request,'User name taken')
            return redirect('signup_form')
        elif User.objects.filter(email=email).exists():
            messages.info(request,'Email id already in use')
            return redirect('signup_form')
        elif password1!=password2:
            messages.info(request,'Password did not match')
            return redirect('signup_form')
        elif not int(roll_no) > 0:
            messages.info(request,'Invalid Roll number')
            return redirect('signup_form')
        else:
            encrypt=''
            for i in password1:
	            pos=numalpha.find(i)
	            newpos=(pos+key)%36
	            encrypt=encrypt+numalpha[newpos]
            
            print('registered')
            #  Email verify using otp
            con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

            cur=con.cursor()
            request.session["email1"] = email
            string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            OTP = ""
            length = len(string) 
            for i in range(6) : 
                OTP = OTP + string[math.floor(random.random() * length)]
            print(OTP)
            user= email_verifiction(email=email,otp=OTP)
            user.save()
            # cur.execute(f"update student_stu_signup set email_otp='{OTP}' where email='{email}'")
            # con.commit()

            subject = 'Verify your gmail account.'
            message = '\n Your OTP is : '+OTP+' .'
            from_email = settings.EMAIL_HOST_USER
            to_list = [email,'lquresh52@gmail.com']
            send_mail(subject , message , from_email , to_list , fail_silently=True)

            data = {'username':username,'first_name':first_name,'last_name':last_name,'gender':gender,'encrypt':encrypt,'password1':password1,'email':f'{email}','mobile_no':f'{mobile_no}','year':year,'branch':branch,'roll_no':f'{roll_no}','gfm':gfm,'p':f'{icard_img}','p1':f'{user_img}'}
            request.session['data'] = data            
            return redirect('email_verify')

        return redirect('student_login')
    else:
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()
        cur.execute("select first_name,last_name,email from gfm_gfm_signup where valid='accepted'")
        rows = cur.fetchall()

        print(rows)
        data = []
        
        # for row in rows:
        #     # print(row[0],row[1])
        #     a =  f'{row[0]} '+row[1]
        #     print(a)
        #     data.append(a)

        # print(data)

        return render(request,'stu_signup.html',{'data':rows})



#************************************************************************************************************************************





def forget_pass11(request):
    if request.method == 'POST':
       
        email=request.POST.get("email")
        mobile_no=request.POST.get("mobile_no")

        # first_name = request.user.first_name
        # last_name = request.user.last_name
        request.session["email"] = email
        print(email,mobile_no)
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()
        cur.execute("select email,mobile_no,valid from student_stu_signup where email='" + email + "' and mobile_no="+mobile_no+"")
        rows=cur.fetchall()
        print(rows)
        if not rows ==[]:
            for r in rows:
                if not r[2]=='rejected':
                    print(r[1])
                    if email == r[0] and int(mobile_no)==r[1]:
                        
                        string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
                        OTP = ""
                        length = len(string) 
                        for i in range(6) : 
                            OTP = OTP + string[math.floor(random.random() * length)]
                        print(OTP)
                        cur.execute(f"update student_stu_signup set otp='{OTP}' where email='{email}'")
                        con.commit()

                        subject = 'Password Change OTP .'
                        message = '\n Your OTP is : '+OTP+'.'
                        from_email = settings.EMAIL_HOST_USER
                        to_list = [email,'lquresh52@gmail.com']
                        send_mail(subject , message , from_email , to_list , fail_silently=True)
                        
                        return redirect('otp')
                    else:
                        messages.info(request,'Email id and mobile number did not match!!!!!!!! ')
                        return render(request,'forget_pass1.html')
                else :
                    messages.info(request,'Your account has been rejected')
                    return render(request,'forget_pass1.html')
        # else:
        #     messages.info(request,'Email id and mobile number didn''t match ')
        #     return render(request,'forget_pass1.html')
    else:
        return render(request,'forget_pass1.html')
    

#************************************************************************************************************************************

def otp(request):
    if request.method=='POST':
        otp=request.POST.get("otp")

        email = request.session["email"]
        
        print(email)

        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()
        cur.execute(f"select otp from student_stu_signup where email='{email}'")
        rows = cur.fetchall()

        for r in rows:
            if r[0]==otp:
                return redirect('forget_pass22')      
            else:
                messages.info(request,'OTP did not match !!!!!!')
                return redirect('otp')

        # return render(request,'otp.html')
    else:
        # email = request.session["email"]
        # print(email)
        return render(request,'otp.html')





#************************************************************************************************************************************

def forget_pass22(request):
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
            encrypt=''
            for i in password1:
	            pos=numalpha.find(i)
	            newpos=(pos+key)%36
	            encrypt=encrypt+numalpha[newpos]


            u = User.objects.get(email=''+email+'')
            u.set_password(''+password1+'')
            u.save()
            print('//////////////  changed pass in AUTH-USER //////////////')
            print(u)

            cur.execute("update student_stu_signup set password='"+ encrypt +"' where email='"+email+"'")
            con.commit()
            con.close()
            return redirect('student_login')
        else:
            messages.info(request,'password and confirm password did not match')
            return redirect('forget_pass22')
    else:
        return render(request,'forget_pass2.html')
    
#************************************************************************************************************************************
# application='none'
@login_required(login_url='../student/student_login')
def stu_home(request):
    if request.method=='POST':
        date_from=request.POST.get('date_from')
        date_to=request.POST.get('date_to')
        print('///////////////')
        print(date_from,date_to)
        username=request.user.username
        if date_from=='' and date_to =='':
            messages.info(request,'Plz enter the dates')
            return render(request,'stu_home.html')

        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()
        cur.execute(f"select apply_time,reason_des,request_type,status,req_acceped_by from student_in_req where username='{username}' and req_date >= '"+ date_from+"' and req_date <= '"+date_to+"'")
        rows=cur.fetchall()
        print(rows)
        new_row = list(rows)
        
        for i in range (0, len(rows)):
            new_row[i] = (i+1,) + new_row[i]

        if rows is not None:
            print(new_row) 
            con.close()
            return render(request,'stu_home.html',{'data':new_row})
        else:
            return render(request,'stu_home.html')
    else:
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")
        print('In student home')
        username=request.user.username
        print(username)
        cur=con.cursor()
        cur.execute("select apply_time,reason_des,request_type,status,req_acceped_by from student_in_req where username='" + username + "'")
        rows=cur.fetchall()
        
        # for generating  id number e.g 1,2,3,4 depend on rows
        new_row = list(rows)
        for i in range (0, len(rows)):
            new_row[i] = (i+1,) + new_row[i]

        print(new_row)
        return render(request,'stu_home.html',{'data':new_row})
        

#************************************************************************************************************************************


@login_required(login_url='../student/student_login')
def my_profile(request):
    if request.method=='POST':
        return render(request,'my_profile.html')
    else:
        username=request.user.username
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")
        
        cur=con.cursor()
        
        cur.execute(f"select first_name,last_name,year,branch,roll_no,email,mobile_no,gfm from student_stu_signup where username='{username}'")
        rows = cur.fetchall()
        print(rows)
        a=''
        for r in rows:
            a = r[7]
        print(a)
        cur.execute(f"select first_name,last_name from gfm_gfm_signup where email='{a}'")
        gfm = cur.fetchall()
        print(gfm)

        cur.execute(f"select icard_img,user_img from student_stu_signup where username='{username}'")
        image = cur.fetchall()


        for g in gfm:
            gfm = f'{g[0]} '+g[1]
        print(gfm)

        return render(request,'my_profile.html',{'data':rows,'gfm':gfm,'img':image})


#************************************************************************************************************************************





def logout(request):
    auth.logout(request)
    return redirect('student_login')



#************************************************************************************************************************************


@login_required(login_url='../student/student_login')
def in_apply(request):
    if request.method=='POST':
        # reason=request.POST.get('radio')
        reason_des=request.POST.get('reason_des')
        # request_type=request.POST.get('Submit')
        print(reason_des)
        now = datetime.datetime.now()
        username=request.user.username
        first_name = request.user.first_name
        last_name = request.user.last_name
        today = str(date.today())
        print(today)
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")


        cur=con.cursor()
        cur.execute("select mobile_no,email,year,branch,first_name,last_name from student_stu_signup where username='" + username + "'")
        rows=cur.fetchall()
        print(rows)
        email=''
        mobile_no=''
        year=''
        branch=''
        first_name=''
        last_name=''
        if not rows==[]:
            for r in rows:
                email=r[1]
                mobile_no=int(r[0])
                year=r[2]
                branch=r[3]
                first_name=r[4]
                last_name=r[5]


        cur.execute("select count(req_date) from student_in_req where username='" + username + "' and req_date='"+today+"' and request_type='IN Request'")
        row=cur.fetchall()
        print(row)
        count=0
        if not row==[]:
            for r in row:
                count=int(r[0])
        print("Request count for todats date is : " + str(count))
        
        if count==0:
            subject = 'There is a IN request by student : '+first_name+last_name+'.'
            message = '\n REASON DESCRIPTION : '+reason_des
            from_email = settings.EMAIL_HOST_USER
            to_list = ['lquresh52@gmail.com']

            send_mail(subject , message , from_email , to_list , fail_silently=True)

            user=in_req(apply_time=datetime.datetime.now(), reason="_", reason_des=reason_des, username=username, gmail=email, mobile_no=mobile_no, status='Pending',request_type='IN Request' , in_req_count=count+1 , req_date=today,branch=branch,year=year,first_name=first_name,last_name=last_name )
            user.save()
            print('data saved in table')
        else:
            messages.info(request,'Your daily limit for apply of gate pass is over contact your respective HOD sir')
            return redirect('in_apply')
        return redirect('stu_home')
    else:
        return render(request,'in_apply.html')




#************************************************************************************************************************************

@login_required
def out_apply(request):
    if request.method=='POST':
        # reason=request.POST.get('radio')
        reason_des=request.POST.get('reason_des')
        # request_type=request.POST.get('Submit')
        print(reason_des)
        now = datetime.datetime.now()
        username=request.user.username
        first_name = request.user.first_name
        last_name = request.user.last_name
        today = str(date.today())
        
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")


        cur=con.cursor()
        cur.execute("select mobile_no,email,year,branch,first_name,last_name from student_stu_signup where username='" + username + "'")
        rows=cur.fetchall()
        email=''
        mobile_no=''
        print(rows)
        year=''
        branch=''
        first_name=''
        last_name=''

        if not rows==[]:
            for r in rows:
                email=r[1]
                mobile_no=int(r[0])
                year=r[2]
                branch=r[3]
                first_name=r[4]
                last_name=r[5]



        cur.execute("select count(req_date) from student_in_req where username='" + username + "' and req_date='"+today+"' and request_type='Out Request'")
        row=cur.fetchall()
        print(row)
        count=0
        if not row==[]:
            for r in row:
                count=int(r[0])
        print("Request count for todats date is : " + str(count))

        if count==0:
            subject = 'There is a OUT Request by student : '+first_name+last_name+'.'
            message = '\n REASON DESCRIPTION : '+reason_des
            from_email = settings.EMAIL_HOST_USER
            to_list = ['lquresh52@gmail.com']

            send_mail(subject , message , from_email , to_list , fail_silently=True)
            user=in_req(apply_time=datetime.datetime.now(), reason='_', reason_des=reason_des, username=username, gmail=email, mobile_no=mobile_no, status='Pending',request_type='Out Request' , out_req_count=count+1 , req_date=today ,branch=branch,year=year,first_name=first_name,last_name=last_name)
            user.save()


        else:
            messages.info(request,'Your daily limit for apply of gate pass is over contact your respective HOD sir')
            return redirect('out_apply')
        return redirect('stu_home')
    else:
        return render(request,'out_apply.html')


    
    
    
    
    
    # if request.method=='POST':
    #     return render(request,'out_apply.html')
    # else:
    #     return render(request,'out_apply.html')




#************************************************************************************************************************************

@login_required
def inout_apply(request):
    if request.method=='POST':

        return render(request,'inout_apply.html')
    else:
        return render(request,'inout_apply.html')




#************************************************************************************************************************************