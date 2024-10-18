import tkinter as tk
from tkinter import messagebox
import cv2  # OpenCV for video playback

# Encapsulation: Use of private variable to hide like and dislike counts.
class Video:
    def __init__(self, title):
        self._title = title  # Encapsulation: Private attribute (single underscore)
        self._likes = 0  # Encapsulated variable
        self._dislikes = 0  # Encapsulated variable

    def like(self):
        self._likes += 1

    def dislike(self):
        self._dislikes += 1

    def get_likes(self):
        return self._likes

    def get_dislikes(self):
        return self._dislikes

    def get_title(self):
        return self._title

    def play_video(self, video_path):
        cap = cv2.VideoCapture(video_path)

        # Check if the video file is opened successfully
        if not cap.isOpened():
            messagebox.showerror("Error", "Could not open video file.")
            return

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow("Video", frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


# Multiple inheritance: GUI class inherits from tk.Tk (Tkinter main window) and Video class.
class VideoApp(tk.Tk, Video):
    def __init__(self, title, video_path):
        tk.Tk.__init__(self)  # Calling the constructor of tk.Tk
        Video.__init__(self, title)  # Calling the constructor of Video

        self.video_path = video_path
        self.title("YouTube Like Interface")
        self.geometry("300x200")

        # Encapsulation: The video title is encapsulated and only accessible via get_title().
        self.label_title = tk.Label(self, text=self.get_title())
        self.label_title.pack(pady=10)

        # Polymorphism: Methods like(), dislike() will behave differently for different video objects.
        self.button_like = tk.Button(self, text="Like", command=self.like_video)
        self.button_like.pack(pady=5)

        self.button_dislike = tk.Button(self, text="Dislike", command=self.dislike_video)
        self.button_dislike.pack(pady=5)

        self.button_play = tk.Button(self, text="Play Video", command=self.play_video_button)
        self.button_play.pack(pady=5)

        self.label_feedback = tk.Label(self, text="Likes: 0, Dislikes: 0")
        self.label_feedback.pack(pady=20)

    # Method overriding: Customizing what happens when the button is clicked.
    def like_video(self):
        self.like()  # Call the like method from Video class
        self.update_feedback()

    def dislike_video(self):
        self.dislike()  # Call the dislike method from Video class
        self.update_feedback()

    def play_video_button(self):
        self.play_video(self.video_path)  # Call the play_video method from Video class

    def update_feedback(self):
        # Method overriding: Update the feedback for the current video instance.
        self.label_feedback.config(text=f"Likes: {self.get_likes()}, Dislikes: {self.get_dislikes()}")


# Decorator example: A function decorator to check login status
def login_required(func):
    def wrapper(*args, **kwargs):
        if args[0].is_logged_in:
            return func(*args, **kwargs)
        else:
            messagebox.showwarning("Login required", "You need to login first!")
    return wrapper


# Multiple inheritance and decorators used together
class User(VideoApp):
    def __init__(self, title, username, video_path):
        super().__init__(title, video_path)  # Calls the constructor of VideoApp
        self.username = username
        self.is_logged_in = False  # Encapsulation: Keeping track of login status.

        self.button_login = tk.Button(self, text="Login", command=self.login)
        self.button_login.pack(pady=5)

    # Decorator example applied to login-required actions.
    @login_required
    def like_video(self):
        super().like_video()

    @login_required
    def dislike_video(self):
        super().dislike_video()

    @login_required
    def play_video_button(self):
        super().play_video_button()

    def login(self):
        self.is_logged_in = True
        messagebox.showinfo("Login", f"Welcome {self.username}!")


# Polymorphism example: Creating multiple video objects that share the same interface.
class PremiumVideo(Video):
    def __init__(self, title, cost):
        super().__init__(title)
        self.cost = cost

    def get_cost(self):
        return self.cost


# Run the application
if __name__ == "__main__":
    video_file_path = video_file_path = r"C:\Users\hp\OneDrive\Documents\CDU\SEM 2\HIT137\tkinter application\Tkinter.mkv"
  # Provide the path to your video file
    app = User("Sample Video", "GROUPCAS302", video_file_path)
    app.mainloop()
