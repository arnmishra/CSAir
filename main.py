""" Main File to facilitate creation of Graph of Airlines and User Interaction """

from scripts.user_prompts import prompt_user_for_input
from scripts.graph_functions import add_file_data_to_graph


def main():
    """ Main function to create graph and prompt user for input. """
    airline_network = add_file_data_to_graph()
    while True:
        prompt_user_for_input(airline_network)

if __name__ == "__main__":
    main()
