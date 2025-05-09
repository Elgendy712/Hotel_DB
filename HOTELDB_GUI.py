import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

def connect_to_db():
    try:
        conn = pyodbc.connect(
            "DRIVER={SQL Server};"
            "SERVER=LAPTOP-FPAGPIV8\\SQLEXPRESS;"
            "DATABASE=HotelDB;"
            "Trusted_Connection=yes;"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to connect to database: {str(e)}")
        return None

def fetch_guests():
    conn = connect_to_db()
    if conn is None:
        return []

    cursor = conn.cursor()
    cursor.execute("SELECT GuestID, FirstName, LastName, PhoneNumber, Email, Address FROM Guest")
    guests = cursor.fetchall()
    cursor.close()
    conn.close()
    return guests

def fetch_rooms():
    conn = connect_to_db()
    if conn is None:
        return []

    cursor = conn.cursor()
    cursor.execute("SELECT RoomID, RoomNumber, RoomType, Capacity, PricePerNight, AvailabilityStatus FROM Room")
    rooms = cursor.fetchall()
    cursor.close()
    conn.close()
    return rooms

def fetch_bookings():
    conn = connect_to_db()
    if conn is None:
        return []

    cursor = conn.cursor()
    cursor.execute("SELECT BookingID, CheckInDate, CheckOutDate, NumberOfGuests, BookingStatus, RoomID, GuestID FROM Booking")
    bookings = cursor.fetchall()
    cursor.close()
    conn.close()
    return bookings

def populate_guests_table():
    guests_table.delete(*guests_table.get_children())
    for row in fetch_guests():
        guests_table.insert("", "end", values=row)

def populate_rooms_table():
    rooms_table.delete(*rooms_table.get_children())
    for row in fetch_rooms():
        rooms_table.insert("", "end", values=row)

def populate_bookings_table():
    bookings_table.delete(*bookings_table.get_children())
    for row in fetch_bookings():
        bookings_table.insert("", "end", values=row)

def add_guest():
    conn = connect_to_db()
    if conn is None:
        return

    cursor = conn.cursor()
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    phone = entry_phone.get()
    email = entry_email.get()
    address = entry_address.get()

    try:
        cursor.execute("INSERT INTO Guest (FirstName, LastName, PhoneNumber, Email, Address) VALUES (?, ?, ?, ?, ?)",
                       (first_name, last_name, phone, email, address))
        conn.commit()
        messagebox.showinfo("Success", "Guest added successfully!")
        populate_guests_table()
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        cursor.close()
        conn.close()

def delete_guest():
    conn = connect_to_db()
    if conn is None:
        return

    cursor = conn.cursor()
    guest_id = entry_delete_guest_id.get()

    try:
        cursor.execute("DELETE FROM Guest WHERE GuestID = ?", (guest_id,))
        conn.commit()
        messagebox.showinfo("Success", "Guest deleted successfully!")
        populate_guests_table()
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        cursor.close()
        conn.close()

def make_booking():
    conn = connect_to_db()
    if conn is None:
        return

    cursor = conn.cursor()
    guest_id = entry_guest_id.get()
    room_id = entry_room_id.get()
    check_in = entry_check_in.get()
    check_out = entry_check_out.get()
    num_guests = entry_num_guests.get()

    try:
        cursor.execute("INSERT INTO Booking (CheckInDate, CheckOutDate, NumberOfGuests, BookingStatus, RoomID, GuestID) VALUES (?, ?, ?, 'Confirmed', ?, ?)",
                       (check_in, check_out, num_guests, room_id, guest_id))
        conn.commit()
        messagebox.showinfo("Success", "Booking made successfully!")
        populate_bookings_table()
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        cursor.close()
        conn.close()

def view_invoice():
    conn = connect_to_db()
    if conn is None:
        return

    cursor = conn.cursor()
    booking_id = entry_booking_id.get()

    try:
        cursor.execute("""
            SELECT 
                b.TotalAmount, 
                b.PaymentStatus, 
                b.PaymentMethod, 
                b.BillingDate,
                (SELECT COALESCE(SUM(s.ServicePrice * su.Quantity), 0)
                 FROM ServiceUsage su
                 JOIN Service s ON su.ServiceID = s.ServiceID
                 WHERE su.BookingID = b.BookingID) AS ServiceCost
            FROM Billing b
            WHERE b.BookingID = ?
        """, (booking_id,))
        invoice = cursor.fetchone()
        if invoice:
            total_with_services = invoice[0] + invoice[4]
            messagebox.showinfo("Invoice", f"Total Amount: {total_with_services}\nPayment Status: {invoice[1]}\nPayment Method: {invoice[2]}\nBilling Date: {invoice[3]}")
        else:
            messagebox.showinfo("Invoice", "No invoice found for this booking.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        cursor.close()
        conn.close()

root = tk.Tk()
root.title("Hotel Reservation System")
root.geometry("1200x800")

top_frame = tk.Frame(root)
top_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

guest_frame = tk.LabelFrame(top_frame, text="Add Guest", padx=10, pady=10)
guest_frame.pack(side=tk.LEFT, padx=10, pady=10)

tk.Label(guest_frame, text="First Name").grid(row=0, column=0, sticky=tk.W)
entry_first_name = tk.Entry(guest_frame)
entry_first_name.grid(row=0, column=1)

tk.Label(guest_frame, text="Last Name").grid(row=1, column=0, sticky=tk.W)
entry_last_name = tk.Entry(guest_frame)
entry_last_name.grid(row=1, column=1)

tk.Label(guest_frame, text="Phone").grid(row=2, column=0, sticky=tk.W)
entry_phone = tk.Entry(guest_frame)
entry_phone.grid(row=2, column=1)

tk.Label(guest_frame, text="Email").grid(row=3, column=0, sticky=tk.W)
entry_email = tk.Entry(guest_frame)
entry_email.grid(row=3, column=1)

tk.Label(guest_frame, text="Address").grid(row=4, column=0, sticky=tk.W)
entry_address = tk.Entry(guest_frame)
entry_address.grid(row=4, column=1)

add_guest_button = tk.Button(guest_frame, text="Add Guest", command=add_guest)
add_guest_button.grid(row=5, columnspan=2, pady=5)

delete_frame = tk.LabelFrame(top_frame, text="Delete Guest", padx=10, pady=10)
delete_frame.pack(side=tk.LEFT, padx=10, pady=10)

tk.Label(delete_frame, text="Guest ID").grid(row=0, column=0, sticky=tk.W)
entry_delete_guest_id = tk.Entry(delete_frame)
entry_delete_guest_id.grid(row=0, column=1)

delete_guest_button = tk.Button(delete_frame, text="Delete Guest", command=delete_guest)
delete_guest_button.grid(row=1, columnspan=2, pady=5)

booking_frame = tk.LabelFrame(top_frame, text="Make Booking", padx=10, pady=10)
booking_frame.pack(side=tk.LEFT, padx=10, pady=10)

tk.Label(booking_frame, text="Guest ID").grid(row=0, column=0, sticky=tk.W)
entry_guest_id = tk.Entry(booking_frame)
entry_guest_id.grid(row=0, column=1)

tk.Label(booking_frame, text="Room ID").grid(row=1, column=0, sticky=tk.W)
entry_room_id = tk.Entry(booking_frame)
entry_room_id.grid(row=1, column=1)

tk.Label(booking_frame, text="Check-in Date (YYYY-MM-DD)").grid(row=2, column=0, sticky=tk.W)
entry_check_in = tk.Entry(booking_frame)
entry_check_in.grid(row=2, column=1)

tk.Label(booking_frame, text="Check-out Date (YYYY-MM-DD)").grid(row=3, column=0, sticky=tk.W)
entry_check_out = tk.Entry(booking_frame)
entry_check_out.grid(row=3, column=1)

tk.Label(booking_frame, text="Number of Guests").grid(row=4, column=0, sticky=tk.W)
entry_num_guests = tk.Entry(booking_frame)
entry_num_guests.grid(row=4, column=1)

make_booking_button = tk.Button(booking_frame, text="Make Booking", command=make_booking)
make_booking_button.grid(row=5, columnspan=2, pady=5)

invoice_frame = tk.LabelFrame(top_frame, text="View Invoice", padx=10, pady=10)
invoice_frame.pack(side=tk.LEFT, padx=10, pady=10)

tk.Label(invoice_frame, text="Booking ID").grid(row=0, column=0, sticky=tk.W)
entry_booking_id = tk.Entry(invoice_frame)
entry_booking_id.grid(row=0, column=1)

view_invoice_button = tk.Button(invoice_frame, text="View Invoice", command=view_invoice)
view_invoice_button.grid(row=1, columnspan=2, pady=5)

bottom_frame = tk.Frame(root)
bottom_frame.pack(side=tk.BOTTOM, padx=10, pady=10, fill=tk.BOTH, expand=True)

bookings_frame = tk.LabelFrame(bottom_frame, text="Bookings", padx=10, pady=10)
bookings_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

bookings_table = ttk.Treeview(bookings_frame, columns=("BookingID", "CheckInDate", "CheckOutDate", "NumberOfGuests", "BookingStatus", "RoomID", "GuestID"), show="headings")
for col in bookings_table["columns"]:
    bookings_table.heading(col, text=col)
    bookings_table.column(col, width=100)
bookings_table.pack(fill=tk.BOTH, expand=True)

tables_frame = tk.Frame(bottom_frame)
tables_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

guests_frame = tk.LabelFrame(tables_frame, text="Guests", padx=10, pady=10)
guests_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

guests_table = ttk.Treeview(guests_frame, columns=("GuestID", "FirstName", "LastName", "PhoneNumber", "Email", "Address"), show="headings")
for col in guests_table["columns"]:
    guests_table.heading(col, text=col)
    guests_table.column(col, width=100)
guests_table.pack(fill=tk.BOTH, expand=True)

rooms_frame = tk.LabelFrame(tables_frame, text="Rooms", padx=10, pady=10)
rooms_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

rooms_table = ttk.Treeview(rooms_frame, columns=("RoomID", "RoomNumber", "RoomType", "Capacity", "PricePerNight", "AvailabilityStatus"), show="headings")
for col in rooms_table["columns"]:
    rooms_table.heading(col, text=col)
    rooms_table.column(col, width=100)
rooms_table.pack(fill=tk.BOTH, expand=True)

populate_guests_table()
populate_rooms_table()
populate_bookings_table()

root.mainloop()