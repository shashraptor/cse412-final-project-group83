CREATE TABLE Users (
   userID SERIAL PRIMARY KEY,
   name VARCHAR(100) not null,
   dateOfBirth DATE not null,
   phoneNumber VARCHAR(15) not null unique,
   passportNumber VARCHAR(20) not null unique,
   email VARCHAR(100) not null unique,
   password VARCHAR(255) not null
);

CREATE TABLE Flight (
	flightID SERIAL PRIMARY KEY,
    flightDate DATE not null,
	departureTime VARCHAR(7) not null,
	arrivalTime VARCHAR(7) not null,
	startGate VARCHAR(3) not null,
	endGate VARCHAR(3) not null,
	startCity VARCHAR(50) not null,
	endCity VARCHAR(50) not null
);

CREATE TABLE Booking (
    bookingID SERIAL PRIMARY KEY,
	userID INT not null,
    flightID INT not null,
    bookingDate DATE not null,
    price NUMERIC not null,
    paymentMethod VARCHAR(50) not null,
    FOREIGN KEY (userID) REFERENCES Users (userID) ON
    DELETE CASCADE,
    FOREIGN KEY (flightID) REFERENCES Flight (flightID) ON
    DELETE CASCADE
);

CREATE TABLE Seat (
    flightID INT not null,
	seatNum VARCHAR(3) not null,
	bookingID INT,
	class VARCHAR(10) not null,
    FOREIGN KEY (flightID) REFERENCES Flight (flightID) ON
	DELETE CASCADE,
	FOREIGN KEY (bookingID) REFERENCES Booking (bookingID) ON
	DELETE SET NULL
);
