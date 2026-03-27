import pytest
from pawpal_system import Task, Pet


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