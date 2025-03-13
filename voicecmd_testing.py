import pyautogui
import speech_recognition as sr
def open_notepad():
    pyautogui.press('win', interval=0.2)
    pyautogui.typewrite('notepad', interval=0.1)
    pyautogui.press('enter', interval=0.2)
def open_application(app_name):
    # Customize this function to include commands for other applications
    if app_name.lower() == "notepad":
        open_notepad()
    # Add more conditions for other applications if needed
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"Command recognized: {query}")
        if "open" in query:
            # Extract the application name from the command
            app_name = query.split("open")[1].strip()
            open_application(app_name)
        elif "new line" in query:
            pyautogui.press('enter')
        else:
            # If no specific command is recognized, type the command into Notepad
            pyautogui.press('space', interval=0.2)
            pyautogui.typewrite(query)
    except Exception as e:
        print("Say that again please...")
        return "None"
if __name__ == "__main__":
    while True:
        take_command()
