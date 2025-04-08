DELETE FROM users;
-- Insert admin user
INSERT INTO users (id, _email, _first_name, _last_name, _password, _is_admin, created_at)
VALUES ('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'admin@hbnb.io', 'Admin', 'HBnB', '$2a$12$NlGI.VPRaWrTnR/1NcX0XuOnoa4f8jIrqW26cG0perXVH21HTpqnC', 1, DATETIME('now')),
('0001', 'test@test.test', 'testuser', 'big', '$2a$12$NlGI.VPRaWrTnR/1NcX0XuOnoa4f8jIrqW26cG0perXVH21HTpqnC', 0, DATETIME('now'));