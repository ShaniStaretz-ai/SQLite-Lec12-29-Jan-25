def enter_new_car() -> None:
    pass


def end_treatment() -> None:
    pass


def remove_from_garage() -> None:
    pass


def test_load() -> None:
    pass


def print_options() -> None:
    print("1.enter car for treatment")
    print("2.end treatment")
    print("3.get your car from the garage")
    print("4.Treatment load test")
    print("5.exit")


print("welcome to Shani Garage:")
print("your options are:")
print_options()
while True:

    selected_option = input("please select one of the above options, here:")
    if selected_option == "5":
        print("goodbye!")
        break
    match selected_option:
        case "1":
            enter_new_car()
        case "2":
            end_treatment()
        case "3":
            remove_from_garage()
