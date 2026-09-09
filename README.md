# Single Bet Placement Feature

This project contains a minimal project scaffold for automating single bet placement tests using a page object model and a betting API client.

## Preconditions and set-up
The Python version needed is 3.11
Installations steps within the project:
- Create a virtual environment
- Open a terminal and activate the virtual environment  
```bash
  .venv\Scripts\activate
```
- Install requirements `pip install -U -r requirements.txt`
- Set the project root as working directory 
  - Recommended IDE: Pycharm

## Structure

- `src/user_interface/pages/betting_page.py` - Page object for the betting UI
- `src/utils/api/betting_api.py` - HTTP client for bet-related API calls
- `tests/bet_placement/test_bet_placement.py` - UI tests for placing a bet
- `tests/api/test_bet_api.py` - API tests for insufficient balance

## Running tests
Option 1: 
Use the terminal to run:
- All the tests 
```bash
  pytest
```
- Specific file 
```bash
  pytest tests/bet_placement/test_bet_placement.py
```
- Particular test
```bash
  pytest tests/bet_placement/test_bet_placement.py::test_successful_single_bet
```

Option 2: Use the IDE tools to run each test. 

## Generating the report

Allure automatically collects the test evidence when required.

To generate the report, run:

```bash 
  allure generate --clean --single-file
```

This generates a single `.html` file that includes the test results and images, making it easier to share when needed.

