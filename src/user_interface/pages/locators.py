from selenium.webdriver.common.by import By

class BettingLocators:
    LBL_TITLE = (By.XPATH, '//title[text()="Sports Betting QA"]')
    LBL_BALANCE = (By.XPATH,'//*[contains(text(),"Balance:")]')

    #CRD
    CRD_MATCH = (By.XPATH,'//span[text()= "{league}"]/parent::*/following-sibling::div[@class="teams"]//span[text()="{home}"]/../following-sibling::*/span[text()="{away}"]/ancestor::div[@class="card matchCard"]')
 #   LBL_BADGE = (By.XPATH,'//span[@class="badge"]')
    LBL_TEAMS = (By.XPATH,'//div[@class="teamName"]')
    BTN_ODDS = (By.XPATH,'//span[@class="oddsButtonLabel" and text()="{odds}"]')
    LBL_SELECTED_TEAM = (By.XPATH,'//button[@class = "oddsButton oddsButtonSelected"]/span[@class="oddsButtonLabel"]')
    LBL_SELECTED_ODDS = (By.XPATH,'//button[@class = "oddsButton oddsButtonSelected"]/span[@class="oddsButtonValue"]')

    #SLIP
    BET_SLIP = (By.XPATH,'//div[@class="betSlipContent"]')
    BET_TEAMS = (By.XPATH,'//div[@class="betSelectionTeams"]')
    BET_WINNER = (By.XPATH,'//div[@class="betSelectionMarket"]')
    BET_ODDS = (By.XPATH,'//span[@class="betSelectionOdds"]')
    TXT_STAKE = (By.ID,'bet-slip-stake-input')
    LBL_TOTAL_STAKE = (By.ID,'bet-slip-total-stake')
    LBL_PAYOUT = (By.ID,'bet-slip-potential-payout')
    BTN_PLACE_BET = (By.ID,'bet-slip-place-bet')
    BTN_PLACING = (By.XPATH,'//span[@class="placeBetButtonPlacing"]')


    #RECEIPT
    LBL_BET_PLACED_SUCCESSFULLY = (By.XPATH,'//h2[contains(text(),"Bet Placed Successfully")]')
    RCPT_BET_ID = (By.ID,'modal-success-bet-id')
    RCPT_MATCH = (By.ID,'modal-success-match')
    RCPT_STAKE = (By.ID,'modal-success-stake')
    RCPT_ODDS = (By.ID,'modal-success-odds')
    RCPT_PAYOUT = (By.ID,'modal-success-payout')
    RCPT_TIMESTAMP = (By.ID,'modal-success-placed-at')
    RCPT_CLOSE = (By.ID,'modal-success-close')