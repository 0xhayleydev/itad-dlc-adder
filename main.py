from IsThereAnyDeal.API import IsThereAnyDeal
from Utils.OAuthUtils.OAuth import OAuth


token = OAuth.authenticate_user()

print(token.access_token)
# app_id = "3656800" # input("Steam App ID: ")    # 3656800

# game = IsThereAnyDeal.get_game(app_id)

# dlcs = game.get_dlc_list()

# print(dlcs)