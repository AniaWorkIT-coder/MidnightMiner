
import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# This script requires matplotlib. Please install it using:
# pip install matplotlib

def plot_solved_challenges_over_time():
    """
    Reads challenges.json, and uses matplotlib to display a solved challenges over time graph.
    """
    try:
        with open('challenges.json', 'r') as f:
            challenges_data = json.load(f)
    except FileNotFoundError:
        print("Error: challenges.json not found.")
        return
    except json.JSONDecodeError:
        print("Error: Could not decode challenges.json.")
        return

    solved_challenges_times = []
    for challenge in challenges_data.values():
        # A challenge is considered solved if 'solved_by' is not empty.
        if challenge.get('solved_by'):
            # The 'discovered_at' timestamp is used for the time of the challenge.
            # The timestamp is in ISO 8601 format with timezone info, which fromisoformat can handle.
            time_str = challenge.get("discovered_at")
            if time_str:
                try:
                    # The format includes microseconds and a timezone, which datetime.fromisoformat handles well.
                    dt_object = datetime.fromisoformat(time_str)
                    solved_challenges_times.append(dt_object)
                except (ValueError, TypeError):
                    print(f"Warning: Could not parse timestamp '{time_str}' for a solved challenge.")


    if not solved_challenges_times:
        print("No solved challenges with valid timestamps found to plot.")
        return

    # Sort the timestamps chronologically
    solved_challenges_times.sort()

    # Create cumulative counts
    cumulative_counts = range(1, len(solved_challenges_times) + 1)

    # Plotting
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(solved_challenges_times, cumulative_counts, marker='o', linestyle='-', color='cyan')

    # Formatting the plot
    ax.set_title('Solved Challenges Over Time', color='white')
    ax.set_xlabel('Date', color='white')
    ax.set_ylabel('Cumulative Number of Solved Challenges', color='white')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')

    # Improve date formatting on the x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.xticks(rotation=45, ha='right', color='white')
    plt.yticks(color='white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')


    plt.tight_layout()

    # Save the figure
    output_filename = 'solved_challenges_over_time.png'
    plt.savefig(output_filename, facecolor='#222222')
    # Only show the plot if a display is available (e.g., not on a headless server)
    import os
    if os.environ.get('DISPLAY'):
        plt.show()
    else:
        print("No display found. Skipping plot window.")
    print(f"Graph saved to {output_filename}")

if __name__ == "__main__":
    plot_solved_challenges_over_time()
