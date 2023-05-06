import pymysql
from flask import Flask, render_template, request, session, url_for, redirect,jsonify,make_response
import Query_Utility as query
from datetime import datetime, timedelta
app = Flask(__name__)

app.secret_key = "NK3K"
# Utility Functions
def save_to_session(dic):
    for key in dic.keys():
        session[key] = dic[key]
    return
conn = pymysql.connect(host= 'localhost',
                       user='root',
                       password = '',
                       db='flight',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

def get_each_month(month_wise, start_year, start_month, end_year, end_month, start_date, end_date):
    if start_year == end_year and start_month == end_month:
        month_wise.append
        ([start_date, end_date, 0])
    else:
        if start_month == 12:
            start_year += 1
            start_month = 0
        month_wise.append([start_date, "%d-%02d-01" % (start_year, start_month + 1), 0])
        start_month += 1
        while start_year <= end_year:
            if start_year == end_year:
                if start_month >= end_month:
                    break
                else:
                    month_wise.append(
                        ["%d-%02d-01" % (start_year, start_month), "%d-%02d-01" % (start_year, start_month + 1), 0])
            else:
                if start_month == 12:
                    month_wise.append(["%d-%02d-01" % (start_year, start_month), "%d-%02d-01" % (start_year + 1, 1), 0])
                    start_year += 1
                    start_month = 0
                else:
                    month_wise.append(
                        ["%d-%02d-01" % (start_year, start_month), "%d-%02d-01" % (start_year, start_month + 1), 0])
            start_month += 1
        month_wise.append(["%d-%02d-01" % (end_year, end_month), end_date, 0])


def update_month_wise_my_spendings(my_spendings, month_wise):
    for i in my_spendings:
        for j in range(len(month_wise)):
            if j == len(month_wise) - 1:
                if month_wise[j][0] <= i[0] <= month_wise[j][1]:
                    month_wise[j][2] += i[1]
                    break
            else:
                if month_wise[j][0] <= i[0] < month_wise[j][1]:
                    month_wise[j][2] += i[1]
                    break
    for i in range(len(month_wise)):
        month_wise[i] = [month_wise[i][0] + " -> " + month_wise[i][1], month_wise[i][2]]

def update_month_wise_reports(reports, month_wise):
    for i in reports:
        for j in range(len(month_wise)):
            if j == len(month_wise) - 1:
                if month_wise[j][0] <= i[1] <= month_wise[j][1]:
                    month_wise[j][2] += 1
                    break
            else:
                if month_wise[j][0] <= i[1] < month_wise[j][1]:
                    month_wise[j][2] += 1
                    break
    for i in range(len(month_wise)):
        month_wise[i] = [month_wise[i][0] + " -> " + month_wise[i][1], month_wise[i][2]]


@app.route('/')
def hello():
    if session.get('signin'):
        if session['user_type'] == 'customer':
            return redirect(url_for('customer_home'))
        elif session['user_type'] == 'agent':
            return redirect(url_for('agent_home'))
        else:
            return redirect(url_for('staff_home'))
    else:
        return render_template('introduction.html')

@app.route('/public_view', methods = ["GET","POST"])
def public_view():
    if request.method =='GET':
        data_dic = query.public_view(conn)
        locations = query.get_locations(conn)
        return render_template("public_view.html",
                           departure_city = locations['departure_loc'],
                           arrival_city = locations['arrival_loc'],
                           d = data_dic)

    elif request.method == 'POST':
        locations = query.get_locations(conn)
        html_get = {'from':request.form['from'],
                    'to':request.form['to'],
                    'dt':request.form['date']}
        print(html_get)
        data_dic = query.filter_result(conn,html_get)
       
        print(data_dic)
        return render_template("public_view.html",
                               departure_city=locations['departure_loc'],
                               arrival_city=locations['arrival_loc'],
                               d=data_dic)


@app.route('/signin', methods = ["GET","POST"])
def signin():
    if request.method =='GET':
        error = session.get('error')
        airlines = query.get_airlines(conn)
        return render_template("signin.html",
                               airlines = airlines, error = error)
    if request.method == 'POST':
        info_cus = {
            "email": request.form.get("cus_email"),
            "password": request.form.get("cus_pass"),
        }
        info_ba = {
            "email": request.form.get("agent_email"),
            "password": request.form.get("agent_pass"),
        }
        info_as = {
            "email": request.form.get("staff_uname"),
            "password": request.form.get("staff_pass"),
            "airline_name": request.form.get("staff_airline")
        }
      
        if query.check_full(info_cus):
            save_to_session(info_cus)
            return redirect(url_for("customer_home"))
        elif query.check_full(info_ba):
            save_to_session(info_ba)
            return redirect(url_for("agent_home"))
        elif query.check_full(info_as):
            save_to_session(info_as)
            return redirect(url_for("staff_home"))
    return render_template("signin.html")





@app.route('/register', methods=["POST", "GET"])
def register():

    if request.method =='GET':
        airlines = query.get_airlines(conn)
        return render_template("register.html",airlines = airlines)
    if request.method == 'POST':
        info_cus = {
            "email": request.form.get("cus_email"),
            "name": request.form.get("cus_name"),
            "password":  request.form.get("cus_pass"),
            "building_number": request.form.get("building"),
            "street": request.form.get("street"),
            "city": request.form.get("city"),
            "state": request.form.get("state"),
            "phone_number": request.form.get("phone_num"),
            "passport_number": request.form.get("passport_num"),
            "passport_expiration": request.form.get("passport_exp"),
            "passport_country": request.form.get("passport_country"),
            "date_of_birth": request.form.get("cus_dob"),
        }
        
        info_agent = {
            "email": request.form.get("agent_email"),
            "password": request.form.get("agent_pass"),
            "booking_agent_id": request.form.get("agent_id")
        }
        info_staff = {
            "email": request.form.get("staff_uname"),
            "password": request.form.get("staff_pass"),
            "first_name": request.form.get("staff_first_name"),
            "last_name": request.form.get("staff_last_name"),
            "date_of_birth": request.form.get("staff_dob"),
            "airline_name": request.form.get("staff_airline"),
            "permission_type": request.form.get("permission")
        }
        
        if query.check_full(info_cus):
            save_to_session(info_cus)
            print("success!!!")
            # return render_template("register.html")
            return redirect(url_for("register_cus"))
        elif query.check_full(info_agent):
            save_to_session(info_agent)
            print("success!!!")
            # return render_template("register.html")
            return redirect(url_for("register_agent"))
        elif query.check_full(info_staff)  :
            save_to_session(info_staff)
            print("success!!!")
            # return render_template("register.html")
            return redirect(url_for("register_staff"))

@app.route('/register/cus', methods=["POST", "GET"])
def register_cus():
    valid, err = query.reg_validation_cus(conn, session)
    print(valid)
    if valid:
        session['signin'] = True
        session["user_type"] = 'customer'
        query.add_cus(conn, session)
        # return render_template("register.html")
        return redirect(url_for("customer_home"))
    else:
        return render_template('register.html', error=err)


@app.route('/register/agent', methods=['POST', 'GET'])
def register_agent():
    # Pass the session input information from html to the backend to check whether the address is already in use.
    valid, err = query.reg_validation_ba(conn, session)
    if valid:
        session['signin'] = True
        session["user_type"] = 'agent'
        query.add_ba(conn, session)
        return redirect(url_for("agent_home"))
    else:
        return render_template('register.html', error=err)


@app.route('/register/staff', methods=['GET', 'POST'])
def register_staff():
    valid, err = query.reg_validation_as(conn, session)
    if valid:
        query.add_as(conn, session)
        session['signin'] = True
        session["user_type"] = 'staff'
        return redirect(url_for("staff_home"))
    else:
        return render_template('register.html', error=err)

@app.route("/sign_in", methods=['GET', 'POST'])
def sign_in():
    if request.method =='GET':
        error = session.get('error')
        airlines = query.get_airlines(conn)
        return render_template("signin.html",airlines = airlines, error = error)
    if request.method == 'POST':
        info_cus = {
            "customer_email": request.form.get("cus_email"),
            "password": request.form.get("cus_pass"),
        }
        info_agent = {
            "agent_email": request.form.get("agent_email"),
            "password": request.form.get("agent_pass"),
        }
        info_staff = {
            "username": request.form.get("staff_uname"),
            "password": request.form.get("staff_pass"),
            "airline_name": request.form.get("staff_airline")
        }
        if query.check_full(info_cus):
            save_to_session(info_cus)
            return redirect(url_for("customer_home"))
        elif query.check_full(info_agent):
            save_to_session(info_agent)
            return redirect(url_for("agent_home"))
        elif query.check_full(info_staff):
            save_to_session(info_staff)
            return redirect(url_for("staff_home"))


@app.route("/sign_in/customer_home", methods=['GET', 'POST'])
def customer_home():
    session['signin'] = query.sign_in_check(conn, session['email'],session["password"], 'customer','')
    session["user_type"] = 'customer'
    locations = query.get_locations(conn)
    d = query.get_top5_number(conn)
    total_amount = 0
    month_wise = [] 
    if not session["signin"] and request.method == 'GET':
        session["error"] = 'Invalid username or password, please try again.'
        return redirect(url_for("sign_in"))
    elif (session["signin"] and request.method == "GET") or(session["signin"] and request.method=="POST" and request.form["submit_button"]=="clear_search"):
        TODAY = datetime.today()
        PAST = (TODAY - timedelta(days=365))
        THIS_YEAR, PAST_YEAR, THIS_MONTH = TODAY.year, TODAY.year - 1, TODAY.month
        month_wise.append(["%d-%02d-01" % (THIS_YEAR, THIS_MONTH), TODAY.strftime("%Y-%m-%d"), 0])
        for i in range(1, 6):
            if THIS_MONTH - i > 0:
                temp = ["%d-%02d-01" % (THIS_YEAR, THIS_MONTH - i), "%d-%02d-01" % (THIS_YEAR, THIS_MONTH - i + 1), 0]
            elif THIS_MONTH - i + 1 > 0:
                temp = ["%d-%02d-01" % (PAST_YEAR, 12 + (THIS_MONTH - i)),
                        "%d-%02d-01" % (THIS_YEAR, THIS_MONTH - i + 1), 0]
            else:
                temp = ["%d-%02d-01" % (PAST_YEAR, 12 + (THIS_MONTH - i)),
                        "%d-%02d-01" % (THIS_YEAR, 12 + (THIS_MONTH - i + 1)), 0]
            month_wise.append(temp)
        total_amount = query.get_my_spendings_total_amount(conn, session["email"], PAST.strftime("%Y-%m-%d"),
                                                              TODAY.strftime("%Y-%m-%d"))
        my_spendings = query.get_my_spendings_certain_range(conn, session["email"], month_wise[-1][0],
                                                               month_wise[0][1])

        month_wise.sort()
        print("Successful:",month_wise)
        update_month_wise_my_spendings(my_spendings, month_wise)
        print("Successful:",month_wise)
        data_dic = query.public_view(conn)
        purchased_flight = query.get_purchased_flight(conn, session)
        return render_template('homepage_customer.html',
                               # same results as
                               departure_city=locations['departure_loc'],
                               arrival_city=locations['arrival_loc'],
                               all=data_dic,
                               purchased = purchased_flight,
                               airlines = query.get_airlines(conn),
                               flight_num = query.get_flight_num(conn),
                               data_list = d,
                               total_amount=total_amount, 
                               month_wise=month_wise
                               )
                               # spent = query.get_spent(query.get_past_year_period())))
    if session["signin"] and request.method =='POST':
        purchased_flight = query.get_purchased_flight(conn, session)
        TODAY = datetime.today()
        PAST = (TODAY - timedelta(days=365))
        THIS_YEAR, PAST_YEAR, THIS_MONTH = TODAY.year, TODAY.year - 1, TODAY.month
        month_wise.append(["%d-%02d-01" % (THIS_YEAR, THIS_MONTH), TODAY.strftime("%Y-%m-%d"), 0])
        for i in range(1, 6):
            if THIS_MONTH - i > 0:
                temp = ["%d-%02d-01" % (THIS_YEAR, THIS_MONTH - i), "%d-%02d-01" % (THIS_YEAR, THIS_MONTH - i + 1), 0]
            elif THIS_MONTH - i + 1 > 0:
                temp = ["%d-%02d-01" % (PAST_YEAR, 12 + (THIS_MONTH - i)),
                        "%d-%02d-01" % (THIS_YEAR, THIS_MONTH - i + 1), 0]
            else:
                temp = ["%d-%02d-01" % (PAST_YEAR, 12 + (THIS_MONTH - i)),
                        "%d-%02d-01" % (THIS_YEAR, 12 + (THIS_MONTH - i + 1)), 0]
            month_wise.append(temp)
        total_amount = query.get_my_spendings_total_amount(conn, session["email"], PAST.strftime("%Y-%m-%d"),
                                                              TODAY.strftime("%Y-%m-%d"))
        my_spendings = query.get_my_spendings_certain_range(conn, session["email"], month_wise[-1][0],
                                                               month_wise[0][1])

        month_wise.sort()
        
        update_month_wise_my_spendings(my_spendings, month_wise)
        # print("Unsuccessful:",month_wise)
        if request.form["submit_button"] == "search":
            html_get = {'from': request.form.get('from'),
                    'to': request.form.get('to'),
                    'dt': request.form.get('date'),
                    'flight_num':request.form.get("flight_num"),
                    'airline': request.form.get("airline")}
            data_dic = query.filter_result(conn, html_get)
            flight_num = html_get["flight_num"]
            return render_template('homepage_customer.html',
                               # same results as
                               departure_city=locations['departure_loc'],
                               arrival_city=locations['arrival_loc'],
                               all=data_dic,
                               purchased = purchased_flight,
                               airlines = query.get_airlines(conn),
                               flight_num = query.get_flight_num(conn),
                               data_list = d,
                               total_amount=total_amount, 
                               month_wise=month_wise)
        elif request.form["submit_button"] == "filter":
            data_dic = query.public_view(conn)
            start_date = request.form["start_date"]
            end_date = request.form["end_date"]
            # print(start_date, end_date)
            start_year, start_month = int(start_date[:4]), int(start_date[5:7])
            end_year, end_month = int(end_date[:4]), int(end_date[5:7])
            month_wise = []
            get_each_month(month_wise, start_year, start_month, end_year, end_month, start_date, end_date)
            print(month_wise)

            total_amount = query.get_my_spendings_total_amount(conn, session["email"], start_date, end_date)
            my_spendings = query.get_my_spendings_certain_range(conn, session["email"], start_date, end_date)
            # print(total_amount)

            update_month_wise_my_spendings(my_spendings, month_wise)# print(total_amount)
            # update_month_wise_my_spendings(my_spendings, month_wise)
            return render_template('homepage_customer.html',
                               # same results as
                               departure_city=locations['departure_loc'],
                               arrival_city=locations['arrival_loc'],
                               all=data_dic,
                               purchased = purchased_flight,
                               airlines = query.get_airlines(conn),
                               flight_num = query.get_flight_num(conn),
                               data_list = d,
                               total_amount=total_amount, 
                               month_wise=month_wise
                            )
        else:
            print("hihihi")
            flight_num = request.form["submit_button"]
            success,err = query.purchase(conn, flight_num, session['email'], 'NULL')
            if success:
                return redirect(url_for("customer_home"))
            else:
                return redirect(url_for("customer_home"))

@app.route("/sign_in/agent_home", methods=["POST", "GET"])
def agent_home():
    session['signin'] = query.sign_in_check(conn, session['email'],session["password"], 'booking_agent','')
    session["user_type"] = 'booking_agent'
    da = query.get_top_customer_number(conn,session)
    data_list2 = query.get_customer_commission(conn, session)
    locations = query.get_locations(conn)
    total_month = query.view_commission_month(conn, session)[0]
    avg_month = query.view_commission_month(conn, session)[1]
    total_year = query.view_commission_month(conn, session)[2]
    avg_year = query.view_commission_month(conn, session)[3]
    customer_emails = query.get_customer_email(conn, session)
    ticket_total = query.get_ticket_total(conn, session)
    if not session["signin"] and request.method == 'GET':
        session["error"] = 'Invalid username or password, please try again.'
        return redirect(url_for("sign_in"))
    elif (session["signin"] and request.method == "GET") or (session["signin"] and request.method=="POST" and request.form["submit_button"]=="clear_search") :
        data_dic = query.public_view(conn)
        locations = query.get_locations(conn)
        purchased_flight = query.get_purchased_flight(conn, session)
        return render_template('homepage_booking_agent.html',
                               departure_city=locations['departure_loc'],
                               arrival_city=locations['arrival_loc'],
                               all=data_dic,
                               purchased=purchased_flight,
                               total_month = total_month,
                               avg_month = avg_month,
                               total_year= total_year,
                                flight_num=query.get_flight_num(conn),
                               avg_year=avg_year,
                               customer_emails = customer_emails,
                               data_list1 = da,
                                data_list2 = data_list2,
                                ticket_total = ticket_total
                               )

    elif request.method == 'POST' and request.form["submit_button"]== "search":
        da = query.get_top_customer_number(conn,session)
        html_get = {'from': request.form.get('from'),
                    'to': request.form.get('to'),
                    'dt': request.form.get('date'),
                    'flight_num': request.form.get("flight_num")
                    }
        data_dic = query.filter_result(conn, html_get)
        purchased_flight = query.get_purchased_flight(conn, session)
        flight_num = html_get["flight_num"]
       
        return render_template('homepage_booking_agent.html',
                                # same results as
                                departure_city=locations['departure_loc'],
                                arrival_city=locations['arrival_loc'],
                                all=data_dic,
                                purchased=purchased_flight,
                                flight_num=query.get_flight_num(conn),
                                total_month=total_month,
                                avg_month=avg_month,
                                data_list1 = da,
                                data_list2 = data_list2,
                                ticket_total = ticket_total)
    else:
        purchase_email = request.form.get("purchase_email")
        if purchase_email is None or purchase_email == '':
            success, err = False, 'Please enter both flight num and the customer email.'
            print('executing if_clause')
            return redirect(url_for("agent_home"))
        else:
            flight_num = request.form["submit_button"]
            purchase_email = request.form.get("purchase_email")
            print(purchase_email)
            query.purchase(conn, flight_num, purchase_email, session['email'])
            return redirect(url_for("agent_home"))

@app.route("/sign_in/staff_home", methods=["POST", "GET"])
def staff_home():
    session['signin'] = query.sign_in_check(conn, session['email'],session["password"], 'booking_agent',session['airline_name'])
    session["user_type"] = 'airline_staff'
    session['signin'] = query.sign_in_check(conn, session['email'],session["password"], 'airline_staff',session['airline_name'])
    airlines = query.get_airlines(conn)
    cur_airline = query.get_cur_airline(conn,session)
    flight_cus = query.get_flight_cus(conn,session)
    locations = query.get_locations(conn)
    if not session["signin"] and request.method == 'GET':
        session["error"] = 'Invalid username or password, please try again.'
        return redirect(url_for("sign_in"))
    elif session["signin"] and request.method == "GET" or (session["signin"] and request.method=="POST" and request.form["submit_button"]=="clear_search"):
        data_dic = query.public_view(conn)
        locations = query.get_locations(conn)
        print(query.get_all_flight_num(conn))
        return render_template("homepage_staff.html",
                               departure_city=locations['departure_loc'],
                               arrival_city=locations['arrival_loc'],
                               all=data_dic,
                               error = session.get('createflighterror'),
                               airlines = airlines,
                               flight_num=query.get_all_flight_num(conn),
                               cur_airline = cur_airline,
                               flight_cus = flight_cus
                               )
    elif session["signin"] and request.method == "POST" and request.form["submit_button"] == "search":
        html_get = {'from': request.form.get('from'),
                    'to': request.form.get('to'),
                    'dt': request.form.get('date'),
                    'flight_num': request.form.get("flight_num")
                    }
        data_dic = query.filter_result(conn, html_get)
        return render_template("homepage_staff.html",
                               departure_city=locations['departure_loc'],
                               arrival_city=locations['arrival_loc'],
                               all=data_dic,
                               error = session.get('createflighterror'),
                               airlines = airlines,
                               cur_airline = cur_airline,
                               flight_cus = flight_cus,
                               flight_num=query.get_all_flight_num(conn),
                               )   
    elif session["signin"] and request.method == "POST" and request.form["submit_button"] == "modify":
        html_get = {'flight_num': request.form.get("flight_num"),
                    'status': request.form.get('status'),
                    }
        print(html_get)
        if html_get['flight_num'] is None or html_get['flight_num']  == '':
            success, err = False, 'Please enter both flight num and the customer email.'
            return redirect(url_for("staff_home"))
        else:
            query.change_flight_status(conn,html_get['flight_num'] , html_get['status'])
            return redirect(url_for("staff_home"))
            
        # create_para = {
        #     'flight_num': request.form.get("flight_c"),
        #     'price': request.form.get('price'),
        #     'departure_time': request.form.get("depdate"),
        #     'arrival_time': request.form.get('arrdate'),
        #     'departure': request.form.get('depplace'),
        #     'arrival': request.form.get('arrplace'),
        #     'plane': request.form.get('plane'),
        #     'status': request.form.get("status"),
        #     'planeid': request.form.get("planeid"),
        #     'seats' : request.form.get('seats')
        # }

        # if create_para['price']:
        #     if query.create_flight(conn, session, create_para['flight_num'], create_para["price"], create_para["departure_time"],create_para['arrival_time'],create_para['departure'][-3:], create_para['arrival'][-3:], create_para['plane']):
        #         return redirect(url_for('staff_home'))
        #     else:
        #         session['createflighterror'] = 'Create Flight failed'

        # if create_para["status"]:
        #     if query.change_flight_status(conn, create_para['flight_num'], create_para["status"]):
        #         return redirect(url_for('staff_home'))
        #     else:
        #         session["createflighterror"] = 'Update Status failed'

        # if create_para["seats"]:
        #     if query.add_airplane(conn,session, create_para["planeid"], create_para["seats"]):
        #         session['createflighterror'] = 'Add airplane'
        #     else:
        #         session["createflighterror"] = 'Update Status failed'
        return redirect(url_for("staff_home"))




@app.route("/sign_out", methods = ['POST','GET'])
def sign_out():
    if request.method == 'GET':
        session.clear()
        return render_template('sign_out.html')



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=9000,debug=True)