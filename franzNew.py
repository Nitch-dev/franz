import time
import pyautogui 
import threading
import subprocess
import os
# --- Coordinates and Colors ---
colorX = 1089
colorY = 668
R = 64
G = 80
B = 141

x = 946
y = 729
x2 = 1215
y2 = 215

# New click coordinates
CLICK_1_X, CLICK_1_Y = 400, 750
CLICK_2_X, CLICK_2_Y = 585, 290
CLICK_3_X, CLICK_3_Y = 550, 840  # This coordinate is used twice

# New color check coordinates/color
CHECK_COLOR_X, CHECK_COLOR_Y = 800, 820
CHECK_R, CHECK_G, CHECK_B = 15, 33, 46
TOLERANCE = 12

# --- Task Functions ---

def click_task():
    """Clicks coordinate (x2, y2) every 60,000 seconds (approx. 16.67 hours)."""
    while True:
        try:
            # Original sleep was 60000 seconds
            time.sleep(60000) 
            pyautogui.click(x2, y2)
        except Exception as e:
            print(f"Error in click_task: {e}")

def open_browser():
    """
    Opens the browser, performs a sequence of initial clicks,
    runs the new color detection loop, and then calls oldScript().
    """
    # Calculate delay in seconds
    delay = 3000 * 60 
    print("Shutdown timer started")
    # Command to reboot after the calculated delay
    command = f"sleep {delay} && sudo reboot -f &"
    subprocess.run(command, shell=True)

    while True:
        print("Opening browser...")
        
        # Open Google Chrome
        br = "cd /root/Downloads/firefox && ./firefox "
        subprocess.run(f"{br} &", shell=True)
        time.sleep(15) # Give the browser time to open
        print("Brpwser Opened Now Clickingg")
        # *** INITIAL CLICKS ***
        time.sleep(25) # Wait 2 seconds as requested
        os.system("notify-send 'browser Load time Over'")

        loadCheck = pyautogui.pixelMatchesColor(354, 425, (31, 255, 32), tolerance=TOLERANCE)
        if(loadCheck == False):
            os.system("notify-send 'Cant see the Bet Btn'")
            time.sleep(120)
            loadCheck = pyautogui.pixelMatchesColor(354, 425, (31, 255, 32), tolerance=TOLERANCE)
            if(loadCheck == False):
                os.system("notify-send 'Still cant see reboot now'")
                os.system('sudo reboot -f')

        os.system("notify-send 'Bet btn is here Inital Clickss'")
        print(f"Clicking 2: ({CLICK_2_X}, {CLICK_2_Y})")
        pyautogui.click(CLICK_2_X, CLICK_2_Y)
        time.sleep(2) # Wait 2 seconds as requested
        print(f"Clicking 3: ({CLICK_3_X}, {CLICK_3_Y})")
        pyautogui.click(CLICK_3_X, CLICK_3_Y)
        

        while True:
            # *** NEW COLOR DETECTION AND CLICK LOOP ***
            print(f"Starting new color check at ({CHECK_COLOR_X}, {CHECK_COLOR_Y}) for color ({CHECK_R}, {CHECK_G}, {CHECK_B})")
            

            color_match = pyautogui.pixelMatchesColor(CHECK_COLOR_X, CHECK_COLOR_Y, (CHECK_R, CHECK_G, CHECK_B), tolerance=TOLERANCE)
            
            if color_match:
                print(f"Color MATCHED at ({CHECK_COLOR_X}, {CHECK_COLOR_Y}). Clicking ({CLICK_3_X}, {CLICK_3_Y}) again.")
                pyautogui.click(CLICK_3_X, CLICK_3_Y)
                time.sleep(2)
            else:
                current_color = pyautogui.pixel(CHECK_COLOR_X, CHECK_COLOR_Y)
                print(f"Color NOT MATCHED. Found {current_color}. Skipping extra click.")
                time.sleep(2)
            
        # *** ORIGINAL POST-BROWSER OPEN COLOR CHECK ***
        color_ref = pyautogui.pixelMatchesColor(1564, 191, (71, 88, 160), tolerance=TOLERANCE)
        while(color_ref == False):
            print("Reference color (1564, 191) not found, clicking to try and make it appear...")
            pyautogui.click(1564, 191)
            time.sleep(1)
            color_ref = pyautogui.pixelMatchesColor(1564, 191, (71, 88, 160), tolerance=TOLERANCE)
        
        print("Reference color found. Starting main script loop.")
        oldScript()
        break 

def oldScript():
    """
    Starts the background click thread and enters the main color-matching loop.
    """
    # Start the background click thread
    threading.Thread(target=click_task, daemon=True).start()
    
    # Main loop: waits for color (R, G, B) to appear at (colorX, colorY)
    while True:
        i = pyautogui.pixelMatchesColor(colorX, colorY, (R, G, B), tolerance=TOLERANCE)
        if(i == True):
            # print(f"Target color found. Clicking ({x}, {y}).")
            pyautogui.moveTo(x, y)
            pyautogui.click()
            time.sleep(1)
        else:
            # print("Color Not Found Trying Again in 1 sec")
            time.sleep(1)


# --- Script Execution ---
print("Start")
open_browser()
