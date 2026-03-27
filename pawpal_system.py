from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple
import datetime


@dataclass
class Task:
    title: str
    task_type: str
    duration: int  # minutes
    priority: int
    scheduled_time: Optional[datetime.datetime] = None
    # frequency can be None, "daily", or "weekly"
    frequency: Optional[str] = None
    # back-reference to the Pet that owns this task (set when added to a Pet)
    pet: Optional["Pet"] = field(default=None, repr=False, compare=False)
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        # avoid double-creating occurrences if already completed
        if self.completed:
            return

        self.completed = True

        # If this task is recurring (frequency set) and has a scheduled_time,
        # create a new Task for the next occurrence and attach it to the same pet.
        if self.frequency and self.scheduled_time and self.pet:
            if self.frequency == "daily":
                delta = datetime.timedelta(days=1)
            elif self.frequency == "weekly":
                delta = datetime.timedelta(days=7)
            else:
                # unknown frequency -- do nothing
                return

            next_time = self.scheduled_time + delta

            # create a new Task for the next occurrence
            new_task = Task(
                title=self.title,
                task_type=self.task_type,
                duration=self.duration,
                priority=self.priority,
                scheduled_time=next_time,
                frequency=self.frequency,
                completed=False,
            )

            # attach to the same pet using Pet.add_task (this will set new_task.pet)
            try:
                self.pet.add_task(new_task)
            except Exception:
                # keep this simple and fail silently if adding fails
                pass

    def update_priority(self, priority: int) -> None:
        """Set a new priority for the task."""
        self.priority = int(priority)

    def update_duration(self, duration: int) -> None:
        """Set a new duration (in minutes) for the task."""
        self.duration = int(duration)


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet if it's not already present."""
        if task not in self.tasks:
            # set back-reference so Task can create next occurrences
            task.pet = self
            self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet if present."""
        if task in self.tasks:
            self.tasks.remove(task)
            # clear back-reference
            if getattr(task, "pet", None) is self:
                task.pet = None

    def get_tasks(self) -> List[Task]:
        """Return a copy of this pet's tasks."""
        return list(self.tasks)


class Owner:
    def __init__(
        self,
        name: str,
        time_available: int,
        preferences: Optional[Dict[str, Any]] = None,
        pets: Optional[List[Pet]] = None,
    ) -> None:
        self.name: str = name
        self.time_available: int = time_available
        self.preferences: Dict[str, Any] = preferences or {}
        self.pets: List[Pet] = pets or []
        self.scheduler: Optional[Scheduler] = None

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list if not already added."""
        if pet not in self.pets:
            self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner's pet list if present."""
        if pet in self.pets:
            self.pets.remove(pet)

    def update_preferences(self, prefs: Dict[str, Any]) -> None:
        """Update the owner's preferences dictionary."""
        self.preferences.update(prefs)

    def attach_scheduler(self, scheduler: "Scheduler") -> None:
        """Attach a Scheduler instance to this owner."""
        self.scheduler = scheduler
        scheduler.owner = self

    def detach_scheduler(self) -> None:
        """Detach any Scheduler instance from this owner."""
        if self.scheduler is not None:
            self.scheduler.owner = None
        self.scheduler = None

    def get_all_tasks(self) -> List[Task]:
        """Return a flat list of all tasks from all of the owner's pets."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    def __init__(self, tasks: Optional[List[Task]] = None, time_available: int = 0) -> None:
        self.tasks: List[Task] = tasks or []
        self.time_available: int = time_available
        self.daily_plan: List[Task] = []
        self.owner: Optional[Owner] = None

    def generate_plan(self, owner: Optional[Owner] = None) -> List[Task]:
        """Generate a daily plan of tasks that fit within available time by priority."""
        source_owner = owner or self.owner
        if source_owner is not None:
            all_tasks = source_owner.get_all_tasks()
            day_time = source_owner.time_available
        else:
            all_tasks = list(self.tasks)
            day_time = self.time_available

        candidates = [t for t in all_tasks if not t.completed]
        candidates.sort(key=lambda t: (-t.priority, t.duration))

        plan: List[Task] = []
        remaining = int(day_time)

        for task in candidates:
            if task.duration <= remaining:
                plan.append(task)
                remaining -= task.duration

        self.daily_plan = plan
        return list(plan)

    def sort_tasks_by_priority(self) -> None:
        """Sort the scheduler's task list by priority (descending)."""
        self.tasks.sort(key=lambda t: (-t.priority, t.duration))

    def sort_tasks_by_scheduled_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Return tasks sorted by scheduled_time, with unscheduled tasks last."""
        source = tasks if tasks is not None else (self.daily_plan if self.daily_plan else self.tasks)
        # Use datetime.max for tasks without scheduled_time so they sort to the end
        return sorted(source, key=lambda t: (t.scheduled_time if t.scheduled_time is not None else datetime.datetime.max))

    def filter_tasks(self, include_completed: bool = False, pet_name: Optional[str] = None, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Filter tasks by completion status and optional pet name."""
        # If a pet name is provided, prefer tasks from that pet (requires attached owner)
        if pet_name:
            if not self.owner:
                return []
            pet = next((p for p in self.owner.pets if p.name == pet_name), None)
            if not pet:
                return []
            source = pet.get_tasks()
        else:
            source = tasks if tasks is not None else (self.daily_plan if self.daily_plan else self.tasks)

        # Filter by completion status
        return [t for t in source if (include_completed or not t.completed)]

    def filter_tasks_by_time(self, max_minutes: Optional[int] = None) -> List[Task]:
        """Return tasks that individually fit within the given time limit."""
        if max_minutes is None:
            max_minutes = self.owner.time_available if self.owner is not None else self.time_available
        return [task for task in self.tasks if task.duration <= int(max_minutes)]

    def detect_conflicts(self, tasks: Optional[List[Task]] = None, return_message: bool = False):
        """Detect overlapping scheduled tasks; optionally return a short warning message."""
        consider = tasks if tasks is not None else (self.daily_plan if self.daily_plan else self.tasks)
        scheduled = [task for task in consider if task.scheduled_time is not None]
        conflicts: List[Tuple[Task, Task]] = []

        for i in range(len(scheduled)):
            task1 = scheduled[i]
            start1 = task1.scheduled_time
            end1 = start1 + datetime.timedelta(minutes=task1.duration)

            for j in range(i + 1, len(scheduled)):
                task2 = scheduled[j]
                start2 = task2.scheduled_time
                end2 = start2 + datetime.timedelta(minutes=task2.duration)

                if start1 < end2 and start2 < end1:
                    conflicts.append((task1, task2))

        # If caller requested a friendly message, return that instead of the raw list
        if return_message:
            if conflicts:
                # build a short sample of conflicts for the message
                sample = []
                for a, b in conflicts[:5]:
                    sample.append(f"'{a.title}' vs '{b.title}'")
                sample_text = ", ".join(sample)
                more = "..." if len(conflicts) > 5 else ""
                return f"Warning: {len(conflicts)} conflict(s) detected: {sample_text}{more}"
            return ""

        return conflicts

    def explain_plan(self) -> str:
        """Provide a short explanation for the current daily plan."""
        if not self.daily_plan:
            return "No tasks selected because there were no available incomplete tasks that fit within the available time."

        total_minutes = sum(task.duration for task in self.daily_plan)
        return (
            f"Selected {len(self.daily_plan)} task(s) totaling {total_minutes} minutes "
            "by prioritizing higher-priority incomplete tasks that fit within the available time."
        )
