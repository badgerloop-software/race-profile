import pandas as pd
import numpy as np
import argparse

from constants import *
from pathlib import Path

import MotorData as motor

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
    df['power_draw'] = df['motor_current'] * HV_PACK_VOLTAGE * UNIT_TO_KILO
    return df

def calculate_range(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the range of the vehicle
    """
    df['range'] = 0
    return df

def set_motor_current(df: pd.DataFrame) -> pd.DataFrame:
    """
    Set the motor current of the vehicle (in Amps)
    """
    df['motor_current'] = 50
    return df

def get_motor_torque(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the motor torque of the vehicle (in Newton-meters)
    """
    df['motor_torque'] = motor.calculated_torque_current(df['motor_current'])
    return df

def get_motor_RPM(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the motor RPM of the vehicle (in RPM)
    """
    df['motor_RPM'] = motor.calculated_RPM_current(df['motor_current'])
    return df

def get_motor_speed(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the motor speed of the vehicle (in m/s)
    """
    df['motor_speed'] = motor.calculated_speed_current(df['motor_current'])
    return df

def calculate_motor_cols(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the motor columns of the vehicle
    """
    df = set_motor_current(df)
    df = get_motor_torque(df)
    df = get_motor_RPM(df)
    df = get_motor_speed(df)
    return df


def main() -> None:
    df = create_run_profile()
    df = calculate_motor_cols(df)
    # df = calculate_range(df)
    df = calculate_power_draw(df)
    df = calculate_soc(df)
    print(df)

    print("Profile Length: {} seconds".format(len(df) * TIME_RES))
    print("Profile Length: %.2f minutes" % (len(df) / SECONDS_PER_MINUTE * TIME_RES))




if __name__ == "__main__":
    main()

