from data.manage_tournament import ManageTournament
from screens.tournaments.view import TournamentView


def main():
    manager = ManageTournament()
    tview = TournamentView(manager)

    while True:
        print("\nMenu:")
        print("1. Create a New Tournament")
        print("2. Manage an Existing Tournament")
        print("3. List all Ongoing Tournaments")
        print("4. Remove a Tournament")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            manager.create_tournament()
        elif choice == '2':
            tview.manage_tournament()
        elif choice == '3':
            tview.get_tournament()
        elif choice == '4':
            manager.remove_tournament()
        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main()
