import re
from datetime import datetime, timedelta
from src.user_interface.base_page import BasePage
from src.user_interface.pages.locators import BettingLocators
from src.utils.constants import MatchResult

class BettingPage(BasePage):
    """Page object model for the betting page."""

    def __init__(self, driver):
        super().__init__(driver)
        self.__locators = BettingLocators()

    def page_opened(self):
        return self.element_present(self.__locators.LBL_TITLE)

    def select_bet(self, league, home, away, odds):
        match_card = self.format_locator(self.__locators.CRD_MATCH, {"league":league,"home":home, "away":away})
        odds = self.format_locator(self.__locators.BTN_ODDS,{"odds":odds})
        self.wait_for_clickable((odds[0], match_card[1]+odds[1]))
        self.driver.find_element(odds[0], match_card[1]+odds[1]).click()

    def bet_slip_present(self):
        return self.element_present(self.__locators.BET_SLIP)

    def card_slip_matchup(self):
        return self.finds_element(self.__locators.BET_TEAMS).text

    def card_slip_winner_comparison(self):
        winner_selected = self.finds_element(self.__locators.LBL_SELECTED_TEAM)
        return self.finds_element(self.__locators.BET_WINNER).text.strip()[-4:].capitalize() == MatchResult(winner_selected.text).name.capitalize()

    def card_slip_odds_comparison(self):
        odds_selected = self.finds_element(self.__locators.LBL_SELECTED_ODDS)
        odds_bet = self.finds_element(self.__locators.BET_ODDS)
        return odds_selected.text == re.search(r"[\d.]+", odds_bet.text).group()

    def get_odds(self):
        return self.finds_element(self.__locators.LBL_SELECTED_ODDS).text

    def get_balance(self):
        return float(re.search(r"[\d.]+", self.finds_element(self.__locators.LBL_BALANCE).text).group())

    def place_stake(self, stake):
        self.finds_element(self.__locators.TXT_STAKE).send_keys(stake)

    def check_total_stake(self):
        return self.finds_element(self.__locators.LBL_TOTAL_STAKE).text

    def check_slip_payout(self,stake):
        odds_x_stake = float(stake) * float(self.finds_element(self.__locators.LBL_SELECTED_ODDS).text)
        return str(odds_x_stake) == re.search(r"[\d.]+", self.finds_element(self.__locators.LBL_PAYOUT).text).group()

    def click_place_bet(self):
        self.finds_element(self.__locators.BTN_PLACE_BET).click()

    def placing_bet(self):
        self.wait_for_visibility(self.__locators.BTN_PLACING)
        self.wait_for_invisibility(self.__locators.BTN_PLACING)

    def bet_placed_successfully(self):
        self.wait_for_visibility(self.__locators.LBL_BET_PLACED_SUCCESSFULLY)
        return self.element_present(self.__locators.LBL_BET_PLACED_SUCCESSFULLY)

    def check_receipt_bet_id(self):
        return self.element_present(self.__locators.RCPT_BET_ID)

    def check_match(self):
        return self.finds_element(self.__locators.RCPT_MATCH).text

    #selection missing from receipt
    def check_selection(self):
        pass

    def check_stake(self):
        return self.finds_element(self.__locators.RCPT_STAKE).text

    def check_odds(self):
        return self.finds_element(self.__locators.RCPT_ODDS).text

    def check_payout(self):
        return self.finds_element(self.__locators.RCPT_PAYOUT).text

    def check_timestamp(self):
        return (self.finds_element(self.__locators.RCPT_TIMESTAMP).text == f"TODAY, {datetime.now().strftime('%H:%M')}") or (self.finds_element(self.__locators.RCPT_TIMESTAMP).text == f"TODAY, {(datetime.now() - timedelta(minutes=1)).strftime('%H:%M')}")

    def click_close_receipt(self):
        self.finds_element(self.__locators.RCPT_CLOSE).click()
        self.wait_for_invisibility(self.__locators.LBL_BET_PLACED_SUCCESSFULLY)

    def check_balance(self):
        return float(re.search(r"[\d.]+", self.finds_element(self.__locators.LBL_BALANCE).text).group())


