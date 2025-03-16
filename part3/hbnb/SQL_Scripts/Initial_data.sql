-- Insert admin user
-- The password 'admin1234' is hashed using bcrypt2
INSERT INTO user (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$tMdW.8OqaSGHGGSsBeUGBe9MxQLJgeRBr8ZjBYr1Xj0UIwLVrPLFi',
    TRUE
);

-- Insert initial amenities with generated UUIDs
INSERT INTO amenity (id, name) VALUES
    ('550e8400-e29b-41d4-a716-446655440000', 'WiFi'),
    ('550e8400-e29b-41d4-a716-446655440001', 'Swimming Pool'),
    ('550e8400-e29b-41d4-a716-446655440002', 'Air Conditioning');