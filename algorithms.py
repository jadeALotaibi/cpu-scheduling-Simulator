"""
CPU Scheduling Algorithms Implementation
Implements: FCFS, SJF (Non-preemptive), Round Robin, Priority Scheduling
"""

from copy import deepcopy
from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class Process:
    """Represents a process with all scheduling-related attributes."""
    pid: str
    arrival_time: int
    burst_time: int
    priority: int = 0
    remaining_time: int = 0
    completion_time: int = 0
    waiting_time: int = 0
    turnaround_time: int = 0
    response_time: int = -1
    start_time: int = -1

    def __post_init__(self):
        self.remaining_time = self.burst_time


@dataclass
class GanttBlock:
    """Represents a single block in the Gantt chart."""
    pid: str
    start: int
    end: int
    is_idle: bool = False


@dataclass
class SchedulingResult:
    """Holds the complete result of a scheduling algorithm."""
    algorithm_name: str
    processes: List[Process]
    gantt_chart: List[GanttBlock]
    avg_waiting_time: float = 0.0
    avg_turnaround_time: float = 0.0
    avg_response_time: float = 0.0
    cpu_utilization: float = 0.0
    throughput: float = 0.0
    total_time: int = 0

    def calculate_metrics(self):
        """Calculate all performance metrics."""
        if not self.processes:
            return

        n = len(self.processes)
        total_wait = sum(p.waiting_time for p in self.processes)
        total_turnaround = sum(p.turnaround_time for p in self.processes)
        total_response = sum(p.response_time for p in self.processes)
        total_burst = sum(p.burst_time for p in self.processes)

        self.avg_waiting_time = total_wait / n
        self.avg_turnaround_time = total_turnaround / n
        self.avg_response_time = total_response / n

        if self.total_time > 0:
            self.cpu_utilization = (total_burst / self.total_time) * 100
            self.throughput = n / self.total_time


def fcfs(processes: List[Process]) -> SchedulingResult:
    """First-Come First-Served Scheduling Algorithm."""
    procs = deepcopy(processes)
    procs.sort(key=lambda p: (p.arrival_time, p.pid))

    gantt = []
    current_time = 0

    for p in procs:
        # If CPU is idle, add idle block
        if current_time < p.arrival_time:
            gantt.append(GanttBlock("IDLE", current_time, p.arrival_time, is_idle=True))
            current_time = p.arrival_time

        p.start_time = current_time
        p.response_time = current_time - p.arrival_time
        p.waiting_time = current_time - p.arrival_time

        gantt.append(GanttBlock(p.pid, current_time, current_time + p.burst_time))
        current_time += p.burst_time

        p.completion_time = current_time
        p.turnaround_time = p.completion_time - p.arrival_time

    result = SchedulingResult("FCFS", procs, gantt, total_time=current_time)
    result.calculate_metrics()
    return result


def sjf_non_preemptive(processes: List[Process]) -> SchedulingResult:
    """Shortest Job First (Non-preemptive) Scheduling Algorithm."""
    procs = deepcopy(processes)
    n = len(procs)
    completed = 0
    current_time = 0
    gantt = []
    is_completed = [False] * n

    while completed < n:
        # Find process with shortest burst time among arrived processes
        idx = -1
        min_burst = float('inf')

        for i, p in enumerate(procs):
            if not is_completed[i] and p.arrival_time <= current_time:
                if p.burst_time < min_burst:
                    min_burst = p.burst_time
                    idx = i
                elif p.burst_time == min_burst and p.arrival_time < procs[idx].arrival_time:
                    idx = i

        if idx == -1:
            # No process available, CPU idle
            next_arrival = min(p.arrival_time for i, p in enumerate(procs) if not is_completed[i])
            gantt.append(GanttBlock("IDLE", current_time, next_arrival, is_idle=True))
            current_time = next_arrival
            continue

        p = procs[idx]
        p.start_time = current_time
        p.response_time = current_time - p.arrival_time
        p.waiting_time = current_time - p.arrival_time

        gantt.append(GanttBlock(p.pid, current_time, current_time + p.burst_time))
        current_time += p.burst_time

        p.completion_time = current_time
        p.turnaround_time = p.completion_time - p.arrival_time

        is_completed[idx] = True
        completed += 1

    result = SchedulingResult("SJF (Non-Preemptive)", procs, gantt, total_time=current_time)
    result.calculate_metrics()
    return result


def round_robin(processes: List[Process], time_quantum: int) -> SchedulingResult:
    """Round Robin Scheduling Algorithm."""
    procs = deepcopy(processes)
    procs.sort(key=lambda p: (p.arrival_time, p.pid))
    n = len(procs)

    gantt = []
    current_time = 0
    ready_queue = []
    arrived = [False] * n
    completed = 0

    # Add initial arrivals
    while procs and procs[0].arrival_time <= current_time:
        ready_queue.append(procs[0])
        arrived[0] = True
        break

    # Better approach: process index tracking
    procs_remaining = list(procs)

    def add_arrivals(time):
        """Add processes that have arrived by given time."""
        added = []
        for p in procs_remaining[:]:
            if p.arrival_time <= time:
                ready_queue.append(p)
                procs_remaining.remove(p)
                added.append(p)
        return added

    add_arrivals(current_time)

    while ready_queue or procs_remaining:
        if not ready_queue:
            # CPU idle, jump to next arrival
            next_arrival = min(p.arrival_time for p in procs_remaining)
            gantt.append(GanttBlock("IDLE", current_time, next_arrival, is_idle=True))
            current_time = next_arrival
            add_arrivals(current_time)
            continue

        p = ready_queue.pop(0)

        # Set response time on first execution
        if p.response_time == -1:
            p.response_time = current_time - p.arrival_time
            p.start_time = current_time

        # Execute for quantum or remaining time
        exec_time = min(time_quantum, p.remaining_time)
        if exec_time > 0:
            gantt.append(GanttBlock(p.pid, current_time, current_time + exec_time))
        current_time += exec_time
        p.remaining_time -= exec_time

        # Add new arrivals during execution
        add_arrivals(current_time)

        if p.remaining_time > 0:
            ready_queue.append(p)
        else:
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time

    # Merge consecutive blocks of same process
    merged_gantt = []
    for block in gantt:
        if merged_gantt and merged_gantt[-1].pid == block.pid and merged_gantt[-1].end == block.start:
            merged_gantt[-1].end = block.end
        else:
            merged_gantt.append(block)

    result = SchedulingResult(f"Round Robin (Q={time_quantum})", procs, merged_gantt, total_time=current_time)
    result.calculate_metrics()
    return result


def priority_scheduling(processes: List[Process], preemptive: bool = False) -> SchedulingResult:
    """Priority Scheduling Algorithm (Lower number = Higher priority)."""
    procs = deepcopy(processes)
    n = len(procs)

    if not preemptive:
        # Non-preemptive priority scheduling
        completed = 0
        current_time = 0
        gantt = []
        is_completed = [False] * n

        while completed < n:
            idx = -1
            highest_priority = float('inf')

            for i, p in enumerate(procs):
                if not is_completed[i] and p.arrival_time <= current_time:
                    if p.priority < highest_priority:
                        highest_priority = p.priority
                        idx = i
                    elif p.priority == highest_priority and p.arrival_time < procs[idx].arrival_time:
                        idx = i

            if idx == -1:
                next_arrival = min(p.arrival_time for i, p in enumerate(procs) if not is_completed[i])
                gantt.append(GanttBlock("IDLE", current_time, next_arrival, is_idle=True))
                current_time = next_arrival
                continue

            p = procs[idx]
            p.start_time = current_time
            p.response_time = current_time - p.arrival_time
            p.waiting_time = current_time - p.arrival_time

            gantt.append(GanttBlock(p.pid, current_time, current_time + p.burst_time))
            current_time += p.burst_time

            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time
            is_completed[idx] = True
            completed += 1

        algo_name = "Priority (Non-Preemptive)"
    else:
        # Preemptive priority scheduling
        current_time = 0
        completed = 0
        gantt = []

        while completed < n:
            idx = -1
            highest_priority = float('inf')

            for i, p in enumerate(procs):
                if p.remaining_time > 0 and p.arrival_time <= current_time:
                    if p.priority < highest_priority:
                        highest_priority = p.priority
                        idx = i

            if idx == -1:
                next_arrival = min(p.arrival_time for p in procs if p.remaining_time > 0)
                gantt.append(GanttBlock("IDLE", current_time, next_arrival, is_idle=True))
                current_time = next_arrival
                continue

            p = procs[idx]
            if p.response_time == -1:
                p.response_time = current_time - p.arrival_time
                p.start_time = current_time

            gantt.append(GanttBlock(p.pid, current_time, current_time + 1))
            p.remaining_time -= 1
            current_time += 1

            if p.remaining_time == 0:
                p.completion_time = current_time
                p.turnaround_time = p.completion_time - p.arrival_time
                p.waiting_time = p.turnaround_time - p.burst_time
                completed += 1

        # Merge consecutive blocks
        merged = []
        for block in gantt:
            if merged and merged[-1].pid == block.pid and merged[-1].end == block.start:
                merged[-1].end = block.end
            else:
                merged.append(block)
        gantt = merged
        algo_name = "Priority (Preemptive)"

    result = SchedulingResult(algo_name, procs, gantt, total_time=current_time)
    result.calculate_metrics()
    return result


# Algorithm registry for easy access
ALGORITHMS = {
    "FCFS": lambda procs, **kwargs: fcfs(procs),
    "SJF": lambda procs, **kwargs: sjf_non_preemptive(procs),
    "Round Robin": lambda procs, **kwargs: round_robin(procs, kwargs.get("quantum", 2)),
    "Priority": lambda procs, **kwargs: priority_scheduling(procs, kwargs.get("preemptive", False)),
}


def run_all_algorithms(processes: List[Process], time_quantum: int = 2) -> List[SchedulingResult]:
    """Run all algorithms for comparison."""
    return [
        fcfs(processes),
        sjf_non_preemptive(processes),
        round_robin(processes, time_quantum),
        priority_scheduling(processes, preemptive=False),
    ]
