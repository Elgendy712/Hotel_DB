-- إنشاء قاعدة بيانات جديدة
CREATE DATABASE HotelDB;
GO

-- استخدام قاعدة البيانات الجديدة
USE HotelDB;
GO

-- إنشاء جدول Room
CREATE TABLE Room (
    RoomID INT IDENTITY(1,1) PRIMARY KEY, -- Auto Increment
    RoomNumber VARCHAR(10),
    RoomType VARCHAR(50),
    Capacity INT,
    PricePerNight DECIMAL(10, 2),
    AvailabilityStatus VARCHAR(20)
);

-- إنشاء جدول Guest
CREATE TABLE Guest (
    GuestID INT IDENTITY(1,1) PRIMARY KEY, -- Auto Increment
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    PhoneNumber VARCHAR(15),
    Email VARCHAR(100),
    Address VARCHAR(255)
);

-- إنشاء جدول Booking
CREATE TABLE Booking (
    BookingID INT IDENTITY(1,1) PRIMARY KEY, -- Auto Increment
    CheckInDate DATE,
    CheckOutDate DATE,
    NumberOfGuests INT,
    BookingStatus VARCHAR(20),
    RoomID INT,
    GuestID INT,
    FOREIGN KEY (RoomID) REFERENCES Room(RoomID),
    FOREIGN KEY (GuestID) REFERENCES Guest(GuestID)
);

-- إنشاء جدول Billing
CREATE TABLE Billing (
    InvoiceID INT IDENTITY(1,1) PRIMARY KEY, -- Auto Increment
    TotalAmount DECIMAL(10, 2),
    PaymentStatus VARCHAR(20),
    PaymentMethod VARCHAR(50),
    BillingDate DATE,
    BookingID INT,
    FOREIGN KEY (BookingID) REFERENCES Booking(BookingID)
);

-- إنشاء جدول Service
CREATE TABLE Service (
    ServiceID INT IDENTITY(1,1) PRIMARY KEY, -- Auto Increment
    ServiceName VARCHAR(100),
    ServiceDescription TEXT,
    ServicePrice DECIMAL(10, 2)
);

-- إنشاء جدول ServiceUsage
CREATE TABLE ServiceUsage (
    ServiceUsageID INT IDENTITY(1,1) PRIMARY KEY, -- Auto Increment
    UsageDate DATE,
    Quantity INT,
    BookingID INT,
    ServiceID INT,
    FOREIGN KEY (BookingID) REFERENCES Booking(BookingID),
    FOREIGN KEY (ServiceID) REFERENCES Service(ServiceID)
);
