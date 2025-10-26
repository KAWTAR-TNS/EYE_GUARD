import sqlite3
import os
from kivy.core.window import Window
from kivy.app import App
from kivy.core.image import Image
from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

class StudentPage(Screen):
    def __init__(self, **kwargs):
        super(StudentPage, self).__init__(**kwargs)
        # Set background image
        with self.canvas.before:
            self.background = Rectangle(source='background.jpg', pos=self.pos, size=self.size)

        # Bind the update of the background size and position
        self.bind(size=self._update_background, pos=self._update_background)

        # Create a layout for the main content
        self.main_layout = BoxLayout(orientation='vertical')
        self.add_widget(self.main_layout)

        # Add title "PERSON" outside the ScrollView
        title_label = Label(text="STUDENT", bold=True, font_size=30, color=(0, 0, 0, 1), size_hint_y=None, height=50)
        self.main_layout.add_widget(title_label)

        # Initialize buttons
        self.add_button = Button(text="Add Student", size_hint_y=None, height=50, bold=True, background_color=(0.5, 0.8, 0.7))
        self.delete_button = Button(text="Delete Student by ID", size_hint_y=None, bold=True, height=50, background_color=(1, 0, 0, 1))
        self.update_button = Button(text="Update Student by ID", size_hint_y=None, bold=True, height=50, background_color=(0, 0, 1, 1))

        # Bind button events
        self.add_button.bind(on_press=self.add_student_popup)
        self.delete_button.bind(on_press=self.delete_student_by_id)
        self.update_button.bind(on_press=self.update_student_by_id)

        # Add buttons to the layout
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        button_layout.add_widget(self.add_button)
        button_layout.add_widget(self.delete_button)
        button_layout.add_widget(self.update_button)

        # Add button layout to the main layout
        self.main_layout.add_widget(button_layout)

        # Encapsulate the student layout in a ScrollView
        scroll_view = ScrollView()
        self.main_layout.add_widget(scroll_view)

        # Create a layout for the student records
        self.student_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.student_layout.bind(minimum_height=self.student_layout.setter('height'))
        scroll_view.add_widget(self.student_layout)

        # Display students
        self.display_students()

        # Add return button
        self.return_button = Button(text="Return", size_hint_y=None, height=50, bold=True,
                                    background_color=(0.7, 0.9, 1, 1))
        self.return_button.bind(on_press=self.return_to_main_menu)
        self.main_layout.add_widget(self.return_button)

    def _update_background(self, instance, value):
        self.background.pos = instance.pos
        self.background.size = instance.size

    def reload_page(self):
        # Clear the existing content
        self.student_layout.clear_widgets()

        # Display the updated content
        self.display_students()

    def display_students(self):
        # Retrieve students from the database
        students = self.retrieve_students_from_database()

        # Create labels to display each student's information
        for student in students:
            line_label = Label(text='-' * 600, color=(0, 0, 0, 1))
            self.student_layout.add_widget(line_label)
            student_info = f"ID: {student[0]}    IMM:  {student[1]}     FULL NAME: {student[2]}     MAJOR: {student[3]}"
            student_label = Label(text=student_info, bold=True, color=(0, 0, 0, 1), font_size=20, size_hint_y=None, height=50)
            self.student_layout.add_widget(student_label)

    def retrieve_students_from_database(self):
        # Establish a connection to the SQLite database
        conn = sqlite3.connect('eye.db')
        cursor = conn.cursor()

        # Execute a SELECT query to fetch all students
        cursor.execute("SELECT id, immatriculation, name, major, image FROM students")
        students = cursor.fetchall()

        # Close the connection
        conn.close()

        # Return the fetched students
        return students

    def add_student_popup(self, instance):
        # Function to display a popup for adding a new student
        popup_content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        immatriculation_input = TextInput(hint_text="Immatriculation", size_hint=(None, None), size=(300, 40))
        name_input = TextInput(hint_text="full name", size_hint=(None, None), size=(300, 40))
        major_input = TextInput(hint_text="major", size_hint=(None, None), size=(300, 40))
        file_chooser = FileChooserListView(path=os.getcwd(), size_hint_y=None, height=150)
        add_button = Button(text="Add", size_hint_y=None, height=50)
        popup_content.add_widget(immatriculation_input)
        popup_content.add_widget(name_input)
        popup_content.add_widget(major_input)
        popup_content.add_widget(file_chooser)
        popup_content.add_widget(add_button)

        def add_student_to_database(instance):
            immatriculation = immatriculation_input.text
            name = name_input.text
            major = major_input.text

            # Check if all fields are filled
            if immatriculation and name and major:
                image_path = file_chooser.selection and file_chooser.selection[0] or None
                image_data = self.get_image_data_from_path(image_path) if image_path else None

                # Insert the new student into the database
                conn = sqlite3.connect('eye.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO students (immatriculation, name, major, image) VALUES (?, ?, ?, ?)",
                               (immatriculation, name, major, image_data))
                conn.commit()
                conn.close()

                # Save image to authorized_faces directory
                if image_data:
                    self.save_image_to_directory(image_data, name )

                # Refresh the page to display the updated list of students
                self.reload_page()
                popup.dismiss()
            else:
                # Show an error message if any field is empty
                error_popup = Popup(title='Error', content=Label(text='All fields are required.'),
                                    size_hint=(None, None), size=(300, 200))
                error_popup.open()

        add_button.bind(on_press=add_student_to_database)

        popup = Popup(title='Add Student', content=popup_content, size_hint=(None, None), size=(500, 500))
        popup.open()

    def delete_student_by_id(self, instance, updat=None):
        # Function to display a popup for deleting a student by ID
        popup_content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        id_input = TextInput(hint_text="ID", size_hint=(None, None), size=(300, 40))
        delete_button = Button(text="Delete", size_hint_y=None, height=50)
        popup_content.add_widget(id_input)
        popup_content.add_widget(delete_button)

        def delete_student(instance):
            student_id = id_input.text

            # Retrieve student's immatriculation for image deletion
            student_name= self.retrieve_student_name_by_id(student_id)

            # Delete the student from the database by ID
            conn = sqlite3.connect('eye.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
            conn.commit()
            conn.close()

            # Remove image from authorized_faces directory
            self.remove_image_from_directory(student_name)

            # Refresh the page to display the updated list of students
            self.reload_page()
            popup.dismiss()

        delete_button.bind(on_press=delete_student)

        popup = Popup(title='Delete Student by ID', content=popup_content, size_hint=(None, None), size=(500, 200))
        popup.open(updat)

    def retrieve_student_name_by_id(self, student_id):
        # Retrieve the name of the student by ID
        conn = sqlite3.connect('eye.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM students WHERE id=?", (student_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        return None

    def save_image_to_directory(self, image_data, student_name):
        # Save the image data to the authorized_faces directory with student's name as the file name
        image_path = os.path.join("simple-face_recognition-main/EyeGuard-main/authorized_faces", f"{student_name}_student.jpg")
        with open(image_path, 'wb') as f:
            f.write(image_data)

    def remove_image_from_directory(self, student_name):
        # Remove the image file from the authorized_faces directory
        image_path = os.path.join("simple-face_recognition-main/EyeGuard-main/authorized_faces", f"{student_name}_student.jpg")
        if os.path.exists(image_path):
            os.remove(image_path)

    def update_student_by_id(self, instance):
        # Function to display a popup for updating a student by ID
        popup_content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        id_input = TextInput(hint_text="ID", size_hint=(None, None), size=(300, 40))
        immatriculation_input = TextInput(hint_text="Immatriculation", size_hint=(None, None), size=(300, 40))
        name_input = TextInput(hint_text="Name", size_hint=(None, None), size=(300, 40))
        major_input = TextInput(hint_text="Major", size_hint=(None, None), size=(300, 40))
        update_button = Button(text="Update", size_hint_y=None, height=50)
        popup_content.add_widget(id_input)
        popup_content.add_widget(immatriculation_input)
        popup_content.add_widget(name_input)
        popup_content.add_widget(major_input)
        popup_content.add_widget(update_button)

        def update_student(instance):
            student_id = id_input.text
            immatriculation = immatriculation_input.text
            name = name_input.text
            major = major_input.text

            # Update the student's information in the database by ID
            conn = sqlite3.connect('eye.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE students SET immatriculation=?, name=?, major=? WHERE id=?",
                           (immatriculation, name, major, student_id))
            conn.commit()
            conn.close()

            # Refresh the page to display the updated list of students
            self.reload_page()
            popup.dismiss()

        update_button.bind(on_press=update_student)

        popup = Popup(title='Update Student by ID', content=popup_content, size_hint=(None, None), size=(500, 250))
        popup.open()

    def get_image_data_from_path(self, image_path):
        # Function to read image data from file path
        if image_path:
            with open(image_path, 'rb') as f:
                return f.read()
        return None

    def return_to_main_menu(self, instance):
        # Navigate back to the Connected screen
        app = App.get_running_app()
        app.root.current = "connected"
class MyApp(App):
    def build(self):
        return StudentPage()

if __name__ == '__main__':
    MyApp().run()

