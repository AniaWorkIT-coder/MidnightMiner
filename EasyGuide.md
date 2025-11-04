# Easy Guide to Running Midnight Miner on Windows

This guide will help you start mining NIGHT tokens on Windows with MidnightMiner. If you have any questions, you can post them [here](https://www.reddit.com/r/Midnight/comments/1onpvk5/comment/nn40j1r/) or message @djeanql on Discord.

## What This Software Does

Midnight Miner automatically solves puzzles to earn NIGHT tokens. It runs on your computer and can use multiple wallets at the same time to earn more rewards.

## Step 1: Install Python

Python is the programming language this software runs on.

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download 3.13.x for windows
4. Click "Install Now" and click through the steps (no need to change any config)
5. Wait for installation to complete

Alternatively, you can install [Python 3.13](https://apps.microsoft.com/detail/9pnrbtzxmb4z) from the Microsoft store.

## Step 2: Install Git

Git allows for the miner to be easily downloaded and updated from the terminal.

1. Go to [git-scm.com/install/windows](https://git-scm.com/install/windows)
2. Download the standalone installer (x64)
3. Run the installer and click through steps, leave all the configuration options as-is

## Step 3: Download MidnightMiner

1. Open Command Prompt:
   - Press `Windows`
   - Type `cmd` and press Enter
2. Type `git clone https://github.com/djeanql/MidnightMiner`
3. Then enter the folder with `cd MidnightMiner`

## Step 4: Install Dependancies


Install the required dependancies by typing:
   ```
   pip install wasmtime requests pycardano cbor2 portalocker
   ```
Press Enter and wait for installation to finish

If you get a command not found error, you can use `python -m pip` instead of `pip`

## Step 5: Start Mining

**For a single wallet** (good for testing):
```
python miner.py
```

**For multiple wallets** (recommended for better earnings):
```
python miner.py --workers 4
```

Replace `4` with the number of wallets you want to use. Each wallet uses one CPU core and about 1GB of memory.

> **Tip**: If you have a 6-core processor, try `--workers 6`. Don't use more workers than you have CPU cores.

## ⚠️ Update Regularly

This software will be updated very frequently, so it is important you update it to earn the highest rewards. To update, run this command while in the MidnightMiner folder:
```
git pull
```

This will fetch any changes made in this repository

## Back Up Your Wallet File

It is import that you back up `wallets.json`, which is in the same folder as ther miner. Copy it to a safe location. If you increase the number of worrkers with the --workers option, new wallets will be added so you should back it up again.

## The Dashboard

Once running, you'll see a dashboard that updates automatically:

- **Address**: Your wallet addresses (where tokens are sent)
- **Challenge**: The puzzle being solved
- **Attempts**: How many guesses have been tried
- **H/s**: Guesses per second
- **Completed**: Number of puzzles solved, number since launching the miner is in brackets
- **NIGHT**: Estimated token rewards

Press `Ctrl+C` to stop the miner anytime.

## Accessing Your Tokens

Your earned tokens are stored in wallets created by the software. To access them:

1. Export your wallet keys by running:
   ```
   python export_skeys.py
   ```

2. This creates a `skeys` folder with wallet files

3. Import these files into a Cardano wallet (like Eternl):
   - Open Eternl wallet
   - Go to Add Wallet -> More -> CLI Signing Keys
   - Select the files from the `skeys` folder
