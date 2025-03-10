# Key Features:
### Creating Reminders:

* Users can create a reminder by specifying the time and text in a free-form manner. For example:
* "Meeting with a friend at 18:30"
* "Send the report tomorrow at 10:00"
* The bot automatically recognizes the user's intent and parses the time to create a reminder.
<img src="https://github.com/user-attachments/assets/3f1b0fb0-6bfb-4a2b-bca0-1d3d01a0db03" width="400" />

### Viewing Reminder List:
* Users can request a list of active reminders using the /list command.
* The bot displays a list of reminders with the specified time and the remaining time until the reminder triggers.
<img src="https://github.com/user-attachments/assets/76f25b21-9c21-4f2e-bb6d-9ef56fed498e" width="400" />

### Deleting Reminders:
* Users can delete a reminder by selecting it from the list and clicking the "Delete" button.
* The bot cancels the scheduled notification and removes the reminder from the list.

### Error Handling:
* If the bot cannot recognize the user's intent or the time, it provides examples of correct requests and hints.

# Logging:
All user actions are logged for tracking and debugging purposes.
<img src="https://github.com/user-attachments/assets/f1a5e36c-e94f-4f7c-8504-9875ddc509e5" width="700" />

# Technical Details:
* aiogram library for Telegram API interaction.
* NLP modules for intent recognition and time parsing.
* Database for storing reminders.
* Task scheduler for managing notifications.
