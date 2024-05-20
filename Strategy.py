import csv

class Strategy:
    hard_strategy = {}
    soft_strategy = {}
    pair_strategy = {}

    def __init__(self, player_file):
        self.player_file = player_file

    def get_st(self):
        hard = 21
        soft = 21
        pair = 20

        # Github Copilot
        with open(self.player_file, 'r') as player_csv:  # Open the player file
            reader = csv.DictReader(player_csv, delimiter=',')  # Create a CSV reader
            for row in reader:  # Iterate over each row in the CSV file
                if hard >= 5:  # Check if hard value is greater than or equal to 5
                    self.hard_strategy[hard] = row  # Add the row to the hard strategy dictionary
                    hard -= 1  # Decrement the hard value by 1
                elif soft >= 12:  # Check if soft value is greater than or equal to 12
                    self.soft_strategy[soft] = row  # Add the row to the soft strategy dictionary
                    soft -= 1  # Decrement the soft value by 1
                elif pair >= 4:  # Check if pair value is greater than or equal to 4
                    self.pair_strategy[pair] = row  # Add the row to the pair strategy dictionary
                    pair -= 2  # Decrement the pair value by 2

        return self.hard_strategy, self.soft_strategy, self.pair_strategy  # Return the strategy dictionaries
