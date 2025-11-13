"""File I/O utilities with cross-platform locking"""
import os
import json
import logging
from datetime import datetime, timezone

# Cross-platform file locking
try:
    import portalocker
    HAS_PORTALOCKER = True
except ImportError:
    HAS_PORTALOCKER = False
    if os.name == 'nt':
        import msvcrt
    else:
        import fcntl


def lock_file(file_handle):
    """Acquire exclusive lock on file (cross-platform)"""
    if HAS_PORTALOCKER:
        portalocker.lock(file_handle, portalocker.LOCK_EX)
    elif os.name == 'nt':
        msvcrt.locking(file_handle.fileno(), msvcrt.LK_LOCK, 1)
    else:
        fcntl.flock(file_handle.fileno(), fcntl.LOCK_EX)


def unlock_file(file_handle):
    """Release lock on file (cross-platform)"""
    if HAS_PORTALOCKER:
        portalocker.unlock(file_handle)
    elif os.name == 'nt':
        file_handle.seek(0)
        msvcrt.locking(file_handle.fileno(), msvcrt.LK_UNLCK, 1)
    else:
        fcntl.flock(file_handle.fileno(), fcntl.LOCK_UN)


def load_latest_balance_snapshot(balances_file="balances.json"):
    """Load the most recent balance snapshot from balances.json. Returns (balance, timestamp) or (None, None) if not found."""
    try:
        if not os.path.exists(balances_file):
            return (None, None)

        with open(balances_file, 'r') as f:
            balances_data = json.load(f)

        if not balances_data or 'snapshots' not in balances_data:
            return (None, None)

        snapshots = balances_data['snapshots']
        if not snapshots:
            return (None, None)

        # Get the most recent snapshot (last in list if sorted chronologically)
        # Sort by timestamp to ensure we get the latest
        sorted_snapshots = sorted(snapshots, key=lambda x: x.get('timestamp', ''))
        latest = sorted_snapshots[-1]

        balance = latest.get('balance')
        timestamp = latest.get('timestamp')

        return (balance, timestamp) if balance is not None else (None, None)
    except Exception as e:
        logging.warning(f"Failed to load balance snapshot: {e}")
        return (None, None)


def save_balance_snapshot(balance, balances_file="balances.json"):
    """Save a balance snapshot with timestamp to balances.json"""
    try:
        # Create file if it doesn't exist
        if not os.path.exists(balances_file):
            with open(balances_file, 'w') as f:
                json.dump({"snapshots": []}, f)

        # Append with locking
        with open(balances_file, 'r+') as f:
            lock_file(f)
            try:
                f.seek(0)
                content = f.read()
                balances_data = json.loads(content) if content else {"snapshots": []}

                # Ensure snapshots list exists
                if 'snapshots' not in balances_data:
                    balances_data['snapshots'] = []

                # Add new snapshot
                snapshot = {
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                    'balance': balance
                }
                balances_data['snapshots'].append(snapshot)

                # Keep only last 10000 snapshots to prevent file from growing too large
                if len(balances_data['snapshots']) > 10000:
                    balances_data['snapshots'] = balances_data['snapshots'][-10000:]

                f.seek(0)
                f.truncate()
                json.dump(balances_data, f, indent=2)
                f.flush()
                os.fsync(f.fileno())

                return True
            finally:
                unlock_file(f)
        return True
    except Exception as e:
        logging.warning(f"Failed to save balance snapshot: {e}")
        return False


def backup_wallets_file(wallet_file):
    """Backup wallets.json to wallets.json.bak before making changes"""
    if os.path.exists(wallet_file):
        backup_file = wallet_file + ".bak"
        try:
            import shutil
            shutil.copy2(wallet_file, backup_file)
            return True
        except Exception as e:
            logging.warning(f"Failed to create backup of {wallet_file}: {e}")
            return False
    return False


def append_solution_to_csv(address, challenge_id, nonce):
    """Append solution to solutions.csv with proper file locking"""
    try:
        # Create file if it doesn't exist
        if not os.path.exists("solutions.csv"):
            with open("solutions.csv", 'w') as f:
                pass

        # Append with locking
        with open("solutions.csv", 'a') as f:
            lock_file(f)
            try:
                f.write(f"{address},{challenge_id},{nonce}\n")
                f.flush()
                os.fsync(f.fileno())
            finally:
                unlock_file(f)
        return True
    except Exception as e:
        return False
