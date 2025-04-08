-- Delete existing entries if needed
DELETE FROM places;

-- Then insert new data
INSERT INTO places (_title, _description, _price, _latitude, _longitude, _owner_id, id)
VALUES 
('The White House', 'The White House is the official residence of the US President', 9, 38.8977, -77.0365, '12345678-1234-1234-1234-123456789012', 'abcdef12-3456-7890-abcd-ef1234567890'),
('Eiffel Tower Apartment', 'Luxury apartment with views of the Eiffel Tower', 49, 48.8584, 2.2945, '0001', 'bcdef123-4567-890a-bcde-f12345678901'),
('Beach House', 'Beautiful beach house on the coast', 100, 34.0522, -118.2437, '0001', 'cdef1234-5678-90ab-cdef-123456789012'),
('Mountain Cabin', 'Cozy cabin in the mountains', 150, 39.5501, -105.7821, '0001', 'def12345-6789-0abc-def1-234567890123'),
('Downtown Loft', 'Modern loft in the heart of the city', 180, 40.7128, -74.0060, '0001', 'ef123456-7890-abcd-ef12-345678901234');