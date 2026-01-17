import time
import logging
from typing import List, Callable, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("JulesScheduler")

class JulesScheduler:
    """
    A simple scheduler to manage background tasks for Exploreon,
    such as processing verified experiences and minting SFTs.
    """
    def __init__(self):
        self.tasks: List[Callable[[], Any]] = []
        self.running = False
        self._stop_event = False

    def add_task(self, task: Callable[[], Any]):
        """Adds a task to the scheduler."""
        self.tasks.append(task)
        logger.info(f"Task added: {task.__name__ if hasattr(task, '__name__') else str(task)}")

    def start(self, interval: int = 1):
        """
        Starts the scheduler loop.
        Note: This is a blocking call if run in the main thread.
        For non-blocking, run this in a separate thread.
        """
        self.running = True
        self._stop_event = False
        logger.info("Jules Scheduler started.")

        try:
            while self.running and not self._stop_event:
                for task in self.tasks:
                    try:
                        task()
                    except Exception as e:
                        logger.error(f"Error executing task {task}: {e}")

                # Sleep in small increments to allow for faster stopping
                for _ in range(interval * 10):
                    if not self.running or self._stop_event:
                        break
                    time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop()

        logger.info("Jules Scheduler stopped.")

    def stop(self):
        """Stops the scheduler loop."""
        self.running = False
        self._stop_event = True
        logger.info("Stopping Jules Scheduler...")

    def run_pending(self):
        """Runs all pending tasks once."""
        for task in self.tasks:
            try:
                task()
            except Exception as e:
                logger.error(f"Error executing task {task}: {e}")

# Example tasks
def process_verified_experiences():
    # Placeholder for logic that checks a database or queue for verified users
    # and triggers SFT minting.
    # logger.info("Checking for verified experiences to mint SFTs...")
    pass

def cleanup_old_verification_logs():
    # Placeholder for cleanup logic
    # logger.info("Cleaning up old verification logs...")
    pass

if __name__ == "__main__":
    scheduler = JulesScheduler()
    scheduler.add_task(process_verified_experiences)
    scheduler.add_task(cleanup_old_verification_logs)

    # Run for a short time for demonstration
    import threading
    t = threading.Thread(target=scheduler.start, args=(2,))
    t.start()

    time.sleep(5)
    scheduler.stop()
    t.join()
