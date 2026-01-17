import unittest
import time
import threading
from src.scheduler import JulesScheduler

class TestJulesScheduler(unittest.TestCase):
    def setUp(self):
        self.scheduler = JulesScheduler()
        self.counter = 0

    def dummy_task(self):
        self.counter += 1

    def test_add_task(self):
        self.scheduler.add_task(self.dummy_task)
        self.assertEqual(len(self.scheduler.tasks), 1)

    def test_run_pending(self):
        self.scheduler.add_task(self.dummy_task)
        self.scheduler.run_pending()
        self.assertEqual(self.counter, 1)

    def test_scheduler_loop(self):
        self.scheduler.add_task(self.dummy_task)

        # Run scheduler in a separate thread
        t = threading.Thread(target=self.scheduler.start, args=(1,))
        t.start()

        # Let it run for enough time to execute at least once
        time.sleep(1.5)

        self.scheduler.stop()
        t.join()

        self.assertGreater(self.counter, 0)

    def test_error_handling(self):
        def faulty_task():
            raise ValueError("Something went wrong")

        self.scheduler.add_task(faulty_task)
        self.scheduler.add_task(self.dummy_task)

        # Should not crash
        try:
            self.scheduler.run_pending()
        except Exception as e:
            self.fail(f"Scheduler raised exception: {e}")

        self.assertEqual(self.counter, 1)

if __name__ == '__main__':
    unittest.main()
