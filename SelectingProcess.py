#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 20:31:44 2024

@author: lucanardinocchi

FileTitle: SelectingProcess
"""

import pandas as pd

#GetInformationIndividual

def get_info_individual(file_path, individual_ID):

    df = pd.read_csv(file_path)
    
    if individual_ID < 0 or individual_ID >= len(df):
        raise IndexError("Row index out of range.")
    
    row_dict = df.iloc[individual_ID].to_dict()
    
    return row_dict


#GetInformationRelationship

def get_info_interaction(file_path, num_rows=2):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Check if num_rows is greater than the available rows
    if num_rows > len(df):
        raise ValueError("Number of rows to select exceeds the number of available rows.")
    
    # Select the two most recent rows
    recent_rows = df.tail(num_rows)
    
    # Create a dictionary to store the results
    result_dict = {col: recent_rows[col].tolist() for col in df.columns}
    
    return result_dict

#GetInformationConversation





#CreateInformationDict

def combine_info(file_path1, file_path2, individual_ID, num_rows=2):

    individual_info = get_info_individual(file_path1, individual_ID)
    
    recent_info = get_info_interaction(file_path2, num_rows)
    
    combined_info = {**individual_info, **recent_info}
    
    return combined_info


#SelectAction

def select_action(df):
    # Check if the DataFrame is empty
    if df.empty:
        print("DataFrame is empty. No action can be selected.")
        return None

    # Get the last row of the DataFrame
    last_row = df.iloc[-1]

    # Initialize condition_id
    condition_id = None

    # Ensure 'TsinceMet' is a scalar value
    since_met = last_row.get('TsinceMet')
    
    if isinstance(since_met, list):
        print("Unexpected list type for 'TsinceMet'. Handling as a single value.")
        # Handle the list case here if needed, for now, we'll convert it to a single value or handle it appropriately
        since_met = since_met[0] if since_met else None
    
    # Check conditions based on the last row's values
    if since_met == 1:
        condition_id = 1
    elif since_met == 3:
        condition_id = 2
    elif since_met == 10:
        condition_id = 3
    elif since_met == 30:
        condition_id = 4
    elif since_met in {50, 100, 150, 200, 250, 300, 350}:
        condition_id = 5
    elif since_met > 30 and last_row.get('TsinceLastP', 0) == 1:
        condition_id = 6
    elif since_met > 30 and last_row.get('TsinceLastP', 0) > 5 and last_row.get('TsinceLastD', 0) > 17:
        condition_id = 7
    elif since_met > 30 and last_row.get('TsinceLastP', 0) > 22:
        condition_id = 8
    else:
        # No condition matched
        condition_id = 0

    return condition_id



