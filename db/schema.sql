-- Create customers table
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT NOT NULL
);

-- Create tickets table
CREATE TABLE tickets (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    issue TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);