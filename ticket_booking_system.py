class Bus:
    def __init__(self, number, route, total_seats):
        self.number = str(number).strip()
        self.route = route
        self.total_seats = total_seats
        self.booked_seats = 0
    
    def available_seats(self):
        return self.total_seats - self.booked_seats
    
    def book_seat(self):
        if self.available_seats() > 0:
            self.booked_seats += 1
            return True
        return False
    
    def __str__(self):
        return f"Bus {self.number}: {self.route} ({self.available_seats()} seats available)"

class Passenger:
    def __init__(self, name, phone, bus):
        self.name = name
        self.phone = phone
        self.bus = bus
        self.fare = 500
    
    def __str__(self):
        return (f"Passenger: {self.name}\n"
                f"Phone: {self.phone}\n"
                f"Bus: {self.bus.number}\n"
                f"Route: {self.bus.route}\n"
                f"Fare: ৳{self.fare}")

class Admin:
    def __init__(self):
        self.username = "admin"
        self.password = "1234"
        self.is_logged_in = False
    
    def login(self, username, password):
        if username == self.username and password == self.password:
            self.is_logged_in = True
            return True
        return False
    
    def logout(self):
        self.is_logged_in = False

class BusSystem:
    def __init__(self):
        self.buses = []
        self.passengers = []
        self.admin = Admin()
    
    def find_bus(self, number):
        search_num = str(number).strip().lower()
        for bus in self.buses:
            if bus.number.lower() == search_num:
                return bus
        return None
    
    def add_bus(self, number, route, seats):
        if not self.admin.is_logged_in:
            print("Error: Admin access required")
            return False
        
        try:
            seats = int(seats)
            if seats <= 0:
                raise ValueError
        except ValueError:
            print("Error: Invalid seat count")
            return False
        
        if not number or not route:
            print("Error: Missing bus details")
            return False
        
        if self.find_bus(number):
            print(f"Error: Bus {number} already exists")
            return False
        
        self.buses.append(Bus(number, route, seats))
        print(f"Bus {number} added successfully")
        return True
    
    def show_buses(self, show_available_only=False):
        if not self.buses:
            print("No buses in system")
            return
        
        print("\nAvailable Buses:" if show_available_only else "\nAll Buses:")
        header = f"{'No.':<8}{'Route':<25}{'Seats':<10}{'Status':<15}"
        print(header)
        print("-" * len(header))
        
        for bus in self.buses:
            if show_available_only and bus.available_seats() <= 0:
                continue
            status = "Available" if bus.available_seats() > 0 else "Full"
            print(f"{bus.number:<8}{bus.route:<25}{bus.available_seats():<10}{status:<15}")
    
    def book_ticket(self, bus_number, name, phone):
        if not name or not phone:
            print("Error: Missing passenger details")
            return False
        
        bus = self.find_bus(bus_number)
        if not bus:
            print(f"Error: Bus {bus_number} not found")
            return False
        
        if bus.book_seat():
            passenger = Passenger(name, phone, bus)
            self.passengers.append(passenger)
            print("\nBooking successful!")
            print(passenger)
            return True
        else:
            print("Error: No seats available")
            return False
    
    def admin_menu(self):
        while True:
            print("\nAdmin Menu:")
            print("1. Add Bus")
            print("2. View All Buses")
            print("3. Logout")
            
            choice = input("Select option (1-3): ").strip()
            
            if choice == "1":
                print("\nAdd New Bus")
                number = input("Bus number: ").strip()
                route = input("Route: ").strip()
                seats = input("Total seats: ").strip()
                self.add_bus(number, route, seats)
            
            elif choice == "2":
                self.show_buses()
            
            elif choice == "3":
                self.admin.logout()
                print("Logged out successfully")
                break
            
            else:
                print("Invalid option")
    
    def user_menu(self):
        while True:
            print("\nMain Menu:")
            print("1. Admin Login")
            print("2. Book Ticket")
            print("3. View Available Buses")
            print("4. Exit")
            
            choice = input("Select option (1-4): ").strip()
            
            if choice == "3":
                self.show_buses(show_available_only=True)
            
            elif choice == "2":
                if not self.buses:
                    print("No buses available")
                    continue
                
                bus_number = input("Enter bus number: ").strip()
                name = input("Your name: ").strip()
                phone = input("Phone number: ").strip()
                self.book_ticket(bus_number, name, phone)
            
            elif choice == "1":
                if self.admin.is_logged_in:
                    print("Already logged in")
                    self.admin_menu()
                else:
                    username = input("Username: ").strip()
                    password = input("Password: ").strip()
                    if self.admin.login(username, password):
                        self.admin_menu()
                    else:
                        print("Login failed")
            
            elif choice == "4":
                print("Thank you for using our system")
                break
            
            else:
                print("Invalid option")

if __name__ == "__main__":
    system = BusSystem()
    system.user_menu()