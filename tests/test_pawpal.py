import pytest
import datetime
from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete_sets_completed_true():
    task = Task(title="Walk", task_type="exercise", duration=30, priority=1)
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_adding_task_to_pet_increases_count():
    pet = Pet(name="Fido", species="dog", age=3)
    task = Task(title="Feed", task_type="feeding", duration=10, priority=2)
    before = len(pet.get_tasks())
    pet.add_task(task)
    after = len(pet.get_tasks())
    assert after == before + 1

def test_sort_tasks_by_time():
    scheduler = Scheduler()

    t1 = Task("Task1", "Test", 10, 1, datetime.datetime(2026, 1, 1, 10, 0))
    t2 = Task("Task2", "Test", 10, 1, datetime.datetime(2026, 1, 1, 8, 0))
    t3 = Task("Task3", "Test", 10, 1, datetime.datetime(2026, 1, 1, 9, 0))

    sorted_tasks = scheduler.sort_tasks_by_scheduled_time([t1, t2, t3])

    assert [t.title for t in sorted_tasks] == ["Task2", "Task3", "Task1"]


def test_recurring_task_creates_next():
    pet = Pet("Buddy", "Dog", 3)

    task = Task(
        "Walk",
        "Walk",
        30,
        1,
        datetime.datetime(2026, 1, 1, 9, 0),
        frequency="daily"
    )

    pet.add_task(task)
    task.pet = pet

    task.mark_complete()

    assert len(pet.tasks) == 2
    assert pet.tasks[1].scheduled_time == datetime.datetime(2026, 1, 2, 9, 0)


def test_conflict_detection():
    scheduler = Scheduler()

    t1 = Task("A", "Test", 60, 1, datetime.datetime(2026, 1, 1, 9, 0))
    t2 = Task("B", "Test", 30, 1, datetime.datetime(2026, 1, 1, 9, 0))

    result = scheduler.detect_conflicts([t1, t2], return_message=True)

    assert "Warning" in result