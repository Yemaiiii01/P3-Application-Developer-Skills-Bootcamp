import os
import json
from models.tournament import Tournament
from models.player import Player
from models.match import Match


class ManageTournament:
    def __init__(self):
        self.tournaments = {}
        self.all_players = []
        self.load_all_clubs()
        self.load_all_tournaments()

    def load_all_clubs(self):
        base_path = r"data/clubs"
        club_files = ["cornville.json", "springfield.json", "SKC.json"]
        for club_file in club_files:
            club_name, club_players = self.load_club(
                os.path.join(base_path, club_file))
            self.all_players.extend(club_players)

    def load_club(self, file_path):
        # Reads player data from a club file and returns the club's name and its players.
        with open(file_path, 'r') as file:
            data = json.load(file)
            players = [Player(player['name'], player['email'], player['chess_id'], player['birthday'])
                       for player in data['players']]
            return data["name"], players

    def create_tournament(self):
        # Creates a new tournament based on user input.
        # Handles tournament creation including venue, dates, player selection, and max rounds.
        tournament_name = input(
            "Enter the name of the new tournament: ").strip()
        venue = input("Enter the venue for the tournament: ").strip()
        start_date = input("Enter the start date (YYYY-MM-DD): ").strip()
        end_date = input("Enter the end date (YYYY-MM-DD): ").strip()

        if tournament_name in self.tournaments:
            print(f"Tournament '{tournament_name}' already exists.")
            return

        num_players = 0
        while num_players % 2 != 0 or num_players <= 0:
            num_players = int(
                input("Enter the number of players to select (must be an even number): "))
        selected_players = self.select_players(num_players)

        max_rounds = int(input("Enter the maximum number of rounds: "))

        new_tournament = Tournament(
            tournament_name, venue, start_date, end_date, selected_players, max_rounds)
        self.tournaments[tournament_name] = new_tournament
        # Save tournament information to a JSON file
        self.save_tournament_to_json(new_tournament)

        print(f"Tournament '{tournament_name}' has been created at {venue} from {start_date} to {end_date}.")

    def save_tournament_to_json(self, tournament):
        # Save tournament information to a JSON file using its name
        file_name = f"{tournament.name}_info.json"
        file_path = os.path.join("data/tournaments/", file_name)

        tournament_info = {
            "name": tournament.name,
            "dates": {
                "from": tournament.start_date,
                "to": tournament.end_date
            },
            "venue": tournament.venue,
            "number_of_rounds": tournament.max_round,
            "current_round": tournament.current_round,
            "completed": tournament.is_completed(),
            "players": [player.chess_id for player in tournament.players],
            "rounds": []
        }

        for round_matches in tournament.rounds:
            round_info = []
            for match in round_matches:
                match_info = {
                    "players": [match.player1.chess_id, match.player2.chess_id],
                    "completed": match.played,
                    "winner": match.result
                }
                round_info.append(match_info)
            tournament_info["rounds"].append(round_info)

        try:
            with open(file_path, 'w') as file:
                json.dump(tournament_info, file, indent=4)
            print(f"Tournament information saved in {os.path.abspath(file_path)}")
        except Exception as e:
            print(f"Failed to save tournament information: {e}")

    def play_next_round(self, tournament):
        # Handles the gameplay for the next round in the given tournament.
        # Processes match results based on user input.
        print(f"Attempting to play round {tournament.current_round + 1}.\n"
              f"Current round: {tournament.current_round}\n"
              f"Max rounds: {tournament.max_round}")

        if tournament.current_round >= tournament.max_round:
            print("Maximum number of rounds reached. The tournament has concluded.")
            tournament.declare_winner()
            return

        tournament.play_round()

        # Adjusted the index to access the correct round
        current_round_index = tournament.current_round - 1
        if 0 <= current_round_index < len(tournament.rounds):
            current_round = tournament.rounds[current_round_index]

            for i, match in enumerate(current_round, start=1):
                if not match.was_played():
                    print(f"Match {i}: {match.player1.name} vs {match.player2.name}")
                    while True:
                        result = input("Enter winner (1 for player1, 2 for player2, 0 for draw): ").strip()
                        if result in ["1", "2", "0"]:
                            if result == "1":
                                match.play_match("player1")
                            elif result == "2":
                                match.play_match("player2")
                            else:
                                match.play_match("draw")
                            break
                        else:
                            print("Invalid input. Please enter 1, 2, or 0.")

        print(f"After Round {tournament.current_round}:")

        self.save_tournament_to_json(tournament)
        tournament.display_rankings()

        if tournament.current_round == tournament.max_round:
            print("Maximum number of rounds reached. The tournament has concluded.")
            tournament.declare_winner()

    def view_player_details(self, tournament_name):
        # Displays details of all players participating in a specific tournament.
        tournament = self.tournaments.get(tournament_name)
        if not tournament:
            print(f"No tournament found with the name '{tournament_name}'.")
            return

        print(f"Player details for {tournament.name}:")
        for player in tournament.players:
            print(player)

    def select_players(self, num_players):
        # Selects players for a tournament based on user input.
        selected_players = []
        while len(selected_players) < num_players:
            search_term = input(
                "Enter a name or chess ID to search, or just press enter to list all players: ")
            display_list = self.search_players(
                search_term) if search_term else self.all_players

            for i, player in enumerate(display_list, 1):
                print(f"{i}: {player.name} ({player.chess_id})")

            player_index = int(
                input(f"Select player {len(selected_players) + 1} (enter number): ")) - 1
            if 0 <= player_index < len(display_list):
                selected_player = display_list[player_index]
                if selected_player not in selected_players:
                    selected_players.append(selected_player)
                    self.display_selected_players(selected_players)
                else:
                    print("Player already selected. Please choose a different player.")
            else:
                print("Invalid player number. Please try again.")
        return selected_players

    def display_selected_players(self, selected_players):
        # Displays a list of currently selected players for the tournament.
        print("\nCurrently selected players:")
        for i, player in enumerate(selected_players, 1):
            print(f"{i}: {player.name} ({player.chess_id})")
        print()

    def view_tournament_report(self, tournament_name):
        # Displays a detailed report of a specific tournament.
        tournament = self.tournaments.get(tournament_name)
        if not tournament:
            print(f"No tournament found with the name '{tournament_name}'.")
            return

        self.create_tournament_report_html(tournament)

    def create_tournament_report_html(self, tournament):
        # Creates an HTML template for the tournament report.
        report_content = self.generate_tournament_report(tournament)

        file_name = f"{tournament.name}_report.html"
        file_path = os.path.join(
            "data/tournaments/tournament_reports", file_name)

        try:
            with open(file_path, 'w') as file:
                file.write(report_content)
            print(f"Tournament report saved in {os.path.abspath(file_path)}")
            print("The Tournament Report has been generated successfully")
            print("Check your tournament reports folder")
        except Exception as e:
            print(f"Failed to save tournament report: {e}")

    def generate_tournament_report(self, tournament):
        # Generates the content for the HTML tournament report.
        report_content = f"<html>\n<head>\n<title>Tournament Report - {
            tournament.name}</title>\n</head>\n<body>\n"
        report_content += f"<h1>Tournament Report: {tournament.name}</h1>\n"
        report_content += f"<p>Dates: {
            tournament.start_date} to {tournament.end_date}</p>\n"
        report_content += f"<p>Venue: {tournament.venue}</p>\n"
        report_content += f"<p>Current Round: {
            tournament.current_round}/{tournament.max_round}</p>\n"

        report_content += "<h2>Players (sorted by points)</h2>\n"
        sorted_players = sorted(
            tournament.players, key=lambda x: x.points, reverse=True)
        report_content += "<ul>\n"
        for player in sorted_players:
            report_content += f"<li>{
                player.name} (Points: {player.points})</li>\n"
        report_content += "</ul>\n"

        report_content += "<h2>Rounds and Matches</h2>\n"
        for round_num, round_matches in enumerate(tournament.rounds, start=1):
            report_content += f"<h3>Round {round_num}</h3>\n<ul>\n"
            for match in round_matches:
                match_info = f"{match.player1.name} vs {match.player2.name}"
                if match.played:
                    result = f"Result: {match.result}"
                else:
                    result = "Not played yet"
                report_content += f"<li>Match: {match_info}, {result}</li>\n"
            report_content += "</ul>\n"

        report_content += "</body>\n</html>"
        return report_content

    def load_all_tournaments(self):
        tournament_files = [file for file in os.listdir(
            "data/tournaments") if file.endswith("_info.json")]
        for file_name in tournament_files:
            tournament_name = file_name.replace("_info.json", "")
            self.load_tournaments(os.path.join(
                "data/tournaments", file_name), tournament_name)

    def load_tournaments(self, file_path, tournament_name):
        """Loads a tournament from a JSON file."""
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            players = []
            for player_id in data['players']:
                # Assuming 'players' in the JSON file contains a list of player IDs
                player = next(
                    (p for p in self.all_players if p.chess_id == player_id), None)
                if player:
                    players.append(player)

            new_tournament = Tournament(
                data['name'],
                data['venue'],
                data['dates']['from'],
                data['dates']['to'],
                players,
                data['number_of_rounds']
            )

            # Add the missing attributes
            new_tournament.current_round = data.get('current_round', 0)

            # Update rounds based on the loaded data
            for round_matches in data.get('rounds', []):
                round_info = []
                for match_info in round_matches:
                    player1_id, player2_id = match_info["players"]
                    player1 = next(
                        (p for p in new_tournament.players if p.chess_id == player1_id), None)
                    player2 = next(
                        (p for p in new_tournament.players if p.chess_id == player2_id), None)

                    winner = match_info.get("winner")

                    # Create a match object and update its state
                    match = Match(player1, player2)
                    match.play_match(winner)

                    round_info.append(match)

                new_tournament.rounds.append(round_info)

            self.tournaments[tournament_name] = new_tournament
            print(f"Tournament '{tournament_name}' loaded from {file_path}.")
        except FileNotFoundError:
            print(f"No tournament file found for '{tournament_name}'.")
        except Exception as e:
            print(f"Error loading tournament '{tournament_name}': {e}")

    def remove_tournament(self):
        # Removes a tournament from the tournaments list based on user input.
        if not self.tournaments:
            print("There are no ongoing tournaments to remove.")
            return

        tournament_name = input(
            "Enter the name of the tournament to remove: ").strip()
        if tournament_name in self.tournaments:
            # removed_tournament = self.tournaments.pop(tournament_name)
            print(f"Tournament '{tournament_name}' has been removed.")

            # Rename the JSON file
            old_file_path = os.path.join(
                "data/tournaments", f"{tournament_name}_info.json")
            new_file_path = os.path.join(
                "data/tournaments", f"{tournament_name}_info_removed.json")

            try:
                os.rename(old_file_path, new_file_path)
                print(f"File '{tournament_name}_info.json' renamed to '{tournament_name}_info_removed.json'")
            except Exception as e:
                print(f"Failed to rename tournament file: {e}")
        else:
            print(f"No tournament found with the name '{tournament_name}'.")

    def search_players(self, search_term):
        # Searches and returns players matching the given search term (name or chess ID).
        return [player for player in self.all_players
                if search_term.lower() in player.name.lower() or search_term.lower() in player.chess_id.lower()]
