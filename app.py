from pawpal_system import Owner, Pet, Task, Scheduler
import streamlit as st

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file connects the simple Streamlit UI to your backend classes.
"""
)

# Initialize persistent objects in session state
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", time_available=120)
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(time_available=st.session_state.owner.time_available)
    st.session_state.owner.attach_scheduler(st.session_state.scheduler)

owner: Owner = st.session_state.owner
scheduler: Scheduler = st.session_state.scheduler

# Owner inputs
st.subheader("Owner")
col1, col2 = st.columns(2)
with col1:
    name_input = st.text_input("Owner name", value=owner.name)
with col2:
    time_input = st.number_input("Available time (minutes)", min_value=0, value=owner.time_available)

# Apply owner updates
owner.name = name_input
owner.time_available = int(time_input)
# keep scheduler's fallback time in sync (optional simple sync)
scheduler.time_available = owner.time_available

st.divider()

# Add pet
st.subheader("Pets")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age", min_value=0, value=1)
    add_pet_btn = st.form_submit_button("Add pet")
    if add_pet_btn and pet_name.strip():
        new_pet = Pet(name=pet_name.strip(), species=species, age=int(age))
        owner.add_pet(new_pet)
        st.success(f"Added pet {new_pet.name}")

# Show current pets and tasks
if owner.pets:
    for pet in owner.pets:
        with st.expander(f"{pet.name} ({pet.species}, age {pet.age})", expanded=False):
            tasks = pet.get_tasks()
            if tasks:
                for t in tasks:
                    st.write(f"- {t.title} — {t.duration}m — priority {t.priority}")
            else:
                st.info("No tasks for this pet yet.")
else:
    st.info("No pets added yet.")

st.divider()

# Add task to selected pet
st.subheader("Add Task to a Pet")
if not owner.pets:
    st.info("Add a pet first to create tasks for it.")
else:
    pet_names = [p.name for p in owner.pets]
    with st.form("add_task_form", clear_on_submit=True):
        chosen_pet_name = st.selectbox("Select pet", pet_names)
        task_title = st.text_input("Task title", value="Feed")
        task_type = st.selectbox("Task type", ["feeding", "exercise", "medication", "grooming", "other"])
        duration = st.number_input("Duration (minutes)", min_value=1, value=10)
        priority_label = st.selectbox("Priority", ["low", "medium", "high"], index=1)
        add_task_btn = st.form_submit_button("Add task")
        if add_task_btn:
            priority_map = {"low": 1, "medium": 2, "high": 3}
            priority_value = priority_map.get(priority_label, 1)
            task = Task(title=task_title.strip(), task_type=task_type, duration=int(duration), priority=priority_value)
            # find pet by name then add task
            pet = next((p for p in owner.pets if p.name == chosen_pet_name), None)
            if pet is not None:
                pet.add_task(task)
                st.success(f"Added task '{task.title}' to {pet.name}")

st.divider()

# Generate schedule
st.subheader("Schedule")
if st.button("Generate schedule"):
    owner.attach_scheduler(scheduler)  # ensure owner/scheduler linked
    plan = scheduler.generate_plan(owner)
    if plan:
        st.success("Schedule generated")
        for idx, t in enumerate(plan, start=1):
            # find which pet the task belongs to (by identity)
            pet_name = next((p.name for p in owner.pets if t in p.tasks), "Unknown")
            st.write(f"{idx}. {t.title} ({pet_name}) — {t.duration}m — priority {t.priority}")
        st.markdown("**Explanation:**")
        st.write(scheduler.explain_plan())
    else:
        st.info("No tasks selected (none fit or no incomplete tasks).")

st.divider()

# Reset session state
st.subheader("Reset")
if st.button("Reset app state"):
    st.session_state.clear()
    st.rerun()