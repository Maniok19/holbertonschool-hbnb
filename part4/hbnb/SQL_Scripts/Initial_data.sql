DELETE FROM users;
-- Insert admin user
INSERT INTO users (id, _email, _first_name, _last_name, _password, _is_admin, created_at)
VALUES ('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'admin@hbnb.io', 'Admin', 'HBnB', '$2a$12$NlGI.VPRaWrTnR/1NcX0XuOnoa4f8jIrqW26cG0perXVH21HTpqnC', 1, DATETIME('now')),
('0001', 'test@test.test', 'testuser', 'big', '$2a$12$NlGI.VPRaWrTnR/1NcX0XuOnoa4f8jIrqW26cG0perXVH21HTpqnC', 0, DATETIME('now'));

-- Delete existing entries if needed
DELETE FROM places;

-- Then insert new data
INSERT INTO places (_title, _description, _price, _latitude, _longitude, _owner_id, id)
VALUES 
('The White House', 'The White House is the official residence of the US President', 9, 38.8977, -77.0365, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'abcdef12-3456-7890-abcd-ef1234567890'),
('Eiffel Tower Apartment', 'Luxury apartment with views of the Eiffel Tower', 49, 48.8584, 2.2945, '0001', 'bcdef123-4567-890a-bcde-f12345678901'),
('Beach House', 'Beautiful beach house on the coast', 100, 34.0522, -118.2437, '0001', 'cdef1234-5678-90ab-cdef-123456789012'),
('Mountain Cabin', 'Cozy cabin in the mountains', 150, 39.5501, -105.7821, '0001', 'def12345-6789-0abc-def1-234567890123'),
('Downtown Loft', 'Modern loft in the heart of the city', 180, 40.7128, -74.0060, '0001', 'ef123456-7890-abcd-ef12-345678901234');

DELETE FROM amenities;
INSERT INTO amenities (id, _name) VALUES
    ('550e8400-e29b-41d4-a716-446655440000', 'WiFi'),
    ('550e8400-e29b-41d4-a716-446655440001', 'Swimming Pool'),
    ('550e8400-e29b-41d4-a716-446655440002', 'Air Conditioning');

-- Delete existing entries if needed
DELETE FROM reviews;

-- Then insert new data
INSERT INTO reviews (_text, _rating, _place_id, _user_id, id, created_at)
VALUES
('Great place to stay!', 5, 'abcdef12-3456-7890-abcd-ef1234567890', '36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'abcdef01-2345-6789-abcd-ef0123456789', DATETIME('now')),
('Not bad, but could be better.', 3, 'abcdef12-3456-7890-abcd-ef1234567890', '36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'bcdef012-3456-7890-abcd-f01234567890', DATETIME('now')),
('Terrible experience, would not recommend.', 1, 'abcdef12-3456-7890-abcd-ef1234567890', '36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'cdef0123-4567-8901-bcde-f12345678901', DATETIME('now'));

-- Delete existing entries if needed
DELETE FROM place_amenity;
-- Then insert new data
INSERT INTO place_amenity (place_id, amenity_id)
VALUES
('abcdef12-3456-7890-abcd-ef1234567890', '550e8400-e29b-41d4-a716-446655440000'),
('abcdef12-3456-7890-abcd-ef1234567890', '550e8400-e29b-41d4-a716-446655440001'),
('bcdef123-4567-890a-bcde-f12345678901', '550e8400-e29b-41d4-a716-446655440002'),
('abcdef12-3456-7890-abcd-ef1234567890', '550e8400-e29b-41d4-a716-446655440002');
