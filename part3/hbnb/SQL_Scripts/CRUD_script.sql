-- SELECT operations
SELECT * FROM user;
SELECT * FROM amenity;

-- INSERT operations
-- Add a new user
INSERT INTO user (id, first_name, last_name, email, password)
VALUES (
    'f47ac10b-58cc-4372-a567-0e02b2c3d479',
    'Test',
    'User',
    'test@example.com',
    '$2b$12$nIWb.v4Qq5g6n2OIcjm3Yu9N4mHw9uV5vLZ7.8WdOkfR6OLuXH2Iy'
);

-- Add a new place
INSERT INTO place (id, title, description, price, latitude, longitude, owner_id)
VALUES (
    '7dc53df5-703e-49b3-8670-b1c468f47f1f',
    'Beautiful Apartment',
    'A cozy apartment in the heart of the city',
    120.00,
    40.7128,
    -74.0060,
    'f47ac10b-58cc-4372-a567-0e02b2c3d479'
);

-- Add a new review
INSERT INTO review (id, text, rating, user_id, place_id)
VALUES (
    '47bac150-58cc-4372-a567-0e02b2c3d480',
    'Amazing place with great views!',
    5,
    'f47ac10b-58cc-4372-a567-0e02b2c3d479',
    '7dc53df5-703e-49b3-8670-b1c468f47f1f'
);

-- Add amenities to a place
INSERT INTO place_amenity (place_id, amenity_id) VALUES
    ('7dc53df5-703e-49b3-8670-b1c468f47f1f', '550e8400-e29b-41d4-a716-446655440000'),
    ('7dc53df5-703e-49b3-8670-b1c468f47f1f', '550e8400-e29b-41d4-a716-446655440002');

-- UPDATE operations
-- Update user information
UPDATE user
SET last_name = 'UpdatedName'
WHERE id = 'f47ac10b-58cc-4372-a567-0e02b2c3d479';

-- Update place price
UPDATE place
SET price = 150.00
WHERE id = '7dc53df5-703e-49b3-8670-b1c468f47f1f';

-- UPDATE review rating
UPDATE review
SET rating = 4
WHERE id = '47bac150-58cc-4372-a567-0e02b2c3d480';

-- DELETE operations
-- Delete place_amenity relationship
DELETE FROM place_amenity
WHERE place_id = '7dc53df5-703e-49b3-8670-b1c468f47f1f'
AND amenity_id = '550e8400-e29b-41d4-a716-446655440002';

-- Delete review
DELETE FROM review
WHERE id = '47bac150-58cc-4372-a567-0e02b2c3d480';

-- Delete place
DELETE FROM place
WHERE id = '7dc53df5-703e-49b3-8670-b1c468f47f1f';

-- Delete user
DELETE FROM user
WHERE id = 'f47ac10b-58cc-4372-a567-0e02b2c3d479';

-- Verification queries
SELECT * FROM user WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';
SELECT * FROM amenity ORDER BY name;