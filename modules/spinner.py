import sys
import time
import threading
from itertools import cycle

class Spinner:
    """A simple terminal spinner."""

    def __init__(self, message="Processing...", delay=0.1):
        """
        Initializes the Spinner object.

        Args:
            message (str): The message to display next to the spinner.
            delay (float): The delay in seconds between each frame of the spinner.
        """
        self.spinner_chars = cycle(['-', '/', '|', '\\'])
        self.delay = delay
        self.busy = False
        self.message = message
        self.thread = None

    def spinner_task(self):
        """The function that runs in a separate thread to display the spinner."""
        while self.busy:
            char = next(self.spinner_chars)
            # Use ANSI escape codes for color and bold text
            # \033[96m -> Cyan color
            # \033[1m  -> Bold
            # \033[0m  -> Reset style
            sys.stdout.write(f"\r\033[96m\033[1m{self.message} {char}\033[0m")
            sys.stdout.flush()
            time.sleep(self.delay)

    def start(self):
        """Starts the spinner."""
        self.busy = True
        self.thread = threading.Thread(target=self.spinner_task)
        self.thread.daemon = True  # Allow main thread to exit even if spinner is running
        self.thread.start()

    def stop(self):
        """Stops the spinner and clears the line."""
        self.busy = False
        if self.thread:
            self.thread.join(timeout=self.delay * 2)
        # Clear the line by overwriting with spaces
        sys.stdout.write('\r' + ' ' * (len(self.message) + 5) + '\r')
        sys.stdout.flush()

    def __enter__(self):
        """Starts the spinner when entering a 'with' block."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Stops the spinner when exiting a 'with' block."""
        self.stop() 