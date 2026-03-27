# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
My initial design focused on the main parts of the PawPal+ system, which are the owner, the pet, the tasks, and the scheduler. I identified three core user actions that the system should support. First, a user should be able to enter and manage basic owner and pet information. Second, a user should be able to add and edit pet care tasks such as walks, feeding, medications, grooming, and enrichment activities. Third, a user should be able to generate and view a daily care plan based on constraints like time available, task priority, and owner preferences.
- What classes did you include, and what responsibilities did you assign to each?
My initial UML design included four main classes: Owner, Pet, Task, and Scheduler. The Owner class stores information about the pet owner, such as their name, available time, preferences, and list of pets. Its methods include adding or removing pets and updating preferences. The Pet class stores information about an individual pet, such as its name, species, age, and assigned care tasks. Its methods include adding, removing, and viewing tasks. The Task class represents a pet care activity. It stores attributes such as the task title, type, duration, priority, scheduled time, whether it recurs, and whether it has been completed. Its methods include marking a task complete and updating task details. The Scheduler class is responsible for generating a daily plan. It stores the task list, available time, and the final daily plan. Its methods include generating a plan, sorting tasks by priority, filtering tasks based on time constraints, detecting conflicts, and explaining the selected plan.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
