# === Defining Base Class ===

class Person:
    def __init__ (self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def display_info (self):
        # Displays general person info
        print(f"Name: {self.name}, Age: {self.age},Gender: {self.gender}")

# === Patient Subclass ===

class Patient(Person):
    patient_num = 1  # Class variable for auto-incrementing patient ID

    def __init__ (self, name, age, gender):
        super().__init__(name, age, gender)
        self.patient_id = f"P{Patient.patient_num:03}"  # e.g., P001
        self.appointment_list = []  # List to store appointments
        Patient.patient_num += 1  # Increment for the next patient

    def view_p_profile(self):
        # Displays patient details
        self.display_info()
        print(f"Patient ID: {self.patient_id}")  # FIXED from self.patient_num

    def view_appointments(self):
        # Show appointments if any exist
        if not self.appointment_list:
            print("No appointments scheduled.")
        else:
            print(f"Appointments for {self.name} (ID: {self.patient_id}):")
            for app in self.appointment_list:
                print(
                    f" - {app.appointment_id}: Dr. {app.doctor.name} on {app.date} at {app.time} | Status: {app.status}"
                )

# === Doctor Subclass ===

class Doctor(Person):
    doctor_num = 1  # Class variable for auto-incrementing doctor ID

    def __init__(self, name, age, gender, speciality, schedule):
        super().__init__(name, age, gender)
        self.doctor_id = f"D{Doctor.doctor_num:03}"  # e.g., D001
        self.speciality = speciality
        self.schedule = schedule  # List of available (date, time) slots
        Doctor.doctor_num += 1

    def available(self, date, time):
        # Check if the doctor is available at given date/time
        return (date, time) in self.schedule

    def view_schedule(self):
        # Display the doctor’s schedule
        print(f"Doctor {self.name}'s Schedule:")
        for slot in self.schedule:
            print(f" - {slot}")

# === Appointment Class ===

class Appointment:
    appointment_num = 1  # Class variable for auto-incrementing appointment ID

    def __init__(self, patient, doctor, date, time, status="Confirmed"):
        self.appointment_id = f"A{Appointment.appointment_num:03}"  # e.g., A001
        self.patient = patient
        self.doctor = doctor
        self.date = date
        self.time = time
        self.status = status
        Appointment.appointment_num += 1

    def confirm(self):
        self.status = "Confirmed"
        print(
            f"Appointment {self.appointment_id} confirmed for {self.patient.name} with Dr. {self.doctor.name} on {self.date} at {self.time}."
        )

    def cancel(self):
        self.status = "Cancelled"
        print(f"Appointment {self.appointment_id} has been cancelled.")

# === Hospital Management System Main Class ===

class HosSystem:
    def __init__ (self):
        self.patients = {}      # Dictionary to store patients by ID
        self.doctors = {}       # Dictionary to store doctors by ID
        self.appointments = {}  # Dictionary to store appointments by ID

    def add_patient(self, name, age, gender):
        # Add new patient after converting age to int
        try:
            age = int(age)
            patient = Patient(name, age, gender)
            self.patients[patient.patient_id] = patient
            print(f"Patient {patient.patient_id} successfully added.")
        except ValueError:
            print("Invalid Criteria Entered")

    def add_doctor(self, name, age, gender, speciality, schedule):
        # Add new doctor
        doctor = Doctor(name, age, gender, speciality, schedule)
        self.doctors[doctor.doctor_id] = doctor
        print(f"Doctor {doctor.doctor_id} successfully added.")

    def booking_appoint(self, patient_id, doctor_id, date, time):
        # Book an appointment between patient and doctor
        try:
            patient = self.patients[patient_id]
            doctor = self.doctors[doctor_id]
            if doctor.available(date, time):
                appointment = Appointment(patient, doctor, date, time)
                patient.appointment_list.append(appointment)
                self.appointments[appointment.appointment_id] = appointment
                doctor.schedule.remove((date, time))  # Mark slot as booked
                appointment.confirm()
            else:
                print("Sorry that slot is already taken")
        except ValueError:
            print("Invalid Patient or Doctor's ID.")

    def cancelling_booking(self, appointment_id):
        # Cancel an existing appointment
        if appointment_id in self.appointments:
            self.appointments[appointment_id].cancel()
        else:
            print("Appointment was not found.")

    def generate_bill(self, appointment_id, add_service=0):
        # Generate and display bill for appointment
        try:
            appointment = self.appointments[appointment_id]
            total = 5000 + add_service
            print("\n===== St Benedict Hospital =======")
            print(f"Patient: {appointment.patient.name}")
            print(f"Doctor: {appointment.doctor.name}")
            print(f"Doctor's Visit Fee: JMD$ 5000")
            print(f"Additional Services: JMD$ {add_service}")
            print(f"Total: JMD {total}")
            print("===================================")
        except ValueError:
            print("Invalid Appointment Number")

# === Main Menu UI ===

def main_menu(system):
    while True:
        # Display menu options
        print("\n=========== Aundrez Hospital Management System ================")
        print("1. Register a Patient")
        print("2. Add a Doctor")
        print("3. Book an Appointment")
        print("4. View the Patient Schedule")
        print("5. Cancel an Appointment")
        print("6. View your Bill Total")
        print("7. Exit")

        # Get user's choice and strip whitespace
        choice = input("Select an option to Proceed:").strip()

        # Register Patient
        if choice == '1':
            name = input("Enter Patient's Name:").strip()
            age = input("Enter Patient's Age:").strip()
            gender = input("Enter Patient's Gender:").strip()
            system.add_patient(name, age, gender)

        # Add Doctor
        elif choice == '2':
            name = input("Enter Doctor's Name:").strip()
            age = input("Enter Doctor's Age:").strip()
            gender = input("Enter Doctor's Gender:").strip()
            speciality = input("Enter Doctor's Speciality:").strip()
            schedule = []
            print("Enter available slots (type 'done' to finish):")
            while True:
                slot = input("Enter slot (format: YYYY-MM-DD HH:MM): ")
                if slot.lower() == 'done':
                    break
                try:
                    date, time = slot.split()
                    schedule.append((date, time))
                except ValueError:
                    print("Invalid Format. Please use 'YYYY-MM-DD HH:MM'")
            if schedule:
                system.add_doctor(name, age, gender, speciality, schedule)
            else:
                print("Doctor not added. No valid slots were provided.")

        # Book Appointment
        elif choice == '3':
            print("\nAvailable Patient IDs:")
            for pa_id in system.patients:
                print(f" - {pa_id}")

            print("\nAvailable Doctor IDs:")
            for do_id in system.doctors:
                print(f" - {do_id}")

            pa_id = input("Enter Patient ID (e.g. P001): ").strip()
            do_id = input("Enter Doctor ID (e.g. D001): ").strip()
            date = input("Enter date (YYYY-MM-DD): ").strip()
            time = input("Enter time (HH:MM): ").strip()
            system.booking_appoint(pa_id, do_id, date, time)

        # View Patient's Appointments
        elif choice == '4':
            print("\nAvailable Patient IDs:")
            for pid in system.patients:
                print(f" - {pid}")
            pid = input("Enter Patient ID: ").strip()
            if pid in system.patients:
                system.patients[pid].view_appointments()
            else:
                print("Patient not found.")

        # Cancel Appointment
        elif choice == '5':
            ap_id = input("Enter Appointment ID: ").strip()
            system.cancelling_booking(ap_id)

        # Generate Bill
        elif choice == '6':
            ap_id = input("Enter Appointment ID: ").strip()
            try:
                e_service = float(input("Enter additional service charges: ").strip())
            except ValueError:
                e_service = 0
            system.generate_bill(ap_id, e_service)

        # Exit Program
        elif choice == '7':
            print("Thank you for using HSM. Goodbye!")
            break

        # Invalid input
        else:
            print("Invalid Selection. Please try again.")

# === Main Program Entry Point ===

if __name__ == "__main__":
    hms = HosSystem()
    main_menu(hms)