import pyautogui
import pygetwindow as gw
import speech_recognition as sr
import time
import uuid
import sys  # Import the sys module
def open_notepad():
    pyautogui.press('win', interval=0.2)
    pyautogui.typewrite('notepad', interval=0.1)
    pyautogui.press('enter', interval=0.2)
def open_mail():
    pyautogui.press('win', interval=0.2)
    pyautogui.typewrite('mail', interval=0.1)
    pyautogui.press('enter', interval=0.2)
    # Give some time for the application to activate
    time.sleep(3)
    # Focus on the Mail application
    focus_on_application("mail")  # Replace with the actual application name
    time.sleep(2)
    focus_on_application("mail")  # Replace with the actual application name
def close_app():
    # Replace this with the appropriate key combination or action to close the Mail application
    pyautogui.hotkey('alt', 'f4')
    print("Closing app...")
def focus_on_application(app_name):
    try:
        app_window = gw.getWindowsWithTitle(app_name)[0]
        app_window.activate()
        print(f"Focusing on {app_name}...")
    except IndexError:
        print(f"{app_name} window not found.")
def open_application(app_name):
    if app_name.lower() == "notepad":
        open_notepad()
    elif app_name.lower() == "mail":
        open_mail()
    # Add more conditions for other applications if needed
def send_new_mail():
    pyautogui.hotkey('ctrl', 'n')  # Press Ctrl+N to start a new mail
    # pyautogui.typewrite('recipient@example.com')  # Replace with the actual recipient
    # pyautogui.press('tab')  # Move to the subject field
    # pyautogui.typewrite('Subject of the email')  # Replace with the actual subject
    # pyautogui.press('tab')  # Move to the email body
    # pyautogui.typewrite('Body of the email')  # Replace with the actual email content
    # pyautogui.hotkey('ctrl', 'enter')  # Press Ctrl+Enter to send the email
    print("Sending new mail...")
def save_file():
    # Generate a random file name using UUID
    random_file_name = str(uuid.uuid4())[:8]
    # Save the file with the generated name
    pyautogui.hotkey('ctrl', 's')
    pyautogui.typewrite(random_file_name)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 's')
    print(f"File saved as {random_file_name}.")
def exit_program():
    print("Exiting program...")
    sys.exit(0)  # Use sys.exit(0) to exit the program gracefully
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.8  # Adjust this threshold as needed
        audio = r.listen(source, timeout=5, phrase_time_limit=5)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"Command recognized: {query}")
        if "open" in query:
            app_name = query.split("open")[1].strip()
            open_application(app_name)
        elif "exit program" in query:
            exit_program()
        elif "send new mail" in query:
            send_new_mail()
        elif "send mail" in query:
            pyautogui.hotkey('ctrl', 'enter')  # Press Ctrl+Enter to send the email
        elif "focus on application" in query:
            pyautogui.hotkey('alt', 'tab')
        elif "save file" in query:
            save_file()
        elif "close application" in query:
            close_app()
        elif "new line" in query or "enter" in query:
            pyautogui.press('enter')
        elif "previous" in query:
            pyautogui.hotkey('shift', 'tab')
        elif "tab" in query:
            pyautogui.press('tab')
        else:
            pyautogui.press('space', interval=0.2)
            pyautogui.typewrite(query)
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except Exception as e:
        print(f"Error: {e}")
if __name__ == "__main__":
    while True:
        take_command()
