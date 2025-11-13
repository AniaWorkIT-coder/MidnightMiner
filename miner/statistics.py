"""Statistics and balance tracking for Midnight Miner"""
import logging
from .api_client import get_wallet_statistics


def fetch_total_night_balance(wallet_manager, api_base):
    """Fetch total NIGHT balance across all wallets once at startup. Returns balance or None if fetch failed."""
    total_night = 0.0
    failed = False

    for wallet in wallet_manager.wallets:
        stats = get_wallet_statistics(wallet['address'], api_base)
        if stats:
            local = stats.get('local', {})
            night = local.get('night_allocation', 0) / 1000000.0
            total_night += night
        else:
            failed = True
            break

    if failed:
        logging.warning("Some wallet statistics could not be fetched.")
        return None  # Return None to indicate failure

    return total_night
