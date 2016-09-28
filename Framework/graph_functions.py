def get_all_cities(airline_network):
    city_names = []
    airline_nodes = airline_network.get_all_nodes()
    for city_code in airline_nodes:
        metro_data = airline_nodes[city_code].get_data()
        city_names.append([metro_data["code"], metro_data["name"]])
    return city_names


def hub_cities(airline_network):
    min_hub = int(raw_input("Minimum number of routes for hub: "))
    all_metros = airline_network.get_all_nodes().values()
    hubs = {}
    for metro in all_metros:
        connected_routes = metro.get_connected_nodes()
        num_routes = len(connected_routes)
        if num_routes >= min_hub:
            if num_routes in hubs:
                hubs[num_routes].append(metro.get_data()["name"])
            else:
                hubs[num_routes] = [metro.get_data()["name"]]
    return hubs


def cities_by_continent(airline_network):
    all_metros = airline_network.get_all_nodes().values()
    continents_served = {}
    for metro in all_metros:
        metro_data = metro.get_data()
        continent = metro_data["continent"]
        if continent in continents_served:
            continents_served[continent].append(metro_data["name"])
        else:
            continents_served[continent] = [metro_data["name"]]
    return continents_served


def average_population(airline_network):
    all_metros = airline_network.get_all_nodes().values()
    all_populations = 0
    num_cities = 0
    for metro in all_metros:
        metro_data = metro.get_data()
        all_populations += metro_data["population"]
        num_cities += 1
    return all_populations/num_cities


def smallest_city(airline_network):
    all_metros = airline_network.get_all_nodes().values()
    smallest_population = None
    for metro in all_metros:
        metro_data = metro.get_data()
        if not smallest_population or metro_data["population"] < smallest_population["population"]:
            smallest_population = metro_data
    return smallest_population["name"]


def biggest_city(airline_network):
    all_metros = airline_network.get_all_nodes().values()
    biggest_population = None
    for metro in all_metros:
        metro_data = metro.get_data()
        if not biggest_population or metro_data["population"] > biggest_population["population"]:
            biggest_population = metro_data
    return biggest_population["name"]


def average_distance(airline_network):
    all_metros = airline_network.get_all_nodes().values()
    total_distance = 0
    num_routes = 0
    for metro in all_metros:
        connected_routes = metro.get_connected_nodes()
        for destination in connected_routes:
            total_distance += connected_routes[destination]
            num_routes += 1
    return total_distance / num_routes


def get_shortest_single_flight(airline_network):
    all_metros = airline_network.get_all_nodes().values()
    shortest_distance = None
    start_city = None
    end_city = None
    for metro in all_metros:
        connected_routes = metro.get_connected_nodes()
        for destination in connected_routes:
            if not shortest_distance or shortest_distance > connected_routes[destination]:
                start_city = metro.get_data()["name"]
                end_city = destination.get_data()["name"]
                shortest_distance = connected_routes[destination]
    return "From %s to %s (%i)" % (start_city, end_city, shortest_distance)


def get_longest_single_flight(airline_network):
    all_metros = airline_network.get_all_nodes().values()
    longest_distance = None
    start_city = None
    end_city = None
    for metro in all_metros:
        connected_routes = metro.get_connected_nodes()
        for destination in connected_routes:
            if not longest_distance or longest_distance < connected_routes[destination]:
                start_city = metro.get_data()["name"]
                end_city = destination.get_data()["name"]
                longest_distance = connected_routes[destination]
    return "From %s to %s (%i)" % (start_city, end_city, longest_distance)


def get_statistic(statistic_code, airline_network):
    if statistic_code == 0:
        return get_longest_single_flight(airline_network)
    if statistic_code == 1:
        return get_shortest_single_flight(airline_network)
    if statistic_code == 2:
        return average_distance(airline_network)
    if statistic_code == 3:
        return biggest_city(airline_network)
    if statistic_code == 4:
        return smallest_city(airline_network)
    if statistic_code == 5:
        return average_population(airline_network)
    if statistic_code == 6:
        return cities_by_continent(airline_network)
    if statistic_code == 7:
        return hub_cities(airline_network)
