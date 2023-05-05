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
        month_wise.append([start_date, end_date, 0])
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
    session.clear()
    return render_template("layout.html")

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
        return render_template("register.html")
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
            "airline_name": request.form.get("staff_airline")
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
        elif query.check_full(info_staff):
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
            "airline_name": request.form.get("airline_name")
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
    elif session["signin"] and request.method == "GET":
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
        if request.form["submit_button"] == "search":
            data_dic = query.filter_result(conn, html_get)
            html_get = {'from': request.form.get('from'),
                    'to': request.form.get('to'),
                    'dt': request.form.get('date'),
                    'flight_num':request.form.get("flight_num"),
                    'airline': request.form.get("airline")}
            flight_num = html_get["flight_num"]
            return render_template('homepage_customer.html',
                               # same results as
                               departure_city=locations['departure_loc'],
                               arrival_city=locations['arrival_loc'],
                               all=data_dic,
                               purchased = purchased_flight,
                               airlines = query.get_airlines(conn),
                               flight_num = query.get_flight_num(conn),
                               data_list = d)
        elif request.form["submit_button"] == "filter":
            start_date = request.form["start_date"]
            end_date = request.form["end_date"]
            data_dic = query.public_view(conn)
            # print(start_date, end_date)
            start_year, start_month = int(start_date[:4]), int(start_date[5:7])
            end_year, end_month = int(end_date[:4]), int(end_date[5:7])

            get_each_month(month_wise, start_year, start_month, end_year, end_month, start_date, end_date)
            print(month_wise)

            total_amount = query.get_my_spendings_total_amount(conn, session["email"], start_date, end_date)
            my_spendings = query.get_my_spendings_certain_range(conn, session["email"], start_date, end_date)
            # print(total_amount)
            update_month_wise_my_spendings(my_spendings, month_wise)
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



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=9000,debug=True)