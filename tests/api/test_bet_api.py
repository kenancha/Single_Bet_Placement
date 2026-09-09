import allure
from pytest_check import check

from src.utils.api.betting_api import BettingAPIClient


def test_place_bet_with_insufficient_balance(context_api):
    base_url = context_api.base_url
    header = context_api.header

    api = BettingAPIClient(base_url)
    with allure.step("Reset balance"):
        api.reset_balance(header=header)

    get_matches = api.get_matches(header)
    with allure.step("Get Matches"):
        assert get_matches.status_code == 200, "The endpoint to get the matches information couldn't be reached"
    match = get_matches.json()[0]
    match_info= {
        "matchId": match["id"],
        "selection": "HOME",
        "stake": 100
    }

    get_balance = api.get_balance(header)
    with allure.step("Get Balance"):
        assert get_balance.status_code == 200, "The endpoint to get the balance couldn't be reached"
    balance = get_balance.json()["balance"]
    with allure.step("Make bets to get the balance in threshold"):
        while balance > 100:
            bet = api.place_bet(payload=match_info, header=header)
            assert bet.status_code == 200
            get_balance = api.get_balance(header)
            assert get_balance.status_code == 200, "The endpoint to get the balance couldn't be reached"
            balance = get_balance.json()["balance"]
    insufficient_balance = api.place_bet(payload=match_info, header=header)
    with check, allure.step("Place a bet without enough balance"):
        assert insufficient_balance.status_code != 200, "The bet was placed without funds"

    with allure.step("Reset balance"):
        api.reset_balance(header=header)







