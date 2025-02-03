import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage

# Global inventory list
inventory = []

class AdventureGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sci-Fi Adventure Game")
        self.root.geometry("800x700")
        
        # Create a frame for narrative text and buttons
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Create text area for narrative
        self.text_area = tk.Text(self.main_frame, wrap=tk.WORD, state=tk.DISABLED, font=('Helvetica', 12), height=10)
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Frame for buttons
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(pady=10)
        
        # Frame for images and animations
        self.media_frame = tk.Frame(root)
        self.media_frame.pack(pady=10)
        
        # Create a canvas for animations
        self.animation_canvas = tk.Canvas(self.media_frame, width=600, height=300, bg="black")
        self.animation_canvas.pack()
        
        # Dictionary to hold PhotoImage objects (to avoid garbage collection)
        self.images = {}
        
        # Start the game
        self.start_game()

    def update_text(self, text):
        """Update the narrative text area with new text."""
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, text)
        self.text_area.config(state=tk.DISABLED)
        self.text_area.see(tk.END)
        self.root.update()

    def clear_buttons(self):
        """Remove all buttons from the button frame."""
        for widget in self.button_frame.winfo_children():
            widget.destroy()
            
    def clear_media(self):
        """Clear the animation canvas and media frame."""
        self.animation_canvas.delete("all")
        # Also clear any other media if added to media_frame (except canvas)
        for widget in self.media_frame.winfo_children():
            if widget != self.animation_canvas:
                widget.destroy()

    def add_button(self, text, command):
        """Add a button to the button frame with a given text and command."""
        btn = tk.Button(self.button_frame, text=text, command=command, width=30)
        btn.pack(pady=5)

    def display_image(self, image_file):
        """Display a static image in the media frame."""
        self.clear_media()
        try:
            # Load image if not already loaded
            if image_file not in self.images:
                self.images[image_file] = PhotoImage(file=image_file)
            img_label = tk.Label(self.media_frame, image=self.images[image_file])
            img_label.pack()
        except Exception as e:
            print(f"Error loading image {image_file}: {e}")

    # ------------------ STAGES AND BRANCHES ------------------

    # Stage 1: Game Start
    def start_game(self):
        self.clear_media()
        welcome_text = (
            "Welcome to the Sci-Fi Adventure Game!\n\n"
            "You wake up in a dimly lit spaceship with no memory of how you got here. "
            "The hum of the engines and distant alarms echo throughout the corridors.\n\n"
            "What will you do?"
        )
        self.update_text(welcome_text)
        self.clear_buttons()
        self.add_button("Explore the spaceship", self.explore_ship)
        self.add_button("Check inventory", self.check_inventory)
        self.add_button("Exit game", self.exit_game)
        self.display_image("spaceship.png")

    # Stage 2: Exploring the spaceship
    def explore_ship(self):
        self.clear_media()
        narrative = (
            "You start exploring the spaceship. The corridors twist into darkness "
            "with flickering lights, and you notice several areas of interest:\n\n"
            "1. A control panel with a blinking screen.\n"
            "2. A storage room with scattered supplies.\n"
            "3. A heavy door marked 'Engine Room'.\n"
            "4. A mysterious corridor with strange symbols on the walls."
        )
        self.update_text(narrative)
        self.clear_buttons()
        self.add_button("Investigate the control panel", self.control_panel)
        self.add_button("Search the storage room", self.search_storage)
        self.add_button("Enter the Engine Room", self.engine_room)
        self.add_button("Enter the mysterious corridor", self.mysterious_corridor)
        self.add_button("Return to main menu", self.start_game)
        self.display_image("spaceship.png")
    
    # Stage 3: Control Panel Branch
    def control_panel(self):
        self.clear_media()
        narrative = (
            "You approach the control panel. The screen flashes with an urgent message:\n"
            "'Critical system failure detected. Escape pod available.'\n\n"
            "But something seems off. You can either use the escape pod or try to access hidden logs."
        )
        self.update_text(narrative)
        self.clear_buttons()
        self.add_button("Use the escape pod", self.use_escape_pod)
        self.add_button("Investigate the ship's logs", self.investigate_logs)
        self.add_button("Return to exploring", self.explore_ship)
        self.display_image("artifact.png")

    def use_escape_pod(self):
        self.clear_media()
        # Instead of a static image, run an animation of the escape pod launching.
        self.update_text("You rush to the escape pod... Brace yourself for launch!")
        self.clear_buttons()
        self.animate_escape_pod()  # call the animation method

    def animate_escape_pod(self):
        """Animate the escape pod image moving upward from the bottom of the canvas."""
        self.animation_canvas.delete("all")
        try:
            if "escape_pod.png" not in self.images:
                self.images["escape_pod.png"] = PhotoImage(file="escape_pod.png")
            pod_img = self.images["escape_pod.png"]
        except Exception as e:
            print(f"Error loading escape pod image: {e}")
            return

        # Starting coordinates (centered at the bottom)
        x = self.animation_canvas.winfo_width() // 2
        y = self.animation_canvas.winfo_height() - 50
        image_obj = self.animation_canvas.create_image(x, y, image=pod_img)

        def move_pod():
            nonlocal y
            # Move the image upward
            self.animation_canvas.move(image_obj, 0, -5)
            y -= 5
            if y > -50:
                # Continue animation until the image is out of view
                self.root.after(50, move_pod)
            else:
                # Animation complete – display end message
                self.update_text(
                    "The escape pod rockets into space...\n"
                    "Game Over: You survived, but the mystery of the spaceship remains unsolved."
                )
                self.clear_buttons()
                self.add_button("Exit Game", self.exit_game)
        move_pod()

    def investigate_logs(self):
        self.clear_media()
        narrative = (
            "Diving into the ship's logs, you discover that the spaceship was involved in secret "
            "experiments with alien technology. Strange signals were detected just before the crisis.\n\n"
            "A new option appears: follow the alien signal to a hidden chamber."
        )
        self.update_text(narrative)
        self.clear_buttons()
        self.add_button("Follow the Alien Signal", self.alien_chamber)
        self.add_button("Return to exploring", self.explore_ship)
        self.display_image("alien.png")
    
    # Stage 4: Storage Room Branch
    def search_storage(self):
        self.clear_media()
        narrative = (
            "You enter the storage room. Dusty crates and scattered supplies fill the area.\n"
        )
        if "Small Key" not in inventory:
            inventory.append("Small Key")
            narrative += "After a careful search, you discover a Small Key tucked behind a crate. (Added to inventory)"
        else:
            narrative += "You search the room again but find nothing new."
        self.update_text(narrative)
        self.clear_buttons()
        self.add_button("Return to exploring", self.explore_ship)
        self.display_image("spaceship.png")
    
    # Stage 5: Engine Room Branch
    def engine_room(self):
        self.clear_media()
        narrative = (
            "You push open the heavy door leading to the Engine Room. The roar of the engines is overwhelming, "
            "and you see technicians desperately trying to stabilize a failing reactor.\n\n"
            "Amidst the chaos, you have two options:\n"
            "1. Help stabilize the reactor.\n"
            "2. Sneak into a side door to explore further."
        )
        self.update_text(narrative)
        self.clear_buttons()
        self.add_button("Help stabilize the reactor", self.stabilize_reactor)
        self.add_button("Sneak into the side door", self.sneak_side_door)
        self.add_button("Return to exploring", self.explore_ship)
        self.display_image("engine_room.png")

    def stabilize_reactor(self):
        self.clear_media()
        narrative = (
            "You rush to the reactor controls. With a combination of skill and luck, "
            "you manage to stabilize the reactor just in time.\n\n"
            "The technicians cheer, and a hidden compartment opens, revealing a mysterious artifact."
        )
        self.update_text(narrative)
        self.clear_buttons()
        if "Alien Artifact" not in inventory:
            inventory.append("Alien Artifact")
            narrative += "\n(Alien Artifact added to inventory)"
        self.add_button("Examine the artifact", self.examine_artifact)
        self.add_button("Return to exploring", self.explore_ship)
        self.display_image("artifact.png")

    def sneak_side_door(self):
        self.clear_media()
        narrative = (
            "You decide to avoid the chaos. Sneaking through the side door, you find yourself in a dim corridor "
            "that leads to a secret research lab filled with abandoned equipment and cryptic notes."
        )
        self.update_text(narrative)
        self.clear_buttons()
        self.add_button("Explore the research lab", self.research_lab)
        self.add_button("Return to exploring", self.explore_ship)
        self.display_image("lab.png")
    
    # Stage 6: Mysterious Corridor Branch
    def mysterious_corridor(self):
        self.clear_media()
        narrative = (
            "The mysterious corridor is lined with strange symbols and pulsing lights. You notice a riddle carved into the wall:\n\n"
            "\"I speak without a mouth and hear without ears. I have nobody, but I come alive with wind. What am I?\"\n\n"
            "Do you try to solve the riddle?"
        )
        self.update_text(narrative)
        self.clear_buttons()
        self.add_button("Solve the riddle", self.riddle_puzzle)
        self.add_button("Ignore and return to exploring", self.explore_ship)
        self.display_image("puzzle.png")
    
    def riddle_puzzle(self):
        self.clear_media()
        self.update_text("Enter your answer for the riddle:")
        self.clear_buttons()
        
        # Create entry widget for answer
        answer_entry = tk.Entry(self.button_frame, width=30, font=('Helvetica', 12))
        answer_entry.pack(pady=5)
        
        def check_answer():
            answer = answer_entry.get().strip().lower()
            if answer == "echo":
                messagebox.showinfo("Correct!", "The symbols glow and the corridor reveals a hidden door!")
                self.alien_chamber()
            else:
                messagebox.showerror("Incorrect", "That doesn't seem to be the right answer. Try again!")
        
        self.add_button("Submit Answer", check_answer)
        self.add_button("Give up and return", self.explore_ship)
        self.display_image("puzzle.png")
    
    # Stage 7: Alien Chamber Branch (Puzzle/Quiz)
    def alien_chamber(self):
        self.clear_media()
        narrative = (
            "Following the alien signal, you navigate through narrow passages until you reach a concealed chamber. "
            "The walls pulsate with an otherworldly glow and are covered with unknown glyphs.\n\n"
            "At the center of the chamber, a pedestal holds a glowing orb. A voice echoes in your mind, posing a challenge:\n"
            "\"Answer my query and unlock the secrets of the universe: What is the sum of 13 and 29?\"\n"
            "Enter your answer below."
        )
        self.update_text(narrative)
        self.clear_buttons()
        
        # Entry for the numeric puzzle
        answer_entry = tk.Entry(self.button_frame, width=30, font=('Helvetica', 12))
        answer_entry.pack(pady=5)
        
        def check_numeric_answer():
            answer = answer_entry.get().strip()
            if answer.isdigit() and int(answer) == 42:
                messagebox.showinfo("Correct!", "The orb pulses brightly as a portal opens to another dimension!")
                self.portal_adventure()
            else:
                messagebox.showerror("Incorrect", "The orb dims... That is not the correct answer!")
        
        self.add_button("Submit Answer", check_numeric_answer)
        self.add_button("Step away and return", self.explore_ship)
        self.display_image("alien.png")
    
    def portal_adventure(self):
        self.clear_media()
        narrative = (
            "With determination, you step into the swirling portal. Colors and shapes meld around you as "
            "you are transported to an alien world filled with vibrant landscapes, bizarre creatures, and endless mysteries.\n\n"
            "Your adventure continues on this strange new planet..."
        )
        self.update_text(narrative)
        self.clear_buttons()
        self.add_button("The End (to be continued)", self.exit_game)
        self.display_image("alien.png")
    
    # Stage 8: Research Lab Branch (Additional Quiz)
    def research_lab(self):
        self.clear_media()
        narrative = (
            "Inside the abandoned research lab, you discover files and experimental notes detailing hybrid research between human and alien DNA.\n\n"
            "On a dusty desk, a torn piece of paper catches your eye. It contains a riddle:\n"
            "\"I have keys but no locks. I have space but no rooms. You can enter, but can't go outside. What am I?\"\n"
            "Enter your answer below."
        )
        self.update_text(narrative)
        self.clear_buttons()
        
        # Entry for the lab quiz
        answer_entry = tk.Entry(self.button_frame, width=30, font=('Helvetica', 12))
        answer_entry.pack(pady=5)
        
        def check_lab_answer():
            answer = answer_entry.get().strip().lower()
            if answer in ("keyboard", "a keyboard"):
                messagebox.showinfo("Correct!", "A secret compartment opens revealing advanced alien equipment!")
                self.find_equipment()
            else:
                messagebox.showerror("Incorrect", "The paper fades... That answer seems to be incorrect!")
        
        self.add_button("Submit Answer", check_lab_answer)
        self.add_button("Ignore and return", self.explore_ship)
        self.display_image("lab.png")
    
    def find_equipment(self):
        self.clear_media()
        narrative = (
            "You rummage through the lab and find a set of advanced tools along with a mysterious gadget.\n\n"
            "The gadget hums with a strange energy and is now added to your inventory."
        )
        if "Mysterious Gadget" not in inventory:
            inventory.append("Mysterious Gadget")
        self.update_text(narrative)
        self.clear_buttons()
        self.add_button("Return to exploring", self.explore_ship)
        self.display_image("lab.png")
    
    # Additional branch: Examine Artifact (from Reactor stabilization branch)
    def examine_artifact(self):
        self.clear_media()
        narrative = (
            "You examine the Alien Artifact closely. Intricate patterns pulse along its surface, and you sense an "
            "inexplicable power emanating from within. Visions of distant galaxies and epic battles flash before your eyes.\n\n"
            "This artifact might hold the key to understanding your fate."
        )
        self.update_text(narrative)
        self.clear_buttons()
        self.add_button("Return to main menu", self.start_game)
        self.display_image("artifact.png")
    
    # Utility: Check Inventory
    def check_inventory(self):
        self.clear_media()
        if inventory:
            narrative = "Your inventory contains:\n" + "\n".join(f"- {item}" for item in inventory)
        else:
            narrative = "Your inventory is empty."
        self.update_text(narrative)
        self.clear_buttons()
        self.add_button("Back to main menu", self.start_game)
    
    # Exit game confirmation
    def exit_game(self):
        if messagebox.askokcancel("Quit", "Do you really want to exit the game?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AdventureGameApp(root)
    root.mainloop()
