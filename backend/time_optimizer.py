"""
Time Optimization Engine
------------------------
Implements time-based optimization algorithms including:

1. Task Scheduling Optimization (Greedy + Priority-based)
2. Critical Path Method (CPM)
3. Time Window Route Optimization
4. Parallel Task Optimization

No database queries included.
"""

from typing import List, Dict, Tuple
from collections import defaultdict, deque
import heapq


class TimeOptimizer:
    """
    Provides multiple time-based optimization strategies.
    """

    # -----------------------------------------------------
    # 1. Priority-Based Task Scheduling (Greedy Algorithm)
    # -----------------------------------------------------
    @staticmethod
    def optimize_task_schedule(tasks: List[Dict]) -> List[Dict]:
        """
        Schedule tasks based on earliest deadline first.
        Each task must contain:
        {
            "name": str,
            "duration": int,
            "deadline": int,
            "priority": int (higher = more important)
        }
        """

        sorted_tasks = sorted(
            tasks,
            key=lambda x: (x["deadline"], -x["priority"])
        )

        current_time = 0
        optimized_schedule = []

        for task in sorted_tasks:
            start_time = current_time
            end_time = current_time + task["duration"]

            optimized_schedule.append({
                "name": task["name"],
                "start": start_time,
                "end": end_time,
                "deadline": task["deadline"]
            })

            current_time = end_time

        return optimized_schedule

    # -----------------------------------------------------
    # 2. Critical Path Method (CPM)
    # -----------------------------------------------------
    @staticmethod
    def critical_path(tasks: Dict[str, Dict]) -> Tuple[int, List[str]]:
        """
        tasks format:
        {
            "A": {"duration": 3, "dependencies": []},
            "B": {"duration": 2, "dependencies": ["A"]}
        }

        Returns:
            total project duration,
            critical path sequence
        """

        in_degree = defaultdict(int)
        graph = defaultdict(list)

        for task, details in tasks.items():
            for dep in details["dependencies"]:
                graph[dep].append(task)
                in_degree[task] += 1

        queue = deque()
        earliest_finish = {}

        for task in tasks:
            if in_degree[task] == 0:
                queue.append(task)
                earliest_finish[task] = tasks[task]["duration"]

        while queue:
            current = queue.popleft()

            for neighbor in graph[current]:
                earliest_finish[neighbor] = max(
                    earliest_finish.get(neighbor, 0),
                    earliest_finish[current] + tasks[neighbor]["duration"]
                )
                in_degree[neighbor] -= 1

                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        total_duration = max(earliest_finish.values())
        critical_tasks = [
            task for task, finish in earliest_finish.items()
            if finish == total_duration
        ]

        return total_duration, critical_tasks

    # -----------------------------------------------------
    # 3. Time Window Optimization (Greedy)
    # -----------------------------------------------------
    @staticmethod
    def optimize_time_windows(jobs: List[Dict]) -> List[Dict]:
        """
        Each job:
        {
            "name": str,
            "duration": int,
            "window_start": int,
            "window_end": int
        }
        """

        jobs = sorted(jobs, key=lambda x: x["window_end"])
        current_time = 0
        scheduled = []

        for job in jobs:
            start_time = max(current_time, job["window_start"])
            end_time = start_time + job["duration"]

            if end_time <= job["window_end"]:
                scheduled.append({
                    "name": job["name"],
                    "start": start_time,
                    "end": end_time
                })
                current_time = end_time

        return scheduled

    # -----------------------------------------------------
    # 4. Parallel Processing Optimization
    # -----------------------------------------------------
    @staticmethod
    def optimize_parallel_tasks(tasks: List[Dict], workers: int) -> List[Dict]:
        """
        Distribute tasks across workers to minimize total time.
        Each task:
        {
            "name": str,
            "duration": int
        }
        """

        if workers <= 0:
            raise ValueError("Number of workers must be greater than zero.")

        heap = [(0, i) for i in range(workers)]  # (available_time, worker_id)
        heapq.heapify(heap)

        assignment = []

        for task in sorted(tasks, key=lambda x: -x["duration"]):
            available_time, worker_id = heapq.heappop(heap)

            start_time = available_time
            end_time = start_time + task["duration"]

            assignment.append({
                "task": task["name"],
                "worker": worker_id,
                "start": start_time,
                "end": end_time
            })

            heapq.heappush(heap, (end_time, worker_id))

        return assignment

    # -----------------------------------------------------
    # Unified Optimization Entry Point (Professional Architecture)
    # -----------------------------------------------------
    def optimize(self):
        """
        Default time optimization execution.
        Keeps architecture consistent with other engines.
        """

        # Default demo tasks (can later connect to DB)
        tasks = [
            {"name": "Task A", "duration": 3, "deadline": 10, "priority": 2},
            {"name": "Task B", "duration": 2, "deadline": 5, "priority": 3},
            {"name": "Task C", "duration": 4, "deadline": 8, "priority": 1},
        ]

        return self.optimize_task_schedule(tasks)

# -----------------------------------------------------
# Example Usage (Safe to Run)
# -----------------------------------------------------
if __name__ == "__main__":

    optimizer = TimeOptimizer()

    print("\n--- Task Scheduling Optimization ---")
    tasks = [
        {"name": "Task A", "duration": 3, "deadline": 10, "priority": 2},
        {"name": "Task B", "duration": 2, "deadline": 5, "priority": 3},
        {"name": "Task C", "duration": 4, "deadline": 8, "priority": 1},
    ]

    schedule = optimizer.optimize_task_schedule(tasks)
    print(schedule)

    print("\n--- Critical Path Method ---")
    project_tasks = {
        "A": {"duration": 3, "dependencies": []},
        "B": {"duration": 2, "dependencies": ["A"]},
        "C": {"duration": 4, "dependencies": ["A"]},
        "D": {"duration": 2, "dependencies": ["B", "C"]},
    }

    total_time, critical = optimizer.critical_path(project_tasks)
    print("Total Duration:", total_time)
    print("Critical Path:", critical)

    print("\n--- Time Window Optimization ---")
    jobs = [
        {"name": "Job 1", "duration": 2, "window_start": 0, "window_end": 5},
        {"name": "Job 2", "duration": 3, "window_start": 3, "window_end": 10},
    ]

    optimized_jobs = optimizer.optimize_time_windows(jobs)
    print(optimized_jobs)

    print("\n--- Parallel Task Optimization ---")
    parallel_tasks = [
        {"name": "Task X", "duration": 5},
        {"name": "Task Y", "duration": 2},
        {"name": "Task Z", "duration": 4},
    ]

    assignments = optimizer.optimize_parallel_tasks(parallel_tasks, workers=2)
    print(assignments)