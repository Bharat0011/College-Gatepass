from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from . models import principal_data
from student.models import stu_signup
from django.core.mail import send_mail
import psycopg2
import datetime


numalpha='abcdefghijklmnopqrstuvwxyz0123456789'
key=5
current_semester = (1 if datetime.datetime.now().month > 6 and datetime.datetime.now().month < 12 else 2)

if current_semester == 2 and datetime.date.month == 12:
    to_year = datetime.datetime.now().year + 1
    from_year = datetime.datetime.now().year
elif current_semester == 2 and datetime.datetime.now().month >= 1:
    from_year = datetime.datetime.now().year - 1
    to_year = datetime.datetime.now().year


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


def principal_login(request):
    if request.method == 'POST':
        username=request.POST.get("username")
        password=request.POST.get("password")
        
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()
        cur.execute("select username,password from principal_principal_data where username='"+ username +"'")
        rows=cur.fetchall()
        print(rows)

        if rows==[]:
            messages.info(request,'User not exists!')
            return redirect("principal_login")
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
                    user = authenticate(request, username=username, password=password)
                    print(user)
                    if user is not None:
                        auth.login(request, user)
                        return redirect("principal_home")
                        # return render(request,'principal_home.html')
                    else:
                        return redirect("principal_login")
                else:         
                    print("out")
                    print(r)
                    messages.info(request,'Username or Password not matched!')
                    con.close()
                    return redirect("principal_login")

        # return render(request,'principal_hom.html') 
    else:
        # user=principal_data(username=username,password=encrypt)
        # user.save()
        # user1= User.objects.create_user(username=username,password=password)
        # user1.save()
        return render(request,'principal_login.html')
    




#************************************************************************************************************************************
@login_required(login_url='../principal/principal_login')
def principal_home(request):
    if request.method == 'POST':
        return render(request,'principal_home.html') 
    else:

        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()

        # cur.execute("select COUNT(status) from student_in_req WHERE (req_date BETWEEN '2019-12-12' AND '2019-12-15')")
        
        
        # ------------------------------------  DATA FOR LINE GRAPH SEM WISE ------------------------------------------
        
        
        #fe,computer, data
        if current_semester==1:
            semInOutCount = []
            #FE
            cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-07-01' AND '{datetime.datetime.now().year}-12-31') and branch='FE' and status='IN'")
            rows=cur.fetchall()
            print(rows)
            for i in rows:
                for a in i:
                    semInOutCount.append(a)
            cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-07-01' AND '{datetime.datetime.now().year}-12-31') and branch='FE' and status='OUT'")
            rows=cur.fetchall()
            print(rows)
            for i in rows:
                for a in i:
                    semInOutCount.append(a)
            
            #Comp

            cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-07-01' AND '{datetime.datetime.now().year}-12-31') and branch='computer' and status='IN'")
            rows=cur.fetchall()
            print(rows)
            for i in rows:
                for a in i:
                    semInOutCount.append(a)
            cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-07-01' AND '{datetime.datetime.now().year}-12-31') and branch='computer' and status='OUT'")
            rows=cur.fetchall()
            print(rows)
            for i in rows:
                for a in i:
                    semInOutCount.append(a)
            
            #Civil

            cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-07-01' AND '{datetime.datetime.now().year}-12-31') and branch='civil' and status='IN'")
            rows=cur.fetchall()
            print(rows)
            for i in rows:
                for a in i:
                    semInOutCount.append(a)
            cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-07-01' AND '{datetime.datetime.now().year}-12-31') and branch='civil' and status='OUT'")
            rows=cur.fetchall()
            print(rows)
            for i in rows:
                for a in i:
                    semInOutCount.append(a)

            #Mechenical

            cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-07-01' AND '{datetime.datetime.now().year}-12-31') and branch='mechanical' and status='IN'")
            rows=cur.fetchall()
            print(rows)
            for i in rows:
                for a in i:
                    semInOutCount.append(a)
            cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-07-01' AND '{datetime.datetime.now().year}-12-31') and branch='mechanical' and status='OUT'")
            rows=cur.fetchall()
            print(rows)
            for i in rows:
                for a in i:
                    semInOutCount.append(a)

            #Electrical

            cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-07-01' AND '{datetime.datetime.now().year}-12-31') and branch='electrical' and status='IN'")
            rows=cur.fetchall()
            print(rows)
            for i in rows:
                for a in i:
                    semInOutCount.append(a)
            cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-07-01' AND '{datetime.datetime.now().year}-12-31') and branch='electrical' and status='OUT'")
            rows=cur.fetchall()
            print(rows)
            for i in rows:
                for a in i:
                    semInOutCount.append(a)

            #Electronics

            cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-07-01' AND '{datetime.datetime.now().year}-12-31') and branch='electronic' and status='IN'")
            rows=cur.fetchall()
            print(rows)
            for i in rows:
                for a in i:
                    semInOutCount.append(a)
            cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-07-01' AND '{datetime.datetime.now().year}-12-31') and branch='electronic' and status='OUT'")
            rows=cur.fetchall()
            print(rows)
            for i in rows:
                for a in i:
                    semInOutCount.append(a)
            
        else:
            
            if current_semester == 2 and datetime.datetime.now().month == 12:
                to_year = datetime.datetime.now().year + 1
                from_year = datetime.datetime.now().year
            elif current_semester == 2 and datetime.datetime.now().month >= 1:
                from_year = datetime.datetime.now().year - 1
                to_year = datetime.datetime.now().year
            
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            print(current_semester)
            print(from_year)
            semInOutCount = []
            #FE
            cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{from_year}-12-01' AND '{to_year}-05-31') and branch='FE' and status='IN'")
            rows=cur.fetchall()
            print(rows)
            for i in rows:
                for a in i:
                    semInOutCount.append(a)
            cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{from_year}-12-01' AND '{to_year}-05-31') and branch='FE' and status='OUT'")
            rows=cur.fetchall()
            print(rows)
            for i in rows:
                for a in i:
                    semInOutCount.append(a)
            
            #Comp

            cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{from_year}-12-01' AND '{to_year}-05-31') and branch='computer' and status='IN'")
            rows=cur.fetchall()
            print(rows)
            for i in rows:
                for a in i:
                    semInOutCount.append(a)
            cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{from_year}-12-01' AND '{to_year}-05-31') and branch='computer' and status='OUT'")
            rows=cur.fetchall()
            print(rows)
            for i in rows:
                for a in i:
                    semInOutCount.append(a)
            
            #Civil

            cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{from_year}-12-01' AND '{to_year}-05-31') and branch='civil' and status='IN'")
            rows=cur.fetchall()
            print(rows)
            for i in rows:
                for a in i:
                    semInOutCount.append(a)
            cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{from_year}-12-01' AND '{to_year}-05-31') and branch='civil' and status='OUT'")
            rows=cur.fetchall()
            print(rows)
            for i in rows:
                for a in i:
                    semInOutCount.append(a)

            #Mechenical

            cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{from_year}-12-01' AND '{to_year}-05-31') and branch='mechanical' and status='IN'")
            rows=cur.fetchall()
            print(rows)
            for i in rows:
                for a in i:
                    semInOutCount.append(a)
            cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{from_year}-12-01' AND '{to_year}-05-31') and branch='mechanical' and status='OUT'")
            rows=cur.fetchall()
            print(rows)
            for i in rows:
                for a in i:
                    semInOutCount.append(a)

            #Electrical

            cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{from_year}-12-01' AND '{to_year}-05-31') and branch='electrical' and status='IN'")
            rows=cur.fetchall()
            print(rows)
            for i in rows:
                for a in i:
                    semInOutCount.append(a)
            cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{from_year}-12-01' AND '{to_year}-05-31') and branch='electrical' and status='OUT'")
            rows=cur.fetchall()
            print(rows)
            for i in rows:
                for a in i:
                    semInOutCount.append(a)

            #Electronics

            cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{from_year}-12-01' AND '{to_year}-05-31') and branch='electronic' and status='IN'")
            rows=cur.fetchall()
            print(rows)
            for i in rows:
                for a in i:
                    semInOutCount.append(a)
            cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{from_year}-12-01' AND '{to_year}-05-31') and branch='electronic' and status='OUT'")
            rows=cur.fetchall()
            print(rows)
            for i in rows:
                for a in i:
                    semInOutCount.append(a)
        
        print(semInOutCount)

        #-------------------------------------------------------------------------------------------------------------
        # ------------------------------------  DATA FOR BAR GRAPH MONTH WISE ------------------------------------------
        #-------------------------------------------------------------------------------------------------------------

        monFEInOut=[]

        #FE
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='FE' and year='FE' and status='IN'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monFEInOut.append(a)
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='FE' and year='FE' and status='OUT'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monFEInOut.append(a)
        # print("FE in out data "+monFEInOut)

        #comp
        monCompInOut=[]
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='computer' and year='SE' and status='IN'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monCompInOut.append(a)
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='computer' and year='SE' and status='OUT'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monCompInOut.append(a)
        
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='computer' and year='TE' and status='IN'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monCompInOut.append(a)
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='computer' and year='TE' and status='OUT'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monCompInOut.append(a)
        
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='computer' and year='BE' and status='IN'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monCompInOut.append(a)
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='computer' and year='BE' and status='OUT'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monCompInOut.append(a)

        # print("Computer in out data "+monCompInOut)


        #civil
        monCivilInOut=[]
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='civil' and year='SE' and status='IN'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monCivilInOut.append(a)
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='civil' and year='SE' and status='OUT'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monCivilInOut.append(a)
        
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='civil' and year='TE' and status='IN'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monCivilInOut.append(a)
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='civil' and year='TE' and status='OUT'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monCivilInOut.append(a)
        
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='civil' and year='BE' and status='IN'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monCivilInOut.append(a)
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='civil' and year='BE' and status='OUT'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monCivilInOut.append(a)

        # print("Civil in out data "+monCivilInOut)


        #Mech
        monMechInOut=[]
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='mechanical' and year='SE' and status='IN'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monMechInOut.append(a)
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='mechanical' and year='SE' and status='OUT'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monMechInOut.append(a)
        
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='mechanical' and year='TE' and status='IN'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monMechInOut.append(a)
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='mechanical' and year='TE' and status='OUT'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monMechInOut.append(a)

        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='mechanical' and year='BE' and status='IN'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monMechInOut.append(a)
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='mechanical' and year='BE' and status='OUT'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monMechInOut.append(a)


        #Elec
        monElectInOut=[]
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='electrical' and year='SE' and status='IN'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monElectInOut.append(a)
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='electrical' and year='SE' and status='OUT'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monElectInOut.append(a)
        
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='electrical' and year='TE' and status='IN'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monElectInOut.append(a)
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='electrical' and year='TE' and status='OUT'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monElectInOut.append(a)
        
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='electrical' and year='BE' and status='IN'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monElectInOut.append(a)
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='electrical' and year='BE' and status='OUT'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monElectInOut.append(a)



        #Electronic
        monElectronicInOut=[]
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='electronic' and year='SE' and status='IN'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monElectronicInOut.append(a)
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='electronic' and year='SE' and status='OUT'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monElectronicInOut.append(a)

        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='electronic' and year='TE' and status='IN'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monElectronicInOut.append(a)
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='electronic' and year='TE' and status='OUT'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monElectronicInOut.append(a)
        
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='electronic' and year='BE' and status='IN'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monElectronicInOut.append(a)
        cur.execute(f"SELECT COUNT(status) FROM student_in_req WHERE (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31') and branch='electronic' and year='BE' and status='OUT'")
        rows=cur.fetchall()
        print(rows)
        for i in rows:
            for a in i:
                monElectronicInOut.append(a)
        
        # print(monElectronicInOut)
         

        return render(request,'principal_home.html',{'data':semInOutCount,'fe':monFEInOut,'comp':monCompInOut,'civil':monCivilInOut,'mech':monMechInOut,'elc':monElectInOut,'elctr':monElectronicInOut})



    



#************************************************************************************************************************************
@login_required(login_url='../principal/principal_login')
def principal_stud_data(request):
    if request.method == 'POST':

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
                cur.execute("update student_in_req set status='rejected',req_accept_time='"+date+"',req_acceped_by='"+username+"' where username='"+per+"'and request_type='"+req_type+"' and req_date='"+today_date+"' and status!='IN' and status!='OUT'")
                # cur.execute("update student_in_req set req_accept_time='"+date+"' where username='"+per+"'")
                con.commit()
        con.close()
        return redirect('principal_stud_data')

        # return render(request,'principal_stud_data.html') 
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
        cur.execute(f"select username,gmail,request_type,mobile_no,reason_des,apply_time,first_name,last_name from student_in_req where (status='hod_rejected' and req_date='{today_date}')")
        rows=cur.fetchall()
    
        print(rows)
        
        for i in range(0, len(rows)):
            print("///////////")
            rows[i] = rows[i] + (stu_signup.objects.get(username=rows[i][0]).user_img, ) 
          
        # return render(request,'hod_accept.html')

        return render(request,'principal_stud_data.html',{'data':rows})




#************************************************************************************************************************************




@login_required(login_url='../principal/principal_login')
def stu_report(request):
    if request.method=='POST':    
        date_from=request.POST.get('date_from')
        date_to=request.POST.get('date_to')
        print('///////////////')
        print(date_from,date_to)

        if date_from=='' and date_to =='':
            messages.info(request,'Plz enter the dates')
            return render(request,'stu_report.html')

        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()
        cur.execute("select username,mobile_no,gmail,reason_des,req_acceped_by,req_date,status from student_in_req where req_date >= '"+ date_from+"' and req_date <= '"+date_to+"' and (status='IN' or status='OUT')")
        rows=cur.fetchall()
        print(rows)

        new_row = list(rows)
        for i in range (0, len(rows)):
            new_row[i] = (i+1,) + new_row[i]

        if rows is not None:
            print(rows) 
            con.close()
            return render(request,'stu_report.html',{'data':new_row})
        else:
            return render(request,'stu_report.html')
    else:
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()
        cur.execute("select username,mobile_no,gmail,reason_des,req_acceped_by,req_date,status from student_in_req where status='accepted' or status='IN' or status='OUT'")
        rows=cur.fetchall()

        new_row = list(rows)
        for i in range (0, len(rows)):
            new_row[i] = (i+1,) + new_row[i]

        if rows is not None:
            print(rows) 
            con.close()
            return render(request,'stu_report.html',{'data':new_row})
        else:
            # return redirect('apply')
            return render(request,'stu_report.html')


#************************************************************************************************************************************


@login_required(login_url='../principal/principal_login')
def frequent_app(request):
    if request.method == 'POST':
        return render(request,'frequent_app.html') 
    else:

        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()
        cur.execute(f"SELECT DISTINCT username FROM student_in_req where (req_date BETWEEN '{datetime.datetime.now().year}-{datetime.datetime.now().month}-01' AND '{datetime.datetime.now().year}-{datetime.datetime.now().month}-31')")
        rows=cur.fetchall()
        print(rows)

        count=[]
        data=[]
        for r in rows:
            for i in r:
                print(i)
                cur.execute(f"select count(username) from student_in_req where username='{i}'")
                a=cur.fetchall()
                print(a)
                for b in a:
                    for c in b:
                        count.append(c)
                cur.execute(f"select username,first_name,last_name,gmail,mobile_no,branch,year from student_in_req where username='{i}'")
                dat = cur.fetchone()
                print(dat)
                data.append(dat)
        print(count)
        print(type(data))
        
        for i in range(0,len(data)):
            data[i] = data[i] + (count[i],) 



        def Sort(tup): 
            # reverse = True (Sorts in Descending order) 
            # key is set to sort using float elements 
            # lambda has been used 
            return(sorted(tup, key = lambda x: float(x[7]), reverse = True)) 
  
        # Driver Code 
        tup = [('lucky', '18.265'), ('nikhil', '14.107'), ('akash', '24.541'),  
        ('anand', '4.256'), ('gaurav', '10.365')] 
        print(Sort(data))
            
        
        print("-------------------------------------")
        print(data)
            


        return render(request,'frequent_app.html',{'d':Sort(data)})



        


#************************************************************************************************************************************
def logout(request):
    auth.logout(request)
    return redirect('/')