# === Defining Base Class ===

class Person:
    def __init__(self, name, age, gender):
        # Initialize basic personal information
        self.name = name
        self.age = age
        self.gender = gender

    def display_info(self):
        # Print out person's basic information
        print(f"Name: {self.name}, Age: {self.age}, Gender: {self.gender}")


# === Patient Subclass ===

class Patient(Person):
    patient_num = 1  # Class-level counter to generate unique patient IDs

    def __init__(self, name, age, gender):
        super().__init__(name, age, gender)
        self.patient_id = f"P{Patient.patient_num:03}"  # Format: P001, P002...
        self.appointment_list = []  # List to hold patient’s appointments
        Patient.patient_num += 1

    def view_p_profile(self):
        # Display patient profile
        self.display_info()
        print(f"Patient ID: {self.patient_id}")

    def view_appointments(self):
        # List all scheduled appointments
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
    doctor_num = 1  # Class-level counter for doctor IDs

    def __init__(self, name, age, gender, speciality, schedule):
        super().__init__(name, age, gender)
        self.doctor_id = f"D{Doctor.doctor_num:03}"  # Format: D001, D002...
        self.speciality = speciality
        self.schedule = schedule  # List of (date, time) tuples
        Doctor.doctor_num += 1

    def available(self, date, time):
        # Check if a given (date, time) is in the doctor's schedule
        return (date, time) in self.schedule

    def view_schedule(self):
        # Print the doctor’s available appointment slots
        print(f"\nDoctor {self.name}'s Schedule:")
        if not self.schedule:
            print(" - No available slots.")
        for slot in self.schedule:
            print(f" - {slot[0]} at {slot[1]}")


# === Appointment Class ===

class Appointment:
    appointment_num = 1  # Class-level counter for appointment IDs

    def __init__(self, patient, doctor, date, time, status="Confirmed"):
        # Initialize appointment details
        self.appointment_id = f"A{Appointment.appointment_num:03}"
        self.patient = patient
        self.doctor = doctor
        self.date = date
        self.time = time
        self.status = status
        Appointment.appointment_num += 1

    def confirm(self):
        # Confirm the appointment and display message
        self.status = "Confirmed"
        print(
            f"Appointment {self.appointment_id} confirmed for {self.patient.name} with Dr. {self.doctor.name} on {self.date} at {self.time}."
        )

    def cancel(self):
        # Cancel the appointment and return slot to doctor
        self.status = "Cancelled"
        self.doctor.schedule.append((self.date, self.time))  # Add slot back
        print(f"Appointment {self.appointment_id} has been cancelled.")


# === Hospital Management System ===

class HosSystem:
    def __init__(self):
        # Initialize storage for patients, doctors, and appointments
        self.patients = {}
        self.doctors = {}
        self.appointments = {}

    def add_patient(self, name, age, gender):
        # Create and add new patient
        try:
            age = int(age)
            patient = Patient(name, age, gender)
            self.patients[patient.patient_id] = patient
            print(f"Patient {patient.patient_id} successfully added.")
        except ValueError:
            print("Invalid Criteria Entered")

    def add_doctor(self, name, age, gender, speciality, schedule):
        # Create and add new doctor
        doctor = Doctor(name, age, gender, speciality, schedule)
        self.doctors[doctor.doctor_id] = doctor
        print(f"Doctor {doctor.doctor_id} successfully added.")

    def booking_appoint(self, patient_id, doctor_id, date, time):
        # Book an appointment if doctor and patient exist and time is available
        if patient_id not in self.patients:
            print("Invalid Patient ID.")
            return
        if doctor_id not in self.doctors:
            print("Invalid Doctor ID.")
            return

        doctor = self.doctors[doctor_id]

        if doctor.available(date, time):
            patient = self.patients[patient_id]
            appointment = Appointment(patient, doctor, date, time)
            patient.appointment_list.append(appointment)
            self.appointments[appointment.appointment_id] = appointment
            doctor.schedule.remove((date, time))  # Mark time slot as used
            appointment.confirm()
        else:
            print("Sorry, that slot is already taken or unavailable.")

    def cancelling_booking(self, appointment_id):
        # Cancel an appointment if it exists
        if appointment_id in self.appointments:
            self.appointments[appointment_id].cancel()
        else:
            print("Appointment was not found.")

    def generate_bill(self, appointment_id, add_service=0):
        # Show the total cost of an appointment
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
        except KeyError:
            print("Invalid Appointment Number")


# === Command-Line Menu ===

def main_menu(system):
    while True:
        print("\n=========== Aundrez Hospital Management System ================")
        print("1. Register a Patient")
        print("2. Add a Doctor")
        print("3. Book an Appointment")
        print("4. View the Patient Schedule")
        print("5. Cancel an Appointment")
        print("6. View your Bill Total")
        print("7. Exit")

        choice = input("Select an option to Proceed: ").strip()

        if choice == '1':
            # Register a new patient
            name = input("Enter Patient's Name: ").strip()
            age = input("Enter Patient's Age: ").strip()
            gender = input("Enter Patient's Gender: ").strip()
            system.add_patient(name, age, gender)

        elif choice == '2':
            # Add a new doctor
            name = input("Enter Doctor's Name: ").strip()
            age = input("Enter Doctor's Age: ").strip()
            gender = input("Enter Doctor's Gender: ").strip()
            speciality = input("Enter Doctor's Speciality: ").strip()
            schedule = []
            print("Enter available slots (type 'done' to finish):")
            while True:
                slot = input("Enter slot (format: YYYY-MM-DD HH:MM): ").strip()
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

        elif choice == '3':
            # Book an appointment
            print("\nAvailable Patient IDs:")
            for pa_id in system.patients:
                print(f" - {pa_id}")

            print("\nAvailable Doctor IDs:")
            for do_id in system.doctors:
                print(f" - {do_id}")

            pa_id = input("Enter Patient ID (e.g. P001): ").strip()
            do_id = input("Enter Doctor ID (e.g. D001): ").strip()

            if do_id in system.doctors:
                system.doctors[do_id].view_schedule()

            date = input("Enter date (YYYY-MM-DD): ").strip()
            time = input("Enter time (HH:MM): ").strip()
            system.booking_appoint(pa_id, do_id, date, time)

        elif choice == '4':
            # View a patient's appointments
            print("\nAvailable Patient IDs:")
            for pid in system.patients:
                print(f" - {pid}")
            pid = input("Enter Patient ID: ").strip()
            if pid in system.patients:
                system.patients[pid].view_appointments()
            else:
                print("Patient not found.")

        elif choice == '5':
            # Cancel an appointment
            ap_id = input("Enter Appointment ID: ").strip()
            system.cancelling_booking(ap_id)

        elif choice == '6':
            # Generate a bill
            ap_id = input("Enter Appointment ID: ").strip()
            try:
                e_service = float(input("Enter additional service charges: ").strip())
            except ValueError:
                e_service = 0
            system.generate_bill(ap_id, e_service)

        elif choice == '7':
            # Exit the program
            print("Thank you for using HSM. Goodbye!")
            break

        else:
            print("Invalid Selection. Please try again.")


# === Main Program Entry Point ===

if __name__ == "__main__":
    hms = HosSystem()
    main_menu(hms)
