#!/usr/bin/env python3
"""
Words Per Minute (WPM) Typing Test

A terminal-based application that tests typing speed and accuracy.
The program displays words that the user needs to type,
tracks typing speed in WPM, and highlights correct/incorrect input.

This program is designed to be beginner-friendly with detailed explanations
of how each part works.
"""
import curses
from curses import wrapper
import time
import random


def load_text():
    """
    Load a list of words for the typing test.
    
    This function creates a fixed list of common English words that will
    be used for the typing test. In a real application, you might load
    these from a file instead.
    
    Returns:
        A list of common English words for typing practice
    """
    words = [
        "the", "be", "to", "of", "and", "a", "in", "that", "have", "I",
        "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
        "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
        "or", "an", "will", "my", "one", "all", "would", "there", "their", "what",
        "so", "up", "out", "if", "about", "who", "get", "which", "go", "me",
        "when", "make", "can", "like", "time", "no", "just", "him", "know", "take",
        "people", "into", "year", "your", "good", "some", "could", "them", "see", "other",
        "than", "then", "now", "look", "only", "come", "its", "over", "think", "also",
        "back", "after", "use", "two", "how", "our", "work", "first", "well", "way",
        "even", "new", "want", "because", "any", "these", "give", "day", "most", "us",
        "is", "are", "was", "were", "had", "has", "it's", "been", "being", "am"
    ]
    return words


def display_text(stdscr, target_text, current_text, wpm=0.0):
    """
    Display the target text, user's current input, and WPM on the screen.
    
    This function is responsible for updating what's shown on the screen.
    It clears the screen, then shows:
    1. Instructions at the top
    2. Current WPM (words per minute) speed
    3. The target text the user should type
    4. The text the user has typed so far, with color coding:
       - Green for correct characters
       - Red for incorrect characters
    
    Args:
        stdscr: The curses window object (handles screen display)
        target_text: The text the user needs to type
        current_text: The text the user has typed so far
        wpm: Current words per minute speed (defaults to 0.0)
    """
    stdscr.clear()  # Clear the screen
    
    # Get screen dimensions (height and width)
    h, w = stdscr.getmaxyx()
    
    # Calculate center position for text display
    start_x = max(0, w // 2 - len(target_text) // 2)
    start_y = h // 2
    
    # Display instructions
    instructions = "Type the text below. Press ESC to exit."
    stdscr.addstr(start_y - 3, max(0, w // 2 - len(instructions) // 2), instructions)
    
    # Display current typing speed
    stats = f"WPM: {wpm:.2f}"
    stdscr.addstr(start_y - 1, max(0, w // 2 - len(stats) // 2), stats)
    
    # Display the target text the user needs to type
    stdscr.addstr(start_y, start_x, target_text)
    
    # Display user's typing with color-coded feedback
    for i, char in enumerate(current_text):
        # Stay within bounds of screen and target text
        if i >= len(target_text) or start_x + i >= w - 1:
            break
            
        # Set color based on whether the character is correct
        if i < len(target_text):
            if char == target_text[i]:
                color = curses.color_pair(1)  # Green for correct
            else:
                color = curses.color_pair(2)  # Red for incorrect
            
            # Show the character with appropriate color
            stdscr.addstr(start_y, start_x + i, char, color)
    
    # Update the screen with all changes
    stdscr.refresh()


def calculate_wpm(start_time, end_time, typed_chars):
    """
    Calculate words per minute based on typing duration and character count.
    
    This function uses the standard typing test formula:
    - 5 characters = 1 word (standard assumption)
    - WPM = (characters typed / 5) / minutes elapsed
    
    Args:
        start_time: The time when typing started (in seconds)
        end_time: The time when typing ended (in seconds)
        typed_chars: Number of characters typed
        
    Returns:
        The calculated WPM (words per minute) as a float
    """
    # Avoid division by zero by ensuring elapsed time is at least 0.001 seconds
    elapsed_time = max(0.001, end_time - start_time)
    
    # Convert character count to word count (5 chars = 1 word)
    words = typed_chars / 5
    
    # Convert elapsed time from seconds to minutes
    minutes = elapsed_time / 60
    
    # Calculate and return WPM
    return words / minutes if minutes > 0 else 0


def generate_target_text(word_list, word_count=10):
    """
    Generate a random string of words for the typing test.
    
    This function takes a list of words and randomly selects a specified
    number of words from it to create the text that the user will type.
    
    Args:
        word_list: List of words to choose from
        word_count: Number of words to include (defaults to 10)
        
    Returns:
        A space-separated string of random words
    """
    # Select random words from the word list
    selected_words = random.sample(word_list, min(word_count, len(word_list)))
    
    # Join words with spaces and return as a single string
    return " ".join(selected_words)


def run_typing_test(stdscr):
    """
    Run the main typing test.
    
    This function contains the main loop of the typing test:
    1. Initialize the screen and colors
    2. Generate text for the user to type
    3. Process user input (keystrokes)
    4. Track timing and accuracy
    5. Generate new text when the current one is completed
    6. End when the user presses ESC
    
    Args:
        stdscr: The curses window object
        
    Returns:
        A tuple containing (WPM, accuracy percentage)
    """
    # Initialize colors for text display
    # Color pair 1: Green text on black background (for correct typing)
    # Color pair 2: Red text on black background (for incorrect typing)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    
    # Prepare words and initial display
    words = load_text()
    target_text = generate_target_text(words)
    current_text = ""
    wpm = 0.0
    
    # Track typing statistics
    start_time = time.time()
    total_correct_chars = 0
    total_chars = 0
    
    # Display initial screen
    display_text(stdscr, target_text, current_text, wpm)
    
    # Main typing test loop
    while True:
        # Calculate and display current WPM
        if current_text:
            current_time = time.time()
            wpm = calculate_wpm(start_time, current_time, len(current_text))
        
        # Update display
        display_text(stdscr, target_text, current_text, wpm)
        
        # Get user input
        try:
            key = stdscr.getch()  # Get the next keypress
        except:
            continue
        
        # Handle key input
        if key == 27:  # ESC key - exit the test
            break
        elif key == curses.KEY_BACKSPACE or key == 127 or key == 8:  # Backspace keys
            if current_text:  # If there's text to delete
                current_text = current_text[:-1]  # Remove the last character
        elif 32 <= key <= 126:  # Printable ASCII characters (letters, numbers, symbols)
            char = chr(key)  # Convert key code to character
            current_text += char  # Add to current text
            total_chars += 1  # Increment total character count
            
            # Check if character is correct (matches target text)
            if len(current_text) <= len(target_text) and char == target_text[len(current_text) - 1]:
                total_correct_chars += 1  # Increment correct character count
        
        # Check if current text is complete (user has typed all target text)
        if len(current_text) >= len(target_text):
            # Short pause to show completion
            display_text(stdscr, target_text, current_text, wpm)
            stdscr.timeout(1500)  # Wait for 1.5 seconds
            stdscr.getch()  # Capture any keypress during wait (likely none)
            stdscr.timeout(-1)  # Reset timeout to infinite wait
            
            # Calculate final statistics for this round
            end_time = time.time()
            final_wpm = calculate_wpm(start_time, end_time, total_chars)
            accuracy = (total_correct_chars / total_chars) * 100 if total_chars > 0 else 0
            
            # Generate new text for continued typing
            target_text = generate_target_text(words)
            current_text = ""
            start_time = time.time()
            total_correct_chars = 0
            total_chars = 0
    
    # Calculate final statistics for the entire session
    end_time = time.time()
    final_wpm = calculate_wpm(start_time, end_time, total_chars)
    accuracy = (total_correct_chars / total_chars) * 100 if total_chars > 0 else 0
    
    return final_wpm, accuracy


def show_results(stdscr, wpm, accuracy):
    """
    Display the final typing test results.
    
    This function shows the user their typing performance after they've
    finished the test (pressed ESC):
    1. Typing speed in WPM (words per minute)
    2. Typing accuracy as a percentage
    
    Args:
        stdscr: The curses window object
        wpm: Words per minute achieved
        accuracy: Typing accuracy percentage
    """
    stdscr.clear()  # Clear the screen
    h, w = stdscr.getmaxyx()  # Get screen dimensions
    
    # Format and display results
    result_text = f"Your typing speed: {wpm:.2f} WPM"
    accuracy_text = f"Accuracy: {accuracy:.2f}%"
    exit_text = "Press any key to exit..."
    
    # Display results centered on screen
    stdscr.addstr(h // 2 - 2, max(0, w // 2 - len(result_text) // 2), result_text)
    stdscr.addstr(h // 2, max(0, w // 2 - len(accuracy_text) // 2), accuracy_text)
    stdscr.addstr(h // 2 + 2, max(0, w // 2 - len(exit_text) // 2), exit_text)
    
    # Update screen and wait for any key
    stdscr.refresh()
    stdscr.getch()


def main(stdscr):
    """
    Main function to initialize and run the typing test.
    
    This function sets up the terminal, runs the typing test, and
    displays the final results.
    
    Args:
        stdscr: The curses window object
    """
    # Set up curses environment
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()  # Clear screen
    
    # Run typing test
    wpm, accuracy = run_typing_test(stdscr)
    
    # Show results
    show_results(stdscr, wpm, accuracy)


if __name__ == "__main__":
    """
    Entry point of the program.
    
    This block runs when the script is executed directly (not imported).
    The curses.wrapper() function initializes curses, calls our main function,
    and ensures proper cleanup of the terminal after the program ends.
    """
    try:
        wrapper(main)  # Start the program with curses wrapper
    except KeyboardInterrupt:
        print("Typing test terminated.")  # Handle Ctrl+C
    except Exception as e:
        print(f"An error occurred: {e}")  # Handle other exceptions