import time
import threading
import platform
import os
import sys

DEFAULT_DURATION = 25 * 60 


pause_flag = threading.Event()
stop_flag = threading.Event()

def play_sound():
    system = platform.system()

    try:
        if system == "Windows":
            import winsound
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        elif system == "Darwin":  
            os.system("afplay /System/Library/Sounds/Ping.aiff")
        elif system == "Linux":
            os.system("play -nq -t alsa synth 1 sine 440") 
        else:
            print("\a") 
    except Exception as e:
        print("\n🔈 Unable to play sound:", e)

def countdown(duration):
    remaining = duration

    while remaining >= 0 and not stop_flag.is_set():
        if not pause_flag.is_set():
            mins, secs = divmod(remaining, 60)
            timer_display = f"{mins:02d}:{secs:02d}"
            print(f"\r⏳ Pomodoro: {timer_display} ", end='', flush=True)
            time.sleep(1)
            remaining -= 1
        else:
            print("\r⏸️  Paused. Press [r] to resume or [q] to quit. ", end='', flush=True)
            time.sleep(1)

    if remaining < 0 and not stop_flag.is_set():
        print("\n⏰ Time's up! Take a break!\n")
        play_sound()

def listen_for_input():
    while not stop_flag.is_set():
        command = input().strip().lower()

        if command == 'p':
            pause_flag.set()
        elif command == 'r':
            pause_flag.clear()
        elif command == 'q':
            stop_flag.set()
            break

def main():
    print("🍅 Pomodoro Timer (25 minutes)")
    print("Commands:")
    print("  [p] Pause")
    print("  [r] Resume")
    print("  [q] Quit\n")

    
    timer_thread = threading.Thread(target=countdown, args=(DEFAULT_DURATION,))
    input_thread = threading.Thread(target=listen_for_input)

    timer_thread.start()
    input_thread.start()

    try:
        timer_thread.join()
        stop_flag.set()
        input_thread.join()
    except KeyboardInterrupt:
        stop_flag.set()
        print("\n👋 Exiting. Stay productive!")

if __name__ == "__main__":
    main()
