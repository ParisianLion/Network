#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 20:31:22 2024

@author: lucanardinocchi

FileTitle : BuildingData
"""
import pandas as pd
from datetime import datetime, timedelta
import os
 
#CollectInformation

def collect_individual_data():
    fields = [
        'Individual ID', 'General Strengths (Vin)', 'General Weaknesses (Vout)', 
        'Romantic Ideals', 'ValueSystem', 'SelfPerception', 'OtherPerception', 
        'Occupation', 'Nationality', 'Origin', 'Family', 'Education', 
        'Travel', 'Partner', 'Media', 'Priviledge', 'Hobbies', 
        'FirstName', 'LastName', 'PhoneNumber'
    ]
    
    individual_data = {}
    
    print("Please enter the following information:")
    for field in fields:
        value = input(f"{field}: ")
        individual_data[field] = value
    
  
    individual_data['TimeOfMeet'] = datetime.now().strftime('%Y-%m-%d')
    
    return individual_data


#InsertIndividual

def insert_individual(file_path):

    df = pd.read_csv(file_path, sep=',', header=0, index_col=False)
    
    fields = df.columns.tolist()
    
    row_data = collect_individual_data()
    
    if 'TimeOfMeet' in fields:
        row_data['TimeOfMeet'] = datetime.now().strftime('%Y-%m-%d')
    
    new_row_df = pd.DataFrame([row_data], columns=df.columns)

    updated_df = pd.concat([df, new_row_df], ignore_index=True)

    updated_df.to_csv(file_path, index=False)

    individual_id = row_data['Individual ID']

    create_csv_r(f"/Users/lucanardinocchi/Desktop/Network/Data/Relationships/{individual_id}.csv")
    create_csv_t(f"/Users/lucanardinocchi/Desktop/Network/Data/Transcripts/{individual_id}.csv")


#UpdateIndividual

def update_individual(file_path):

    df = pd.read_csv(file_path, sep=',', header=0, index_col=False)
    
    unique_id_column = 'Individual ID'
    df[unique_id_column] = df[unique_id_column].astype(str)

    individual_id = str(input("Enter the individual ID to update: "))

    print("Available IDs:", df[unique_id_column].unique())

    if individual_id not in df[unique_id_column].values:
        print(f"Individual ID {individual_id} not found.")
        return
    
    fields = df.columns.tolist()

    print("Please enter the updated information:")
    updated_data = collect_updated_individual_data()

    if not updated_data:
        print("No updates provided.")
        return

    for key in updated_data.keys():
        if key not in df.columns:
            print(f"Warning: Column '{key}' does not exist in DataFrame.")
            return

    for field, value in updated_data.items():
        if field in df.columns:
            df.loc[df[unique_id_column] == individual_id, field] = value

    df.to_csv(file_path, index=False)
    print(f"Individual ID {individual_id} updated and saved to {file_path}")




def collect_updated_individual_data():
    updated_data = {}
    
    fields = [
        'Individual ID', 'General Strengths (Vin)', 'General Weaknesses (Vout)', 
        'Romantic Ideals', 'ValueSystem', 'SelfPerception', 'OtherPerception', 
        'Occupation', 'Nationality', 'Origin', 'Family', 'Education', 
        'Travel', 'Partner', 'Media', 'Priviledge', 'Hobbies', 
        'FirstName', 'LastName', 'PhoneNumber'
    ]
    
    for field in fields:
        if field != 'Individual ID':  # Skip the ID field
            value = input(f"Enter new value for {field} (or press Enter to keep current): ")
            if value:  # Only add to updated_data if value is not empty
                updated_data[field] = value
    return updated_data



#DeleteIndividual

def delete_individual(file_path):

    df = pd.read_csv(file_path, sep=',', header=0, index_col=False)

    unique_id_column = 'Individual ID'
    df[unique_id_column] = df[unique_id_column].astype(str)

    unique_id_value = str(input(f"Enter the {unique_id_column} to delete: "))

    print("Available IDs:", df[unique_id_column].unique())

    if unique_id_value not in df[unique_id_column].values:
        print(f"{unique_id_column} {unique_id_value} not found.")
        return

    df = df[df[unique_id_column] != unique_id_value]

    df.to_csv(file_path, index=False)
    print(f"Row with {unique_id_column} {unique_id_value} deleted and changes saved to {file_path}")




#CreateRelationshipCSV

def create_csv_r(file_path):
    
    fields = [
        'Date', 'Physical_Digital', 
        'D_Type', 'P_Action', 'P_Duration', 'P_VulnerabilitiesShared', 'P_Context', 'IdeasForFuture',
        'P_ProcessBefore?', 'P_ImageBuilt?', 'TsinceD', 'TsinceP', 'TsinceMet'
    ]
    
    df = pd.DataFrame(columns=fields)
    df.to_csv(file_path, index=False)
    print(f"CSV file created and saved to {file_path}")

#CreateConversationCSV

def create_csv_t(file_path):
    
    fields = [
        'Date', 'Sender', 'Message'
    ]
    
    df = pd.DataFrame(columns=fields)
    df.to_csv(file_path, index=False)
    print(f"CSV file created and saved to {file_path}")


#CollectInformation

def collect_interaction_data():
    fields = [
        'Date', 'Physical_Digital', 
        'D_Type', 'P_Action', 'P_Duration', 'P_VulnerabilitiesShared', 'P_Context', 'IdeasForFuture',
        'P_ProcessBefore?', 'P_ImageBuilt?'
    ]
    
    interaction_data = {}
    
    print("Please enter the following information:")
    for field in fields:
        value = input(f"{field}: ")
        interaction_data[field] = value
    
    interaction_data['Date'] = datetime.now().strftime('%Y-%m-%d')

    interaction_data['TsinceD'] = None
    interaction_data['TsinceP'] = None
    interaction_data['TsinceMet'] = None
    
    return interaction_data

#InsertInteraction

def insert_interaction(file_path):
    # Load the entire CSV file into a DataFrame
    df = pd.read_csv(file_path, sep=',', header=0, index_col=False)
    
    # Collect interaction data from user
    row_data = collect_interaction_data()
    
    # Ensure 'Date' is a datetime object
    current_date = pd.to_datetime(row_data['Date'], format='%Y-%m-%d')
    
    # Calculate last interaction dates
    if 'Physical_Digital' in df.columns:
        last_physical_date = df[df['Physical_Digital'] == 'P']['Date'].max()
        last_digital_date = df[df['Physical_Digital'] == 'D']['Date'].max()
    else:
        last_physical_date = df['Date'].max()
        last_digital_date = df['Date'].max()
    
    # Convert last dates to datetime objects or use default values
    last_physical_date = pd.to_datetime(last_physical_date, format='%Y-%m-%d') if not pd.isna(last_physical_date) else current_date - timedelta(days=1)
    last_digital_date = pd.to_datetime(last_digital_date, format='%Y-%m-%d') if not pd.isna(last_digital_date) else current_date - timedelta(days=1)
    
    # Calculate time since last interactions
    row_data['TsinceD'] = (current_date - last_digital_date).days
    row_data['TsinceP'] = (current_date - last_physical_date).days
    row_data['TsinceMet'] = (current_date - pd.to_datetime(row_data['Date'], format='%Y-%m-%d')).days
    
    # Create a DataFrame for the new row and append it to the existing DataFrame
    new_row_df = pd.DataFrame([row_data], columns=df.columns)
    updated_df = pd.concat([df, new_row_df], ignore_index=True)
    
    # Save the updated DataFrame back to the CSV file
    updated_df.to_csv(file_path, index=False)

def update_daily_csv(file_path):
    # Load the entire CSV file into a DataFrame
    df = pd.read_csv(file_path, sep=',', header=0, index_col=False)
    
    # Convert 'Date' column to datetime objects
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce')
    
    # Get the current date
    current_date = datetime.now()
    
    # Compute the last dates for physical and digital interactions
    if 'Physical_Digital' in df.columns:
        last_physical_date = df[df['Physical_Digital'] == 'P']['Date'].max()
        last_digital_date = df[df['Physical_Digital'] == 'D']['Date'].max()
    else:
        last_physical_date = df['Date'].max()
        last_digital_date = df['Date'].max()
    
    # Handle missing dates
    last_physical_date = last_physical_date if not pd.isna(last_physical_date) else current_date - timedelta(days=1)
    last_digital_date = last_digital_date if not pd.isna(last_digital_date) else current_date - timedelta(days=1)
    
    # Calculate time since last interactions
    time_since_last_physical = (current_date - last_physical_date).days
    time_since_last_digital = (current_date - last_digital_date).days
    
    # Calculate time since the earliest interaction
    earliest_date = df['Date'].min()
    time_since_met = (current_date - earliest_date).days if pd.notna(earliest_date) else 0
    
    # Create a new row with current date and calculated times
    new_row = {
        'Date': current_date.strftime('%Y-%m-%d'),
        'TsinceD': time_since_last_digital,
        'TsinceP': time_since_last_physical,
        'TsinceMet': time_since_met,
        'Physical_Digital': None,
        'D_Type': None,
        'P_Action': None,
        'P_Duration': None,
        'P_VulnerabilitiesShared': None,
        'P_InternalExperience': None,
        'P_ProcessBefore?': None,
        'IdeasForFuture': None
    }
    
    # Convert the new row to a DataFrame
    new_row_df = pd.DataFrame([new_row], columns=df.columns)
    
    # Use .loc to append the new row
    df.loc[len(df)] = new_row_df.iloc[0]
    
    # Save the updated DataFrame back to the CSV file
    df.to_csv(file_path, index=False)
    print(f"New row added and saved to {file_path}")
#UpdateConversationsDaily







