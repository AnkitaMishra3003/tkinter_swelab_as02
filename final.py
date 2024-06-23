import re
import tkinter as tk
from tkinter import messagebox, simpledialog

class Person:
    def __init__(self, user_id, password, name,role,count):
        self.user_id = user_id
        self.password = password
        self.name = name
        self.role=role
        self.count=count

class Teacher(Person):
    def __init__(self, user_id, password, name ,role ,count, subject):
        super().__init__(user_id, password, name ,role ,count)
        self.subject=subject

class Student(Person):
    def __init__(self, user_id, password, name, role, count ,dept):
        super().__init__(user_id, password, name, role, count)
        self.dept=dept

class UGStudent(Student):
    def __init__(self, user_id, password, name, role, count, dept, course):
        super().__init__(user_id, password, name, role, count, dept)
        self.course=course

class PGStudent(Student):
    def __init__(self, user_id, password, name, role, count, dept, year):
        super().__init__(user_id, password, name, role, count, dept)
        self.year=year

class AcademicUnitSystem:
    def __init__(self):
        self.users = []

    def is_valid_password(self, password):
        # Password validation logic
        if 8 <= len(password) <= 12 and re.search(r'[A-Z]', password) and re.search(r'[a-z]', password) \
                and re.search(r'\d', password) and re.search(r'[!@#$%&*]', password) and ' ' not in password:
            return True
        else:
            return False
        
    def register_user(self, user):
        if user.user_id.endswith('@gmail.com') and self.is_valid_password(user.password):
            for one in self.users:
                if one.user_id==user.user_id:
                    messagebox.showerror("Registration Error", "Account with same user id already exists.Log in with correct password.")
                    return False
            self.users.append(user)
            return True
        else:
            return False

    def authenticate_user(self, user_id, entered_password):
        user = next((u for u in self.users if u.user_id == user_id), None)
        if user and user.password==entered_password:
            user.count=0
            return user
        elif user:
            user.count=user.count+1
            if user.count==3:
                self.users.remove(user)
                messagebox.showinfo("Deregistration", "3 failed login attempts. Account successfully deactivated.") 
            return None
        else:
            return None

    def deregister_user(self, user):
        self.users.remove(user)
        messagebox.showinfo("Deregistration", "Account successfully deactivated.")

class UserInterface:
    def __init__(self, academic_unit_system):
        self.academic_unit_system = academic_unit_system
        self.root = tk.Tk()
        self.root.title("Academic Unit System")
        label=tk.Label(self.root,text='''A valid password should satisfy the following: 
a) It should be within 8-12 character long. 
b) It should contain at least one upper case, one digit, and one lower case. 
c) It should contains one or more special character(s) from the list [! @ # $ % & *] 
d) No blank space will be allowed. 
 A valid gmail_id must end with @gmail.com''',font=("Courier New", 10),borderwidth=2, relief="solid",bg='lightgrey')
        label.pack()

        self.create_widgets()

    def create_widgets(self):
        # Labels
        self.label_name = tk.Label(self.root, text="Name:")
        self.label_user_id = tk.Label(self.root, text="User ID:")
        self.label_password = tk.Label(self.root, text="Password:")
        self.label_role = tk.Label(self.root, text="Role:")
        

        # Entry fields
        self.entry_name = tk.Entry(self.root)
        self.entry_user_id = tk.Entry(self.root)
        self.entry_password = tk.Entry(self.root, show="*")
        self.role_var = tk.StringVar()
        self.role_var.set("Teacher")
        self.role_options = ["Teacher", "UG Student", "PG Student"]
        self.role_menu = tk.OptionMenu(self.root, self.role_var, *self.role_options)

        # Buttons
        self.button_register = tk.Button(self.root, text="Register", command=self.register_user)
        self.button_login = tk.Button(self.root, text="Login", command=self.login)

        # Pack elements
        self.label_name.pack()
        self.entry_name.pack()
        self.label_user_id.pack()
        self.entry_user_id.pack()
        self.label_password.pack()
        self.entry_password.pack()
        self.label_role.pack()
        self.role_menu.pack()

        #Conditions
        self.label_subject = tk.Label(self.root, text="Subject(If teacher):")
        self.entry_subject = tk.Entry(self.root)
        self.label_subject.pack()
        self.entry_subject.pack()
        self.label_dept = tk.Label(self.root, text="Department(If Student):")
        self.entry_dept = tk.Entry(self.root)
        self.label_dept.pack()
        self.entry_dept.pack()
        self.label_course = tk.Label(self.root, text="Course(If UG Student):")
        self.course_var = tk.StringVar()
        self.course_var.set("BTech")
        self.course_options = ["Btech", "Dual Degree"]
        self.course_menu = tk.OptionMenu(self.root, self.course_var, *self.course_options)
        self.label_course.pack()
        self.course_menu.pack()
        self.label_year = tk.Label(self.root, text="Year(If PG Student):")
        self.year_var = tk.StringVar()
        self.year_var.set("1st Year")
        self.year_options = ["1st Year", "2nd Year"]
        self.year_menu = tk.OptionMenu(self.root, self.year_var, *self.year_options)
        self.label_year.pack()
        self.year_menu.pack()

        #Final Buttons
        self.button_register.pack()
        self.button_login.pack()


    def register_user(self):
        name = self.entry_name.get()
        user_id = self.entry_user_id.get()
        password = self.entry_password.get()
        role = self.role_var.get()
        subject=self.entry_subject.get()
        dept=self.entry_dept.get()
        course=self.course_var.get()
        year=self.year_var.get()
        if role=='Teacher':
            new_user=Teacher(user_id,password,name,role,0,subject)
        elif role=='UG Student':
            new_user=UGStudent(user_id,password,name,role,0,dept,course)
        else:
            new_user=PGStudent(user_id,password,name,role,0,dept,year)

        if self.academic_unit_system.register_user(new_user):
            messagebox.showinfo("Registration", "User registered successfully.")
        else:
            messagebox.showerror("Registration Error", "Invalid user ID or Password.")

    def login(self):
        user_id = self.entry_user_id.get()
        password = self.entry_password.get()

        user = self.academic_unit_system.authenticate_user(user_id, password)
        if user:
            self.show_profile_options(user)
        else:
            messagebox.showerror("Login Error", "Invalid credentials.")

    def show_profile_options(self, user):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Add profile information
        tk.Label(self.root, text=f"Welcome, {user.name}!").pack()
        tk.Label(self.root, text=f"User_ID: {user.user_id}").pack()
        tk.Label(self.root, text=f"Password: {user.password}").pack()
        tk.Label(self.root, text=f"Role: {user.role}").pack()
        if(user.role=='Teacher'):
            tk.Label(self.root, text=f"Subject: {user.subject}").pack()
        else:
            tk.Label(self.root, text=f"Department: {user.dept}").pack()
            if user.role=='UG Student':
                tk.Label(self.root, text=f"Course: {user.course}").pack()
            else:
                tk.Label(self.root, text=f"Year: {user.year}").pack()

        tk.Button(self.root, text="Edit User ID", command=lambda: self.edit_user_id(user)).pack()
        tk.Button(self.root, text="Edit Name", command=lambda: self.edit_name(user)).pack()

        if(user.role=='Teacher'):
            tk.Button(self.root, text="Change Subject: ", command=lambda: self.edit_subject(user)).pack()
        else:
            tk.Button(self.root, text="Change dept: ", command=lambda: self.edit_dept(user)).pack()
            if user.role=='UG Student':
                tk.Button(self.root, text="Change Course: ", command=lambda: self.edit_course(user)).pack()
            else:
                tk.Button(self.root, text="Change Year", command=lambda: self.edit_year(user)).pack()

        tk.Button(self.root, text="Change Password", command=lambda: self.change_password(user)).pack()
        tk.Button(self.root, text="Deregister", command=lambda: self.deregister_user(user)).pack()
        tk.Button(self.root, text="Logout", command=self.logout).pack()

    def edit_user_id(self, user):
        new_user_id = simpledialog.askstring("Edit User ID", "Enter new user ID:")
        if new_user_id and new_user_id.endswith('@gmail.com'):
            user.user_id = new_user_id
            messagebox.showinfo("Edit User ID", "User ID updated successfully.")
        else:
            messagebox.showerror("Edit User ID Error", "Invalid user ID. Must end with @gmail.com")


    def edit_name(self, user):
        new_name = simpledialog.askstring("Edit Name", "Enter new name:")
        if new_name:
            user.name = new_name
            messagebox.showinfo("Edit Name", "Name updated successfully.")
        else:
            messagebox.showwarning("Edit Name", "Name change canceled.")

    def edit_subject(self, user):
        new_subject = simpledialog.askstring("Edit Subject", "Enter new Subject:")
        if new_subject:
            user.subject = new_subject
            messagebox.showinfo("Edit Subject", "Subject updated successfully.")
        else:
            messagebox.showwarning("Edit Subject", "Subject change canceled.")

    def edit_dept(self, user):
        new_dept = simpledialog.askstring("Edit Department", "Enter new Department:")
        if new_dept:
            user.dept = new_dept
            messagebox.showinfo("Edit Department", "Department updated successfully.")
        else:
            messagebox.showwarning("Edit Department", "Department change canceled.")
    def edit_course(self, user):
        new_course=simpledialog.askstring("Edit Course", "Enter new Course:")
        if new_course:
            user.course = new_course
            messagebox.showinfo("Edit Course", "Course updated successfully.")
        else:
            messagebox.showwarning("Edit Course", "Course change canceled.")
    def edit_year(self, user):
        new_year = simpledialog.askstring("Edit Year", "Enter new Year:")
        if new_year:
            user.name = new_year
            messagebox.showinfo("Edit Year", "Year updated successfully.")
        else:
            messagebox.showwarning("Edit Year", "Year change canceled.")
    def change_password(self, user):
        new_password = simpledialog.askstring("Change Password", "Enter new password:")
        if new_password and self.academic_unit_system.is_valid_password(new_password):
            user.password = new_password
            messagebox.showinfo("Password Changed", "Password changed successfully.")
        else:
            messagebox.showwarning("Password Change", "Password change canceled.Give a valid Password")

    def deregister_user(self, user):
        # Ask for password for validation
        entered_password = simpledialog.askstring("Deregistration", "Enter your password:")
        
        if entered_password == user.password:
            self.academic_unit_system.deregister_user(user)
            messagebox.showinfo("Deregistration", "Account successfully deactivated.")
            # Go back to the login/register screen after deregistration
            for widget in self.root.winfo_children():
                widget.destroy()
            self.create_widgets()
        else:
            messagebox.showerror("Deregistration Error", "Invalid password. Deregistration failed.")
    def logout(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_widgets()
    def run(self):
        self.root.mainloop()

# Example usage
academic_unit_system = AcademicUnitSystem()
ui = UserInterface(academic_unit_system)
ui.run()
