-- Insert exact fake data from documentation
INSERT INTO customers (id, name, city) VALUES (1, 'John Doe', 'New York');
INSERT INTO customers (id, name, city) VALUES (2, 'Jane Smith', 'London');
INSERT INTO customers (id, name, city) VALUES (3, 'Alex Brown', 'Toronto');

INSERT INTO tickets (id, customer_id, issue, status) VALUES (1, 1, 'Login not working', 'open');
INSERT INTO tickets (id, customer_id, issue, status) VALUES (2, 1, 'Password reset', 'close');
INSERT INTO tickets (id, customer_id, issue, status) VALUES (3, 3, 'Billing question', 'open');