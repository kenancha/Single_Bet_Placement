import warnings
from pathlib import Path
import yaml
from yaml import SafeLoader
from src.utils.constants import MatchResult

project_path = Path.cwd()

def get_data(case):
    file_path = Path(project_path, "tests", "bet_placement", "cases.yaml")
    with open(file_path, encoding="utf-8") as f :
        try:
            _yaml = yaml.load(f,Loader=SafeLoader)
            _yaml=_yaml[case]
            return_list = []
            for data_set in _yaml:
                home = data_set["home"]
                away = data_set["away"]
                league = data_set["league"]
                stake = data_set["stake"]
                bet = data_set["bet"] if len(data_set["bet"]) == 1 else MatchResult[data_set["bet"].upper()].value
#                date = data_set["date"]
                return_list.append((home,away,league,stake,bet))
            return return_list
        except ValueError:
            warnings.warn(f"Case '{case}' does not exist in the file '{file_path}' or contains no data.")