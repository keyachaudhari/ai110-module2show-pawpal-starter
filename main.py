from pawpal_system import Owner, Pet, Task, Scheduler
import datetime


def main():
    owner = Owner(name="Alex", time_available=120)

    dog = Pet(name="Buddy", species="Dog", age=3)
    cat = Pet(name="Whiskers", species="Cat", age=2)

    owner.add_pet(dog)
    owner.add_pet(cat)

    task1 = Task(
        title="Morning Walk",
        task_type="Walk",
        duration=30,
        priority=3,
        scheduled_time=datetime.datetime(2026, 1, 1, 9, 0)
    )

    task2 = Task(
        title="Feed Cat",
        task_type="Feeding",
        duration=10,
        priority=5,
        scheduled_time=datetime.datetime(2026, 1, 1, 8, 0)
    )

    task3 = Task(
        title="Vet Appointment",
        task_type="Appointment",
        duration=60,
        priority=4,
        scheduled_time=datetime.datetime(2026, 1, 1, 9, 0) 
    )

    dog.add_task(task1)
    cat.add_task(task2)
    dog.add_task(task3)

    scheduler = Scheduler()
    owner.attach_scheduler(scheduler)

    plan = scheduler.generate_plan(owner)

    # Check for scheduling conflicts and print a warning if any
    conflict_warning = scheduler.detect_conflicts(owner.get_all_tasks(), return_message=True)
    if conflict_warning:
        print("\nCONFLICT WARNING:")
        print(conflict_warning)

    # Print schedule
    print("\nToday's Schedule:\n")

    for task in plan:
        time_str = task.scheduled_time.strftime("%H:%M") if task.scheduled_time else "No time"
        print(f"- {task.title} ({task.task_type}) at {time_str} | Duration: {task.duration} mins | Priority: {task.priority}")

    print("\nExplanation:")
    print(scheduler.explain_plan())
    print("\n--- Sorted Tasks by Scheduled Time ---")
    sorted_tasks = scheduler.sort_tasks_by_scheduled_time(owner.get_all_tasks())
    for task in sorted_tasks:
        print(f"{task.title} - {task.scheduled_time}")

    print("\n--- Incomplete Tasks Only ---")
    incomplete_tasks = scheduler.filter_tasks(tasks=owner.get_all_tasks(), include_completed=False)
    for task in incomplete_tasks:
        print(task.title)

    print("\n--- Tasks for Buddy ---")
    buddy_tasks = scheduler.filter_tasks(pet_name="Buddy")
    for task in buddy_tasks:
        print(task.title)

    print("\n--- Conflict Detection ---")
    message = scheduler.detect_conflicts(owner.get_all_tasks(), return_message=True)

    if message:
        print("⚠️", message)
    else:
        print("No conflicts found.")


if __name__ == "__main__":
    main()