-- Delete existing entries if needed
DELETE FROM reviews;

-- Then insert new data
INSERT INTO reviews (_text, _rating, _place_id, _user_id, id, created_at)
VALUES
('Great place to stay!', 5, 'abcdef12-3456-7890-abcd-ef1234567890', '36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'abcdef01-2345-6789-abcd-ef0123456789', DATETIME('now')),
('Not bad, but could be better.', 3, 'abcdef12-3456-7890-abcd-ef1234567890', '36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'bcdef012-3456-7890-abcd-f01234567890', DATETIME('now')),
('Terrible experience, would not recommend.', 1, 'abcdef12-3456-7890-abcd-ef1234567890', '36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'cdef0123-4567-8901-bcde-f12345678901', DATETIME('now'));