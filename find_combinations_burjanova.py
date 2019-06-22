from dateutil import parser
from datetime import datetime
import sys
import click


def time(duration):
    date_object = parser.parse(duratio
    date_object = datetime.timestamp(date_object)
    return date_object


def search_flights(flight, flight_input, result_flight_list, bags):
    for possible_flight in flight_input:
        delta = possible_flight[8]-flight[9]
        max_bags = min(int(possible_flight[6]), int(flight[6]))
        if (flight[1] == possible_flight[0]) and (delta >= 3600) and (delta <= 14400) and (bags <= max_bags):
            result_flight_list.append(possible_flight[4])
            return search_flights(possible_flight, flight_input, result_flight_list, bags)
    return result_flight_list


def check_flights(array, index_list, flights_list, bags):
    price_flight = []
    price_per_bag = []
    source_list = []
    destination_list = []
    for code in array:
        coord = index_list.index(code)
        source_list.append(flights_list[coord][0])
        destination_list.append(flights_list[coord][1])
        price_flight.append(int(flights_list[coord][5]))
        price_per_bag.append(int(flights_list[coord][7]))
    if len(array) > 3:
        if source_list[0] == destination_list[1] == destination_list[3]:
            pass
    else:
        final_price = sum(price_flight) + sum(price_per_bag)*bags
        sys.stdout.write("combination of flights: {} for 1 person with {} bags for {}\n".format(array, bags, final_price))


@click.command()
@click.option('--bags', default=1, help='How many bags do you have?')
def main(bags):
    data = sys.stdin.read().splitlines()
    if len(data) == 0:
        raise Exception('no data given to the script, try: cat input.csv | python3 find_combinations_burjanova.py --bags 1\n')
    flight_input = []
    iter_flights = iter(data)
    next(iter_flights)
    for line in iter_flights:
        line = line.split(',')
        line.append(time(line[2]))
        line.append(time(line[3]))
        flight_input.append(line)

    index = []
    for f in flight_input:
        index.append(f[4])

    result = []
    for first_flight in flight_input:
        flight_list = []
        flight_list.append(first_flight[4])
        result_to_be = search_flights(first_flight, flight_input, flight_list, bags)
        if len(result_to_be) > 1:
            result.append(result_to_be)

    for combination in result:
        check_flights(combination, index, flight_input, bags)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        sys.stderr.write(str(e))
