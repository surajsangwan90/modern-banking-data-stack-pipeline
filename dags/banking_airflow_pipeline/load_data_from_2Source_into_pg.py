import pandas as pd
from io import StringIO
import psycopg2
import os
from datetime import datetime
from dotenv import load_dotenv
import logging
# Load environment variables from .env file
load_dotenv()

def load_accounts_data_into_pg():
    # Load environment variables
    host = os.getenv('pg_host')
    port = os.getenv('pg_port')
    database = os.getenv('pg_database')
    user = os.getenv('pg_user')
    password = os.getenv('pg_password')

    # PostgreSQL connection parameters
    pf_conn_info = {
        'host': host,
        'port': port,
        'database': database,
        'user': user,
        'password': password
    }

    # Establish connection to PostgreSQL
    logging.basicConfig(level=logging.INFO)
    logging.info("Connecting to PostgreSQL database...")
    conn = psycopg2.connect(**pf_conn_info)
    logging.info("Connection established successfully.")
    cur = conn.cursor()
    
    # Read the CSV files from local path
    local_path = os.getenv('local_file_path')
    folders = [f for f in os.listdir(local_path) 
           if os.path.isdir(os.path.join(local_path, f)) and f.startswith("run_")]
    latest_folder = sorted(folders)[-1]
    LATEST_PATH = os.path.join(local_path, latest_folder)
    logging.info(f"Reading CSV files from local path: {LATEST_PATH}")
    df_accounts = pd.read_csv(os.path.join(LATEST_PATH, 'accounts.csv'))
    # Add metadata in dataframes
    logging.info("Adding metadata to dataframes...")
    # for df in [df_accounts, df_transactions, df_credit_cards, df_credit_cards_transactions]:
    df_accounts['created_at_pg'] = datetime.now()
    df_accounts['updated_at_pg'] = datetime.now()
    df_accounts['source'] = 'local'

    # Write to database using copy for better performance
    logging.info("Loading accounts data into PostgreSQL...")
    buffer_accounts = StringIO()
    df_accounts.to_csv(buffer_accounts, index=False, header=False)
    buffer_accounts.seek(0)
    


    # Use COPY command to load data into PostgreSQL
    # Copy data from the StringIO buffer to PostgreSQL

    logging.info("Loading accounts data into PostgreSQL...")
    cur.copy_expert("""
        COPY local.accounts(account_id, customer_id, account_type, account_number, balance, opened_date, status, interest_rate, created_at_pg, updated_at_pg, source_data)
        FROM STDIN WITH CSV
    """, buffer_accounts)
    buffer_accounts.close()
    logging.info("Accounts data loaded successfully.")

    conn.commit()
    logging.info("Loading data into PostgreSQL...")
    # Close the connection
    cur.close()
    conn.close()
    logging.info("PostgreSQL connection closed.")
    logging.info("Data loading completed successfully.")
    return "Data loaded successfully from local accounts csv to PostgreSQL database."

def load_transaction_data_into_pg():
    host = os.getenv('pg_host')
    port = os.getenv('pg_port')
    database = os.getenv('pg_database')
    user = os.getenv('pg_user')
    password = os.getenv('pg_password')

    # PostgreSQL connection parameters
    pf_conn_info = {
        'host': host,
        'port': port,
        'database': database,
        'user': user,
        'password': password
    }
    # Establish connection to PostgreSQL
    logging.basicConfig(level=logging.INFO)
    logging.info("Connecting to PostgreSQL database...")
    conn = psycopg2.connect(**pf_conn_info)
    logging.info("Connection established successfully.")
    cur = conn.cursor()

    # Read the CSV files from local path
    local_path = os.getenv('local_file_path')
    folders = [f for f in os.listdir(local_path) 
        if os.path.isdir(os.path.join(local_path, f)) and f.startswith("run_")]
    latest_folder = sorted(folders)[-1]
    LATEST_PATH = os.path.join(local_path, latest_folder)
    logging.info(f"Reading CSV files from local path: {LATEST_PATH}")
    df_transactions = pd.read_csv(os.path.join(LATEST_PATH , 'transactions.csv'))

    # Add metadata in dataframes
    logging.info("Adding metadata to dataframes...")
    df_transactions['created_at_pg'] = datetime.now()
    df_transactions['updated_at_pg'] = datetime.now()
    df_transactions['source'] = 'local'
    # Write to database using copy for better performance
    logging.info("Loading transactions data into PostgreSQL...")
    buffer_transactions = StringIO()
    df_transactions.to_csv(buffer_transactions, index=False, header=False)
    buffer_transactions.seek(0)
    cur.copy_expert("""
        COPY local.transactions(transaction_id, account_id, transaction_type, amount, transaction_date, balance_after_txn,reference_number, created_at_pg, updated_at_pg, source_data)
        FROM STDIN WITH CSV
    """, buffer_transactions)
    buffer_transactions.close()
    logging.info("Transactions data loaded successfully.")
    conn.commit()
    logging.info("Loading data into PostgreSQL...")
    # Close the connection
    cur.close()
    conn.close()
    logging.info("PostgreSQL connection closed.")
    logging.info("Data loading completed successfully.")
    return "Data loaded successfully from local transaction csv to PostgreSQL database."

def load_credit_cards_data_into_pg():
    host = os.getenv('pg_host')
    port = os.getenv('pg_port')
    database = os.getenv('pg_database')
    user = os.getenv('pg_user')
    password = os.getenv('pg_password')

    # PostgreSQL connection parameters
    pf_conn_info = {
        'host': host,
        'port': port,
        'database': database,
        'user': user,
        'password': password
    }
    # Establish connection to PostgreSQL
    logging.basicConfig(level=logging.INFO)
    logging.info("Connecting to PostgreSQL database...")
    conn = psycopg2.connect(**pf_conn_info)
    logging.info("Connection established successfully.")
    cur = conn.cursor()

    # Read the CSV files from local path
    local_path = os.getenv('local_file_path')
    folders = [f for f in os.listdir(local_path) 
        if os.path.isdir(os.path.join(local_path, f)) and f.startswith("run_")]
    latest_folder = sorted(folders)[-1]
    LATEST_PATH = os.path.join(local_path, latest_folder)
    logging.info(f"Reading CSV files from local path: {LATEST_PATH}")
    df_credit_cards = pd.read_csv(os.path.join(LATEST_PATH , 'credit_cards.csv'))

    # Add metadata in dataframes
    logging.info("Adding metadata to dataframes...")
    df_credit_cards['created_at_pg'] = datetime.now()
    df_credit_cards['updated_at_pg'] = datetime.now()
    df_credit_cards['source'] = 'local'
    
    # Write to database using copy for better performance
    logging.info("Loading accounts data into PostgreSQL...")
    buffer_credit_cards= StringIO()
    df_credit_cards.to_csv(buffer_credit_cards, index=False, header=False)
    buffer_credit_cards.seek(0)
    
    logging.info("Loading credit cards data into PostgreSQL...")
    cur.copy_expert("""
        COPY local.credit_cards(card_id, customer_id, card_number, card_type, expiry_date,credit_limit,available_limit,issued_date, status,  created_at_pg, updated_at_pg, source_data)
        FROM STDIN WITH CSV
    """, buffer_credit_cards)
    buffer_credit_cards.close()
    logging.info("Credit cards data loaded successfully.")
    
    conn.commit()
    
    logging.info("Loading data into PostgreSQL...")
    
    # Close the connection
    cur.close()
    conn.close()
    
    logging.info("PostgreSQL connection closed.")
    
    logging.info("Data loading completed successfully.")
    
    return "Data loaded successfully from local credit cards csv to PostgreSQL database."


def load_credit_card_transactions_data_into_pg():
    host = os.getenv('pg_host')
    port = os.getenv('pg_port')
    database = os.getenv('pg_database')
    user = os.getenv('pg_user')
    password = os.getenv('pg_password')

    # PostgreSQL connection parameters
    pf_conn_info = {
        'host': host,
        'port': port,
        'database': database,
        'user': user,
        'password': password
    }
    
    # Establish connection to PostgreSQL
    logging.basicConfig(level=logging.INFO)
    logging.info("Connecting to PostgreSQL database...")
    conn = psycopg2.connect(**pf_conn_info)
    logging.info("Connection established successfully.")
    cur = conn.cursor()

    # Read the CSV files from local path
    local_path = os.getenv('local_file_path')
    folders = [f for f in os.listdir(local_path) 
        if os.path.isdir(os.path.join(local_path, f)) and f.startswith("run_")]
    latest_folder = sorted(folders)[-1]
    LATEST_PATH = os.path.join(local_path, latest_folder)
    logging.info(f"Reading CSV files from local path: {LATEST_PATH}")
    df_credit_card_transactions = pd.read_csv(os.path.join(LATEST_PATH , 'credit_card_txns.csv'))

    # Add metadata in dataframes
    logging.info("Adding metadata to dataframes...")
    df_credit_card_transactions['created_at_pg'] = datetime.now()
    df_credit_card_transactions['updated_at_pg'] = datetime.now()
    df_credit_card_transactions['source'] = 'local'
    
    # Write to database using copy for better performance
    logging.info("Loading credit card transactions data into PostgreSQL...")
    buffer_credit_card_transactions = StringIO()
    df_credit_card_transactions.to_csv(buffer_credit_card_transactions, index=False, header=False)
    buffer_credit_card_transactions.seek(0)
    
    cur.copy_expert("""
        COPY local.credit_card_transactions(txn_id, card_id, txn_type, amount, txn_date,merchant_name,location, statement_month, created_at_pg, updated_at_pg, source_data)
        FROM STDIN WITH CSV
    """, buffer_credit_card_transactions)
    
    buffer_credit_card_transactions.close()
    
    logging.info("Credit card transactions data loaded successfully.")
    
    conn.commit()
    
    logging.info("Loading data into PostgreSQL...")
    
    # Close the connection
    cur.close()
    conn.close()
    
    logging.info("PostgreSQL connection closed.")
    
    logging.info("Data loading completed successfully.")
    
    return "Data loaded successfully from local credit card transactions csv to PostgreSQL database."


def load_customer_data_into_pg():
    host = os.getenv('pg_host')
    port = os.getenv('pg_port')
    database = os.getenv('pg_database')
    user = os.getenv('pg_user')
    password = os.getenv('pg_password')

    # PostgreSQL connection parameters
    pf_conn_info = {
        'host': host,
        'port': port,
        'database': database,
        'user': user,
        'password': password
    }
    
    # Establish connection to PostgreSQL
    logging.basicConfig(level=logging.INFO)
    logging.info("Connecting to PostgreSQL database...")
    conn = psycopg2.connect(**pf_conn_info)
    logging.info("Connection established successfully.")
    cur = conn.cursor()

    # Read the CSV files from local path
    sftp_path = os.getenv('sftp_file_path')
    folders = [f for f in os.listdir(sftp_path) 
           if os.path.isdir(os.path.join(sftp_path, f)) and f.startswith("run_")]
    latest_folder = sorted(folders)[-1]
    LATEST_PATH = os.path.join(sftp_path, latest_folder)
    logging.info(f"Reading CSV files from sftp path: {LATEST_PATH}")
    df_customers = pd.read_csv(os.path.join(LATEST_PATH, 'customers.csv'))
    
    # logging.info(f"Reading CSV files from local path: {sftp_path}")
    # df_customers = pd.read_csv(sftp_path + 'customers.csv')

    # Add metadata in dataframes
    logging.info("Adding metadata to dataframes...")
    df_customers['created_at_pg'] = datetime.now()
    df_customers['updated_at_pg'] = datetime.now()
    df_customers['source'] = 'sftp'
    
    # Write to database using copy for better performance
    logging.info("Loading customer data into PostgreSQL...")
    # buffer_customers = StringIO()
    # df_customers.to_csv(buffer_customers, index=False, header=False)
    # buffer_customers.seek(0)
    
    # cur.copy_expert("""
    #     COPY sftp.customer(customer_id, first_name, last_name, email, phone_number, address, created_at_pg, updated_at_pg, source_data)
    #     FROM STDIN WITH CSV
    # """, buffer_customers)
    buffer_customers = StringIO()
    df_customers.to_csv(buffer_customers, index=False, header=False)
    buffer_customers.seek(0)
    
    logging.info("Loading customers data into PostgreSQL...")
    cur.copy_expert("""
        COPY sftp.customer(customer_id,	first_name,	last_name,	dob,	gender,	email,	phone_number,	address,	created_at,	updated_at,	created_at_pg,	updated_at_pg,	source_data)
        FROM STDIN WITH CSV
    """, buffer_customers)
    
    # buffer_customers.close()
    
    logging.info("Customer data loaded successfully.")
    
    conn.commit()
    
    logging.info("Loading data into PostgreSQL...")
    
    # Close the connection
    cur.close()
    conn.close()
    
    logging.info("PostgreSQL connection closed.")
    
    logging.info("Data loading completed successfully.")
    
    return "Data loaded successfully from local customers csv to PostgreSQL database."
