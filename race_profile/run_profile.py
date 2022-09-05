import pandas as pd
import numpy as np

from constants import *

def create_run_profile() -> pd.DataFrame:
    df = setup_dataframe() # Always start with this
    return df # Must return a dataframe of the run profile

def setup_dataframe() -> pd.DataFrame:
    """
    Setup the run profile dataframe with the correct timestamps
    """
    df = pd.DataFrame()
    df['ts'] = np.arange(0, PROFILE_LENGTH, TIME_RES)
    return df

def calculate_soc(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the State of Charge (SOC) of the battery
    """
    df.loc[0, 'kwh'] = STARTING_KWH
    df.loc[0, 'soc'] = STARTING_KWH / FULL_PACK_KWH
    for i in range(1, len(df)):
        df.loc[i, 'kwh'] = max(0, df.loc[i-1, 'kwh'] - df.loc[i, 'power_draw'] * TIME_RES / SECONDS_PER_HOUR)
        df.loc[i, 'soc'] = df.loc[i, 'kwh'] / FULL_PACK_KWH
    return df

def calculate_power_draw(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the power draw of the vehicle
    """
    df['power_draw'] = 10
    return df

def calculate_range(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the range of the vehicle
    """
    df['range'] = 0
    return df

def main():
    df = create_run_profile()
    df = calculate_power_draw(df)
    df = calculate_soc(df)
    df = calculate_range(df)
    print(df)




if __name__ == "__main__":
    main()

