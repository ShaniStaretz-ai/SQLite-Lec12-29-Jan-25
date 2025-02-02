import sqlite3


def enter_new_car(_cursor, _conn) -> None:
    try:
        car_number = input("please enter your Vehicle registration number:")
        problem = input("please describe the vehicle issue:")
        owner_phone = input("please enter your contact number:")
        insert_query = '''
            INSERT INTO garage (car_number, car_problem, fixed,owner_ph)
            values (?,?,0,?) '''
        _cursor.execute(insert_query, (car_number, problem, owner_phone))
        _conn.commit()
    except sqlite3.IntegrityError:
        print("this car number is already exist in the system")


def end_treatment(_cursor, _conn) -> None:
    car_number = input("please enter your Vehicle registration number:")
    get_car_query='''
    SELECT fixed,car_number 
    FROM garage
    WHERE car_number=?
    '''
    cursor.execute(get_car_query,(car_number,))
    rows_results = cursor.fetchone()
    if rows_results['fixed']!=0:# TRUE=1,0=FALSE
        print("the car is already fixed")
    else:
        update_car_status_query='''
        update garage set fixed=1 WHERE car_number=?
        '''
        cursor.execute(update_car_status_query, (car_number,))
        _conn.commit()
        print("the treatment was ended")


def remove_from_garage(_cursor, _conn) -> None:
    car_number = input("please enter your Vehicle registration number:")
    get_car_query = '''
        SELECT fixed,car_number,owner_ph 
        FROM garage
        WHERE car_number=?
        '''
    cursor.execute(get_car_query, (car_number,))
    rows_results = cursor.fetchone()
    if rows_results['fixed']!=1:# TRUE=1,0=FALSE
        print("the treatment is not completed yet")
    print(f"the treatment ended, contact the owner number {rows_results['owner_ph']}")
    delete_car_query='''
    DELETE FROM garage
    where car_number=?
    '''
    cursor.execute(delete_car_query, (car_number,))
    _conn.commit()

def test_load(_cursor) -> None:
    get_pending_treatment_query='''
    SELECT COUNT(*) as car_count
    FROM garage
    where fixed=0
    '''
    cursor.execute(get_pending_treatment_query, )
    rows_results = cursor.fetchone()
    print(f"there are {rows_results['car_count']} cars pending for treatment")



def print_options() -> None:
    print("1.enter car for treatment")
    print("2.end treatment")
    print("3.get your car from the garage")
    print("4.Treatment load test")
    print("5.exit")


conn = sqlite3.connect('29_01_2025.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("welcome to Shani Garage:")
print("your options are:")

while True:
    print_options()
    selected_option = input("please select one of the above options, here:")
    if selected_option == "5":
        print("goodbye!")
        break
    match selected_option:
        case "1":
            enter_new_car(cursor, conn)
        case "2":
            end_treatment(cursor, conn)
        case "3":
            remove_from_garage(cursor, conn)
        case "4":
            test_load(cursor)
conn.close()
