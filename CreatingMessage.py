#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 20:32:01 2024

@author: lucanardinocchi

FileTitle: CreatingMessage
"""

from transformers import pipeline
import random
import csv
import pandas as pd
import os
import subprocess
from datetime import datetime
import shutil
import requests


#DefineAction

def get_action_prompt(condition_id):
    # Define action prompts within the function
    action_prompts = {
        1: "Write a text to let a friend know it was cool to meet them",
        2: "Write a text to send a friend an article I found that might be of interest",
        3: "Write a text to invite a friend to a catch up",
        4: random.choice([
            "Write a text to check-in with a friend",
            "Write a text to recommend a book to a friend",
            "Write a text to send an interesting quote to a friend"
        ]),
        5: "Write a text to a friend to ask a follow-up question based on a previous conversation",
        6: "Write a text to a friend to remind them of a cool memory we share together based on previous interactions",
        0: "Default Action Prompt"
    }
    
    # Return the action prompt based on the condition_id
    return action_prompts.get(condition_id, "Unknown Condition ID")


#CreatePrompt

def create_prompt(action_description, combined_info):

    name = combined_info.get('name', 'Friend')
    relationship = combined_info.get('relationship', 'friend')
    context = combined_info.get('context', 'general')
    personal_details = combined_info.get('personal_details', 'no additional details')

    prompt = (
        f"You are a character-replicating model. Your task is to generate a message based on the following information:\n\n"
        f"Action Description: {action_description}\n"
        f"Friend's Name: {name}\n"
        f"Relationship: {relationship}\n"
        f"Context: {context}\n"
        f"Personal Details: {personal_details}\n\n"
        f"Generate a message based on the action description provided. The message should reflect the relationship and context described, "
        f"and incorporate relevant personal details."
    )

    return prompt


#CallModel

YOUR_TOKEN = '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'

def generate_response(prompt, model="meta-llama/Llama-2-70b-chat-hf", token="YOUR_HUGGING_FACE_TOKEN"):
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 150,
            "num_return_sequences": 1
        }
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Extract the generated text from the response
        result = response.json()
        
        # Handle different formats of response depending on the model
        if isinstance(result, list):
            return result[0]['generated_text']  # For models returning list of outputs
        else:
            return result.get('generated_text', 'No text generated')  # Fallback

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None



#StoreMessage

def create_temp_csv(file_path):
    
    fields = [
        'TimeToSend', 'Reciever', 'Message', 'URL'
    ]
    
    df = pd.DataFrame(columns=fields)
    df.to_csv(file_path, index=False)
    print(f"CSV file created and saved to {file_path}")



def append_to_csv(file_path, time, reciever, message, URL):

    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)

        writer.writerow([time, reciever, message, URL])



#ApproveEditDeleteMessage

def read_csv(file_path):

    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
    return rows

def write_csv(file_path, rows):

    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def process_messages(file_path):

    temp_file_path = '/Users/lucanardinocchi/Desktop/Network/Messages/Temporary/temp.csv'
    processed_file_path = '/Users/lucanardinocchi/Desktop/Network/Messages/Processed/temp.csv'
    approved_dir = '/Users/lucanardinocchi/Desktop/Network/Messages/Approved'
    
    df = pd.read_csv(temp_file_path)
    
    if df.empty:
        print("No messages to process.")
        return

    approved_df = pd.DataFrame(columns=df.columns)

    for index, row in df.iterrows():
        receiver = row['ReceiverNumber']
        timetosend = row['TimeToSend']
        message = row['Message']
        url = row['URL']
        
        print(f"\nMessage {index + 1}:")
        print(f"Receiver: {receiver}")
        print(f"Time to Send: {timetosend}")
        print(f"Message: {message}")
        print(f"URL: {url}")
        
        while True:
            action = input("Do you want to [S]end, [E]dit, or [D]elete this message? (S/E/D): ").strip().upper()
            
            if action == 'S':
                approved_df = approved_df.append(row, ignore_index=True)
                print(f"Message sent to {receiver}.")
                break
            elif action == 'E':
                new_message = input("Enter the new message content: ")
                new_url = input("Enter the new URL (or leave empty to keep current URL): ")
                if new_message:
                    row['Message'] = new_message
                if new_url:
                    row['URL'] = new_url
                approved_df = approved_df.append(row, ignore_index=True)
                print("Message updated and approved.")
                break
            elif action == 'D':
                print("Message deleted.")
                break
            else:
                print("Invalid action. Please enter 'S', 'E', or 'D'.")

    if not os.path.exists(approved_dir):
        os.makedirs(approved_dir)
        
    date_str = datetime.now().strftime('%Y%m%d')  # Format date as YYYYMMDD
    approved_file_path = os.path.join(approved_dir, f'Approved{date_str}.csv')
    approved_df.to_csv(approved_file_path, index=False)
    print(f"Approved messages saved to {approved_file_path}")

    shutil.move(temp_file_path, processed_file_path)
    print(f"Original CSV file moved to {processed_file_path}")


#SendMessage

def send_imessage(recipient_number, message, csv_r_path=None, csv_t_path=None):

    applescript_command = f"""
    osascript -e 'tell application "Messages"
        set targetService to 1st service whose service type = iMessage
        set targetBuddy to buddy "{recipient_number}" of targetService
        send "{message}" to targetBuddy
    end tell'
    """

    try:
        subprocess.run(applescript_command, shell=True, check=True)
        print(f"Message sent to {recipient_number}: {message}")
        
        # Update CSV files if paths are provided
        if csv_t_path:
            update_csv_t(csv_t_path, recipient_number, message)
        
        if csv_r_path:
            action_type = 'Send'  # Example action type; adjust as needed
            update_csv_r(csv_r_path, action_type)
    
    except subprocess.CalledProcessError as e:
        print(f"Failed to send message: {e}")


#UpdateData

def update_csv_r(file_path, action_type):

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    record = {
        'Date': timestamp,
        'Physical_Digital': 'D',
        'D_Type': action_type,  
        'P_Action': '',
        'P_Duration': '',  
        'P_VulnerabilitiesShared': '',  
        'P_Context': '',  
        'IdeasForFuture': '',  
        'P_ProcessBefore?': '',  
        'P_ImageBuilt?': '', 
        'TsinceD': '',  
        'TsinceP': '',  
        'TsinceMet': ''  
    }
    
    df = pd.read_csv(file_path)
    df = df.append(record, ignore_index=True)
    df.to_csv(file_path, index=False)
    print(f"Record added to {file_path}")

def update_csv_t(file_path, sender, message):

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    record = {'Date': timestamp, 'Sender': sender, 'Message': message}
    
    df = pd.read_csv(file_path)
    df = df.append(record, ignore_index=True)
    df.to_csv(file_path, index=False)
    print(f"Message record added to {file_path}")


def delete_csv_file(file_path):

    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"File '{file_path}' has been deleted successfully.")
        except Exception as e:
            print(f"An error occurred while trying to delete the file: {e}")
    else:
        print(f"The file '{file_path}' does not exist.")


