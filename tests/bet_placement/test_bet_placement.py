import allure
import pytest
from pytest_check import check

from src.user_interface.pages.betting_page import BettingPage
from src.utils.api.betting_api import BettingAPIClient
from tests.data_providers.bet_placement import get_data

@pytest.mark.parametrize("bet_placement",get_data("betPlacement"))
def test_successful_single_bet(context, bet_placement):
    home = bet_placement[0]
    away = bet_placement[1]
    league = bet_placement[2]
    stake = bet_placement[3]
    bet = bet_placement[4]

    betting_page= BettingPage(context)
    with allure.step("Page open"):
        assert betting_page.page_opened(), "Betting page could not be loaded"

    betting_page.select_bet(league=league, home=home, away=away, odds=bet)

    betting_page.bet_slip_present()
    matchup = home + " vs " + away
    slip_matchup = betting_page.card_slip_matchup()
    with check, allure.step("Matchup in slip vs bet"):
        assert matchup == slip_matchup, f"Matchup displayed in the bet receipt does not match the selected matchup: Expected {matchup}, actual {slip_matchup}"
    with check, allure.step("Selected outcome in slip vs bet"):
        assert betting_page.card_slip_winner_comparison(), "Selected outcome does not match the bet slip"
    with check, allure.step("Odds in slip vs bet"):
        assert betting_page.card_slip_odds_comparison(), "Selected odds does not match the bet slip"

    odds= betting_page.get_odds()
    balance = betting_page.get_balance()

    betting_page.place_stake(stake)
    total_stake = betting_page.check_total_stake()
    with check, allure.step("Matchup in 'Total Stake' vs bet"):
        assert f"€{float(stake):.2f}" == total_stake, f"Stake shown in 'Total Stake' does not match the user's input: expected €'{float(stake):.2f}', found '{total_stake}'"
    with check, allure.step("Payout in slip"):
        assert betting_page.check_slip_payout(stake), "Potential payout is not calculated correctly"

    betting_page.click_place_bet()
    with check, allure.step("Message in receipt"):
        assert betting_page.bet_placed_successfully(), "Something went wrong placing the bet"
    with check, allure.step("Bet id in receipt"):
        assert betting_page.check_receipt_bet_id(), "The bet id didnt show up on the receipt"
    bet_matchup = betting_page.check_match()
    # todo: matchup in receipt is bugged
    with check, allure.step("Matchup in receipt vs bet"):
        assert matchup == bet_matchup, f"Matchup displayed in the bet receipt does not match the selected matchup: Expected {matchup}, actual {bet_matchup}"

    bet_stake = betting_page.check_stake()
    with check, allure.step("Stake in receipt vs input"):
        assert f"€{float(stake):.2f}" == bet_stake, f"Stake shown in receipt does not match the user's input. Expected €'{float(stake):.2f}', found '{bet_stake}'"

    receipt_odds = betting_page.check_odds()
    with check, allure.step("Odds in receipt vs bet"):
        assert str(odds) == receipt_odds, f'Odds shown in receipt does not match the expected. Expected "{odds}", actual "{receipt_odds}"'
    payout = float(odds) * float(stake)
    receipt_payout = betting_page.check_payout()

    with check, allure.step("Payout in receipt vs bet"):
    #todo: payout in receipt is bugged
        assert str(payout) == receipt_payout, f'Payout shown in receipt not calculated correctly. Expected {payout}, actual{receipt_payout}'
    with check, allure.step("Timestamp in receipt"):
        assert betting_page.check_timestamp(), 'There was a problem with the timestamp calculated in the receipt'
    betting_page.click_close_receipt()

    final_balance = betting_page.check_balance()
    calculated_balance = balance - float(stake)
    with check, allure.step("Check balance"):
    # todo: balance is bugged
        assert final_balance == calculated_balance, f"Balance is incorrect: expected '{calculated_balance}', found '{final_balance}'"

    