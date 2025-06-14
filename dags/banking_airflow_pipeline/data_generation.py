import os
import json
import random
import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

def data_generation():
    """
    Main function to generate banking data.
    This function generates customer, account, transaction, credit card, sign-in logs, and audit logs data.
    It saves the generated data to specified local and SFTP paths.
    """

    # Initialize Faker and set random seeds for reproducibility
    fake = Faker()
    random.seed(42)
    np.random.seed(42)

    # Save path
    BASE_PATH_LOCAL = os.getenv('host_path_local')
    BASE_PATH_SFTP=os.getenv('host_path_sftp')
    run_folder = datetime.now().strftime("run_%Y%m%d_%H%M%S")
    SAVE_PATH_LOCAL = os.path.join(BASE_PATH_LOCAL, run_folder)
    SAVE_PATH_SFTP = os.path.join(BASE_PATH_SFTP, run_folder)
    # print(SAVE_PATH)
    os.makedirs(SAVE_PATH_LOCAL, exist_ok=True)
    os.makedirs(SAVE_PATH_SFTP, exist_ok=True)
    
    # Files to track used IDs
    USED_CUSTOMER_IDS_FILE = os.path.join(BASE_PATH_SFTP, "used_customer_ids.json")
    USED_ACCOUNT_IDS_FILE = os.path.join(BASE_PATH_SFTP, "used_account_ids.json")
    USED_CARD_IDS_FILE = os.path.join(BASE_PATH_SFTP, "used_card_ids.json")
    USED_TXN_IDS_FILE = os.path.join(BASE_PATH_SFTP, "used_txn_ids.json")
    USED_CARD_TXN_IDS_FILE = os.path.join(BASE_PATH_SFTP, "used_card_txn_ids.json")

    # Function to load and save used IDs
    def load_used_ids(file_path):
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return set(json.load(f))
        return set()

    def save_used_ids(file_path, used_ids):
        with open(file_path, "w") as f:
            json.dump(sorted(list(used_ids)), f)

    # Function to generate unique IDs
    def generate_unique_ids(min_val, max_val, count, used_ids_file):
        all_possible_ids = set(range(min_val, max_val + 1))
        used_ids = load_used_ids(used_ids_file)
        available_ids = list(all_possible_ids - used_ids)
        
        if len(available_ids) < count:
            raise ValueError(f"Not enough unique IDs left to generate {count} new records.")
        
        selected_ids = random.sample(available_ids, count)
        used_ids.update(selected_ids)
        save_used_ids(used_ids_file, used_ids)
        return selected_ids

    # Constants
    NUM_CUSTOMERS = random.randint(1000, 2500)
    
    today = datetime.today().date()
    one_year_ago = today - timedelta(days=365)

    GENDERS = ['M', 'F']
    ACCOUNT_TYPES = ['Savings', 'Fixed Deposit', 'Current']
    CARD_TYPES = ['Visa', 'MasterCard']
    TXN_TYPES = ['credit', 'debit']
    CARD_TXN_TYPES = ['purchase', 'payment']
    SIGNIN_METHODS = ['password', 'OTP']
    SIGNIN_STATUSES = ['success', 'failed']
    SIGNIN_FAILURE_REASONS = {
        50050: 'Error validating credentials due to invalid username or password.',
        50057: 'Other.',
        50126: 'The user account is disabled.'
    }

    ERROR_CODE=[50050, 50057, 50126]
    OPERATINGSYSTEM=['Ios 18.1','MacOs','Linux','Window 10','Window 11','Android','Ios 18.2','Ios 18.3','Ios 18.4']
    BROWSER=['Chrome','Edge','Firefox','Safari']
    STATES_COUNTERIES = {
        'Auckland': 'New Zealand',
        'Bay Of Plenty': 'New Zealand',
        'Canterbury': 'New Zealand',
        "Hawke's Bay": 'New Zealand',
        'Manawatu-Wanganui': 'New Zealand',
        'Marlborough District': 'New Zealand',
        'Nelson City': 'New Zealand',
        'Northland': 'New Zealand',
        'Otago': 'New Zealand',
        'Southland': 'New Zealand',
        'Taranaki': 'New Zealand',
        'Waikato': 'New Zealand',
        'Wellington': 'New Zealand',
        'West Coast': 'New Zealand',
        'New South Wales': 'Australia',
        'Queensland': 'Australia',
        'South Australia': 'Australia',
        'Victoria': 'Australia',
        'Western Australia': 'Australia'
    }
    AUDIT_EVENTS = ['profile_update', 'password_change', 'account_locked']
    INITIATORS = ['customer', 'system']
    ACCOUNT_STATUSES = ['active', 'closed', 'blocked']
    CARD_STATUSES = ['active', 'blocked', 'expired']

    def rand_date(start, end):
        """Return a random date between two dates (all date objects)"""
        if isinstance(start, datetime): start = start.date()
        if isinstance(end, datetime): end = end.date()
        if start > end: return start
        return start + timedelta(days=random.randint(0, (end - start).days))

    def generate_account_number(account_type):
        if account_type == 'Savings':
            return str(fake.random_number(digits=random.randint(12, 14), fix_len=True))
        elif account_type == 'Fixed Deposit':
            return str(fake.random_number(digits=16, fix_len=True))
        else:  # Current
            return str(fake.random_number(digits=random.randint(13, 14), fix_len=True))

    def generate_card_number():
        return str(fake.random_number(digits=random.choice([16, 18]), fix_len=True))

    # 1. Customers (Parent table - must be created first)
    customer_ids = generate_unique_ids(100000, 9999999, NUM_CUSTOMERS, USED_CUSTOMER_IDS_FILE)
    customers = []
    for cid in customer_ids:
        dob = fake.date_of_birth(minimum_age=18, maximum_age=65)
        earliest_created_at = dob + timedelta(days=18 * 365)
        created_at = rand_date(earliest_created_at, one_year_ago)
        updated_at = rand_date(created_at, today)
        customers.append({
            'customer_id': cid,
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'dob': dob,
            'gender': random.choice(GENDERS),
            'email': fake.email(),
            'phone_number': fake.phone_number(),
            'address': fake.address().replace("\n", ", "),
            'created_at': created_at,
            'updated_at': updated_at
        })
    df_customers = pd.DataFrame(customers)
    df_customers.to_csv(os.path.join(SAVE_PATH_SFTP, "customers.csv"), index=False)

    # 2. Accounts (Child of customers - must reference valid customer_id)
    accounts = []
    temp_accounts = []
    
    # Pre-determine account counts for each customer
    customer_account_counts = []
    total_accounts = 0
    for customer in customers:
        num_accounts = random.randint(1, 3)
        customer_account_counts.append(num_accounts)
        total_accounts += num_accounts
    
    # Generate unique account IDs
    account_ids = generate_unique_ids(100000, 9999999, total_accounts, USED_ACCOUNT_IDS_FILE)
    account_id_idx = 0
    
    for i, customer in enumerate(customers):
        num_accounts = customer_account_counts[i]
        for _ in range(num_accounts):
            acc_type = random.choice(ACCOUNT_TYPES)
            opened_date = fake.date_between(customer['created_at'], datetime.today())
            temp_accounts.append({
                'account_id': account_ids[account_id_idx],
                'customer_id': customer['customer_id'],  # FK to customers
                'account_type': acc_type,
                'account_number': generate_account_number(acc_type),
                'balance': round(random.uniform(10, 1000000), 2),
                'opened_date': opened_date,
                'status': random.choice(ACCOUNT_STATUSES),
                'interest_rate': round(random.uniform(2.5, 9.5), 2)
            })
            account_id_idx += 1
    
    random.shuffle(temp_accounts)
    accounts = temp_accounts
    df_accounts = pd.DataFrame(accounts)
    df_accounts.to_csv(os.path.join(SAVE_PATH_LOCAL, "accounts.csv"), index=False)

    # 3. Credit Cards (Child of customers - must reference valid customer_id)
    credit_cards = []
    temp_credit_cards = []
    
    # Pre-determine which customers get cards and count
    customer_gets_card = []
    total_cards = 0
    for customer in customers:
        gets_card = random.random() < 0.6
        customer_gets_card.append(gets_card)
        if gets_card:
            total_cards += 1
    
    # Generate unique card IDs only if we have cards to create
    if total_cards > 0:
        card_ids = generate_unique_ids(100000, 9999999, total_cards, USED_CARD_IDS_FILE)
        card_id_idx = 0
        
        for i, customer in enumerate(customers):
            if customer_gets_card[i]:
                card_type = random.choice(CARD_TYPES)
                issued = rand_date(customer["created_at"], today)
                expiry = issued + timedelta(days=365 * random.randint(3, 5))
                temp_credit_cards.append({
                    'card_id': card_ids[card_id_idx],
                    'customer_id': customer['customer_id'],  # FK to customers
                    'card_number': generate_card_number(),
                    'card_type': card_type,
                    'expiry_date': expiry,
                    'credit_limit': round(random.uniform(10000, 200000), 2),
                    'available_limit': round(random.uniform(5000, 150000), 2),
                    'issued_date': issued,
                    'status': random.choice(CARD_STATUSES)
                })
                card_id_idx += 1
    
    random.shuffle(temp_credit_cards)
    credit_cards = temp_credit_cards
    df_cards = pd.DataFrame(credit_cards)
    df_cards.to_csv(os.path.join(SAVE_PATH_LOCAL, "credit_cards.csv"), index=False)

    # 4. Account Transactions (Child of accounts - must reference valid account_id)
    transactions = []
    txn_temp_list = []
    
    # Pre-determine transaction counts for each account
    account_txn_counts = []
    total_txns = 0
    for acc in accounts:
        num_txns = random.randint(2, 5)
        account_txn_counts.append(num_txns)
        total_txns += num_txns
    
    # Generate unique transaction IDs
    txn_ids = generate_unique_ids(100000, 9999999, total_txns, USED_TXN_IDS_FILE)
    txn_id_idx = 0
    
    for i, acc in enumerate(accounts):
        num_txns = account_txn_counts[i]
        for _ in range(num_txns):
            tx_date = fake.date_between(acc['opened_date'], datetime.today())
            txn_temp_list.append({
                'transaction_id': txn_ids[txn_id_idx],
                'account_id': acc['account_id'],  # FK to accounts
                'transaction_type': random.choice(TXN_TYPES),
                'amount': round(random.uniform(100, 50000), 2),
                'transaction_date': tx_date,
                'balance_after_txn': round(random.uniform(1000, acc['balance']), 2),
                'reference_number': fake.uuid4()
            })
            txn_id_idx += 1
    
    random.shuffle(txn_temp_list)
    transactions = txn_temp_list
    df_txns = pd.DataFrame(transactions)
    df_txns.to_csv(os.path.join(SAVE_PATH_LOCAL, "transactions.csv"), index=False)

    # 5. Credit Card Transactions (Child of credit_cards - must reference valid card_id)
    card_txns = []
    temp_card_txns = []
    
    # Pre-determine transaction counts for each card
    card_txn_counts = []
    total_card_txns = 0
    for card in credit_cards:
        num_txns = random.randint(2, 4)
        card_txn_counts.append(num_txns)
        total_card_txns += num_txns
    
    # Generate unique card transaction IDs only if we have cards
    if total_card_txns > 0:
        card_txn_ids = generate_unique_ids(100000, 9999999, total_card_txns, USED_CARD_TXN_IDS_FILE)
        card_txn_id_idx = 0
        
        for i, card in enumerate(credit_cards):
            num_txns = card_txn_counts[i]
            for _ in range(num_txns):
                txn_date = fake.date_between(card['issued_date'], datetime.today())
                temp_card_txns.append({
                    'txn_id': card_txn_ids[card_txn_id_idx],
                    'card_id': card['card_id'],  # FK to credit_cards
                    'txn_type': random.choice(CARD_TXN_TYPES),
                    'amount': round(random.uniform(500, 5000), 2),
                    'txn_date': txn_date,
                    'merchant_name': fake.company(),
                    'location': fake.city(),
                    'statement_month': txn_date.strftime("%Y-%m")
                })
                card_txn_id_idx += 1
    
    random.shuffle(temp_card_txns)
    card_txns = temp_card_txns
    df_card_txns = pd.DataFrame(card_txns)
    df_card_txns.to_csv(os.path.join(SAVE_PATH_LOCAL, "credit_card_txns.csv"), index=False)

    # 6. Sign-in Logs (Child of customers - must reference valid customer_id)
    signin_logs = []
    for customer in customers:
        for _ in range(random.randint(1, 3)):
            status = random.choice(SIGNIN_STATUSES)
            log = {
                'log_id': fake.uuid4(),
                'customer_id': customer['customer_id'],  # FK to customers
                'sign_in_time': fake.date_between(customer['created_at'], datetime.today()),
                'status': status,
                'method': random.choice(SIGNIN_METHODS),
                'ip_address': fake.ipv4()
            }

            # Add error details if failed
            if status == 'failed':
                code = random.choice(ERROR_CODE)
                log['status_detail'] = {
                    'error_code': code,
                    'failure_reason': SIGNIN_FAILURE_REASONS[code]
                }

            # Add device details
            log['deviceDetail'] = {
                'operatingSystem': random.choice(OPERATINGSYSTEM),
                'browser': random.choice(BROWSER)
            }

            # Add location info
            state = random.choice(list(STATES_COUNTERIES.keys()))
            country = STATES_COUNTERIES[state]
            log['location'] = {
                'state': state,
                'country': country
            }

            signin_logs.append(log)
    
    with open(SAVE_PATH_LOCAL + "/signin_logs.json", 'w') as f:
        json.dump(signin_logs, f, indent=2, default=str)

    # 7. Audit Logs (Child of customers - must reference valid customer_id)
    audit_logs = []
    for customer in customers:
        for _ in range(random.randint(1, 2)):
            audit_logs.append({
                'audit_id': fake.uuid4(),
                'customer_id': customer['customer_id'],  # FK to customers
                'event': random.choice(AUDIT_EVENTS),
                'event_time': fake.date_between(customer['created_at'], datetime.today()),
                'initiated_by': random.choice(INITIATORS)
            })
    
    with open(SAVE_PATH_LOCAL + "/audit_logs.json", 'w') as f:
        json.dump(audit_logs, f, indent=2, default=str)
