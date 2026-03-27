# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
My initial design focused on the main parts of the PawPal+ system, which are the owner, the pet, the tasks, and the scheduler. I identified three core user actions that the system should support. First, a user should be able to enter and manage basic owner and pet information. Second, a user should be able to add and edit pet care tasks such as walks, feeding, medications, grooming, and enrichment activities. Third, a user should be able to generate and view a daily care plan based on constraints like time available, task priority, and owner preferences.
- What classes did you include, and what responsibilities did you assign to each?
My initial UML design included four main classes: Owner, Pet, Task, and Scheduler. The Owner class stores information about the pet owner, such as their name, available time, preferences, and list of pets. Its methods include adding or removing pets and updating preferences. The Pet class stores information about an individual pet, such as its name, species, age, and assigned care tasks. Its methods include adding, removing, and viewing tasks. The Task class represents a pet care activity. It stores attributes such as the task title, type, duration, priority, scheduled time, whether it recurs, and whether it has been completed. Its methods include marking a task complete and updating task details. The Scheduler class is responsible for generating a daily plan. It stores the task list, available time, and the final daily plan. Its methods include generating a plan, sorting tasks by priority, filtering tasks based on time constraints, detecting conflicts, and explaining the selected plan.

**b. Design changes**

- Did your design change during implementation?
Yes
- If yes, describe at least one change and why you made it.
I made a small design adjustment after reviewing the class skeleton. I added a clearer relationship between the Owner and Scheduler classes because the owner is the one who uses the scheduler to generate a daily plan. This made the design more consistent with the UML diagram while still keeping the system simple.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
The scheduler considers constraints such as the total available time and the priority of each task. It selects tasks that can fit within the available time while prioritizing higher-priority tasks.
- How did you decide which constraints mattered most?
I decided that time and priority mattered most because the goal of the app is to help users complete the most important tasks within limited time.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
One tradeoff in my scheduler is that conflict detection checks every pair of scheduled tasks to find overlaps. This makes the algorithm easy to read and understand, but it is less efficient than a more optimized approach that sorts tasks first and only compares nearby tasks. I decided to keep the simpler version because it is clearer for a human reader and works well for the smaller number of tasks in this project.
- Why is that tradeoff reasonable for this scenario?
This tradeoff is reasonable for this scenario because the number of tasks in a pet care app is typically small. Prioritizing readability and simplicity makes the code easier to maintain and understand, which is more important than optimizing for performance in this case.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used VS Code Copilot to help with brainstorming system design, generating class structures, and implementing methods such as sorting, filtering, recurring tasks, and conflict detection. I also used it to help generate test cases and debug issues in my code.
- What kinds of prompts or questions were most helpful?
The most helpful prompts were specific and clear instructions, such as asking for simple or beginner-friendly implementations of certain features. For example, asking how to sort tasks by time or how to implement conflict detection helped me quickly build the required functionality.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
One moment where I did not accept an AI suggestion as-is was when Copilot generated overly complex code for the Streamlit UI with multiple fallback checks and try/except blocks.
- How did you evaluate or verify what the AI suggested?
I evaluated the suggestion by reviewing the code and testing it in my app. I simplified the logic to make it easier to read and maintain, while still ensuring it worked correctly by running the app and tests.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
I tested task completion, adding tasks to pets, sorting tasks by scheduled time, recurring task creation, and conflict detection.
- Why were these tests important?
These tests were important to ensure that the core features of the scheduler worked correctly and that the system behaved as expected.

**b. Confidence**

- How confident are you that your scheduler works correctly?
I am very confident that my scheduler works correctly because all automated tests pass successfully.
- What edge cases would you test next if you had more time?
If I had more time, I would test edge cases such as tasks without scheduled times, multiple overlapping tasks, and handling a large number of tasks.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I am most satisfied with successfully building a complete system that integrates backend logic with a working user interface and automated tests.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
If I had another iteration, I would improve the user interface by allowing users to set task times directly and enhance the scheduling algorithm to handle more complex scenarios.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
One important thing I learned is that working with AI requires balancing automation with human decision-making. While AI can generate useful code quickly, it is important to review, simplify, and ensure the design remains clear and maintainable. I learned that being the "lead architect" means guiding the AI and making final decisions about the system design.
