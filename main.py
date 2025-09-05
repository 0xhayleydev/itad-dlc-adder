from pathlib import Path

from IsThereAnyDeal.API import IsThereAnyDeal
from IsThereAnyDeal.Config import Config
from Utils.OAuth import OAuth


def main():
    config_file = Path("./config.json")
    Config.load(config_file)

    token = OAuth.authenticate_user()

    if not token:
        print("Could not get token.")
        return

    print(token.access_token)
    app_id = "3656800" # input("Steam App ID: ")    # 3656800

    game = IsThereAnyDeal.get_game(app_id)

    print(game.title)

if __name__ == "__main__":
    main()
