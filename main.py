import subprocess
import time
import sys
import os
import signal

# --- Configuration ---
# Define paths to your scripts relative to the project root
# Ensure you moved btc_producer.py to 'src/producers/'
PRODUCER_SCRIPT = os.path.join("src", "producers", "btc_producer.py")
PROCESSOR_SCRIPT = os.path.join("src", "processors", "stream_processor.py")

# Global variables to hold process references
producer_process = None
processor_process = None


def stop_processes(sig, frame):
    """
    Callback function to handle Ctrl+C (KeyboardInterrupt).
    It terminates both child processes gracefully.
    """
    print("\nStopping all services...")

    if producer_process:
        print("Terminating Producer...")
        producer_process.terminate()

    if processor_process:
        print("Terminating Spark Processor...")
        processor_process.terminate()

    print("All services stopped. Exiting.")
    sys.exit(0)


def check_files_exist():
    """
    Verifies if the script files exist in the expected paths.
    """
    if not os.path.exists(PRODUCER_SCRIPT):
        print(f"Error: Could not find producer script at: {PRODUCER_SCRIPT}")
        print("Tip: Check if the file is inside 'src/producers' folder.")
        return False
    if not os.path.exists(PROCESSOR_SCRIPT):
        print(f"Error: Could not find processor script at: {PROCESSOR_SCRIPT}")
        print("Tip: Check if the file is inside 'src/processors' folder.")
        return False
    return True


# --- Main Execution ---
if __name__ == "__main__":
    # Register the signal handler for Ctrl+C
    signal.signal(signal.SIGINT, stop_processes)

    print("Starting Crypto Streaming Pipeline...")
    print(f"Python Executable: {sys.executable}")

    # Verify file paths before starting
    if not check_files_exist():
        sys.exit(1)

    try:
        # 1. Start the Producer (Background Process)
        # This starts the process and immediately releases the terminal
        print(f"--> Launching Producer ({PRODUCER_SCRIPT})...")
        producer_process = subprocess.Popen([sys.executable, PRODUCER_SCRIPT])

        # 2. Buffer Time
        # Wait 5 seconds to allow Kafka connection and initial data ingestion
        print("--> Waiting 5 seconds for Kafka connection...")
        time.sleep(5)

        # 3. Start the Spark Processor (Background Process)
        print(f"--> Launching Spark Processor ({PROCESSOR_SCRIPT})...")
        processor_process = subprocess.Popen([sys.executable, PROCESSOR_SCRIPT])

        # 4. Keep Alive
        print("\nPipeline is running! Both scripts are active.")
        print("Press Ctrl+C to stop both processes.\n")

        # wait() keeps the main script running, monitoring the child processes
        producer_process.wait()
        processor_process.wait()

    except Exception as e:
        print(f"An error occurred: {e}")
        stop_processes(None, None)