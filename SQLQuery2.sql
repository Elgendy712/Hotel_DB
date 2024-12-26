CREATE DATABASE HotelDB;
GO

USE HotelDB;
GO

CREATE TABLE Room (
    RoomID INT IDENTITY(1,1) PRIMARY KEY,    RoomNumber VARCHAR(10),
    RoomType VARCHAR(50),
    Capacity INT,
    PricePerNight DECIMAL(10, 2),
    AvailabilityStatus VARCHAR(20)
);

CREATE TABLE Guest (
    GuestID INT IDENTITY(1,1) PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    PhoneNumber VARCHAR(15),
    Email VARCHAR(100),
    Address VARCHAR(255)
);

CREATE TABLE Booking (
    BookingID INT IDENTITY(1,1) PRIMARY KEY,    CheckInDate DATE,
    CheckOutDate DATE,
    NumberOfGuests INT,
    BookingStatus VARCHAR(20),
    RoomID INT,
    GuestID INT,
    FOREIGN KEY (RoomID) REFERENCES Room(RoomID),
    FOREIGN KEY (GuestID) REFERENCES Guest(GuestID)
);

CREATE TABLE Billing (
    InvoiceID INT IDENTITY(1,1) PRIMARY KEY,
    TotalAmount DECIMAL(10, 2),
    PaymentStatus VARCHAR(20),
    PaymentMethod VARCHAR(50),
    BillingDate DATE,
    BookingID INT,
    FOREIGN KEY (BookingID) REFERENCES Booking(BookingID)
);

CREATE TABLE Service (
    ServiceID INT IDENTITY(1,1) PRIMARY KEY, 
    ServiceName VARCHAR(100),
    ServiceDescription TEXT,
    ServicePrice DECIMAL(10, 2)
);

CREATE TABLE ServiceUsage (
    ServiceUsageID INT IDENTITY(1,1) PRIMARY KEY,
    UsageDate DATE,
    Quantity INT,
    BookingID INT,
    ServiceID INT,
    FOREIGN KEY (BookingID) REFERENCES Booking(BookingID),
    FOREIGN KEY (ServiceID) REFERENCES Service(ServiceID)
);
