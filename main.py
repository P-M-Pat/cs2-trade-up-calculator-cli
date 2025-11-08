import statistics
import argparse


def print_horizontal_line():
    print("----------------------------------------------------------------")

def ordinal_suffix(num: int) -> str:
    '''
    Returns the string representation of the given integer with an ordinal suffix (st, nd, rd, th)

    :param num: The input number
    :raises ValueError: If the input number is negative or not an integer
    :return: The number as a string with its ordinal suffix
    '''
    if num < 0 or not isinstance(num, int):
        raise ValueError("Please Enter a positive integer!!!")

    last_two_digits = num % 100
    last_digit = last_two_digits % 10
    
    suffix_dict = {
        1: "st", 
        2: "nd", 
        3: "rd"
    }

    match last_two_digits:
        case 11 | 12 | 13:
            return f"{num}th"
        case _:
            return f"{num}{suffix_dict.get(last_digit, "th")}"
        

def input_and_validate(prompt: str) -> tuple[float, ...]:
    '''
    Prompts the user to enter one or more numbers, splitting them by spaces and
    validates that all numbers are in the [0, 1] interval.

    :param prompt: The prompt to be used in the input() function
    :return: a tuple of valid floats
    '''
    valid = False
    while not valid:
         user_input = input(prompt)
         try:
             numbers = tuple(map(float, user_input.split()))
             
             if not numbers:
                 print("Empty input! Try again.")
                 continue
             
             if all(0 <= num <= 1 for num in numbers):
              valid = True
             else:
                 print("All numbers must be in the [0, 1] interval.")
         except ValueError:
             print("ERROR! Inputs must only contain numbers")
    return numbers

def normalize_float(skin_float: float, float_min: float, float_max: float) -> float:    
    '''
    Returns the normalized skin float 

    :param skin_float: the float value for the skin
    :param float_min: the minimum value for the skin float range
    :param float_max: the maximum value for the skin float range
    :raises ValueError: if the minimum value is greater than the maximum value or the skin float is greater than the max value
    :return: a normalized float in the [0, 1] interval
    '''
    if float_min >= float_max or skin_float > float_max:
        raise ValueError("minimum value must not be greater than or equal to the maximum value")

    result = (skin_float - float_min)/(float_max - float_min)
    return result

def get_trade_float(ordinal = "") -> float:
    '''
    Gets the skin float and its float range values from the user, normalizing the skin float and 
    returns the trade float

    :param ordinal(optional): when used in trade up contract
    :return: The trade float
    '''
    skin_float = input_and_validate(f"enter the {ordinal} skin float:  ")[0]
    float_min, float_max = input_and_validate(f"enter the float range(space separated): ")
    trade_float = normalize_float(skin_float=skin_float, float_min=float_min, float_max=float_max)
    return trade_float
        
def calculate_trade_up_avg() -> float:
    '''
    Gets 10 input skin floats and their float ranges and calculates their trade floats and returns the trade up average float

    :return: the trade up average float value
    '''
    trade_floats = []
    for i in range(10):
        ordinal_num = ordinal_suffix(i+1)
        trade_float = get_trade_float(ordinal=ordinal_num)
        trade_floats.append(trade_float)
        print(f"the {ordinal_num} trade float is {trade_float}")
        print_horizontal_line()
    trade_up_avg = statistics.mean(trade_floats)
    return trade_up_avg


def calculate_output_float(input_trade_up_avg: float) -> float:
    '''
    Gets the expected output skin's float range from the user and returns its expected float based on the given input average float

    :param input_trade_up_avg: The average input float
    :return: the float value of the expected output skin
    '''
    output_float_min, output_float_max = input_and_validate(f"enter the output float range: ")
    output_float = (input_trade_up_avg * (output_float_max - output_float_min)) + output_float_min
    return output_float

def main(mode: str):
    match mode:
        case "output":
            input_avg = float(input("Enter the input tradeup average value: "))
            output_float = calculate_output_float(input_trade_up_avg=input_avg)
            print(f"The expected output float is {output_float}")
        case "float":
            print(get_trade_float())
        case "contract":
            tradeup_avg = calculate_trade_up_avg()
            print(f"avg trade up float: {tradeup_avg}")

if __name__=="__main__":
    parser = argparse.ArgumentParser(
        prog="CS2 Trade Up calculator", 
        usage="%(prog)s [-h] mode", 
        description="Some simple useful tools for CS2 Trade Ups.", 
        epilog=("Use 'contract' to get the average trade float of 10 input skins, "
                "'output' to calculate the output float of the expected skin based on an input avg float, "
                "or 'float' to calculate the trade float of an input skin")
    )
    parser.add_argument("mode", 
                        choices=["output", "float", "contract"], 
                        help="the operation mode. Must be one of: output, float or contract")
    
    args = parser.parse_args()
    main(mode=args.mode)
