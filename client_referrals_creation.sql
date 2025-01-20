CREATE TABLE client_referrals (
    id SERIAL PRIMARY KEY,
    client_name VARCHAR(100),
    asset_address VARCHAR(255),
	asset_price FLOAT,
	comission FLOAT,
    referral_date DATE,
    real_estate_agent_name VARCHAR(100),
	real_estate_agent_email VARCHAR(100),
	last_contact DATE,
	payment_collected BOOL
);

-- Insert sample data into the table
INSERT INTO client_referrals (client_name, asset_address, asset_price, comission, referral_date, real_estate_agent_name, real_estate_agent_email,last_contact,payment_collected)
VALUES
    ('Bob Smith', '456 Oak Ave, Riverside',100000,1.5, '2024-11-15', 'Jane Miller', 'janemiller@example.com','2025-01-12',True ),
    ('Charlie Brown', '789 Pine Rd, Hilltop',100000,1.5, '2024-12-05', 'Emily Davis', 'emilydavis@example.com','2025-01-12',True),
    ('Diana Prince', '321 Elm St, Meadowville',100000,1.5, '2025-01-10', 'Peter Parker', 'peterparker@example.com','2025-01-12',True),
	 ('Alice Johnson', '123 Maple St, Springfield',100000,1.5, '2025-01-10', 'Irene Garcia', 'moniregar@gmail.com','2025-01-10',False),
    ('Evan Wright', '654 Cedar Ln, Brookfield',100000,1.5,'2025-01-12', 'Bruce Wayne', 'brucewayne@example.com','2025-01-12',True);

-- Query the data to confirm it was added correctly
SELECT * FROM client_referrals;