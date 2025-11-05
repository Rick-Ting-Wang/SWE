-- ###########################################################
-- Script Purpose: Insert initial system data (users/organizations/classes/activities and other base data)
-- Prerequisites: The table structure creation script has been executed and the database name is `your_database_name`
-- Password Info:
-- - All password hashes correspond to the original plaintext (e.g., admin123 → $2b$12$...)
-- - If you need to change a password, generate a new bcrypt hash (tool: https://bcrypt-generator.com/)
-- Execution Order: Execute in strict order to avoid foreign key constraint errors
-- ###########################################################

-- Switch to the target database
USE your_database_name;

-- 1. Insert user data (including admin, school, and community roles)
INSERT INTO users (username, email, password_hash, user_type)
VALUES 
-- System Admin: username=asnawi, password=admin123
('asnawi', 'asnawi@komodo.org', '$2b$12$EixZaYb05a2eQ8GLs5aK4eBqUc9F3x7y8z9A0B1C2D3E4F5G6H7I8J', 'admin'),
-- School Principal: username=khairunnisa, password=principal123
('khairunnisa', 'khairunnisa@ujungraya.sch.id', '$2b$12$A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X', 'principal'),
-- School Admin: username=ayu_lestari, password=admin123
('ayu_lestari', 'ayu@ujungraya.sch.id', '$2b$12$EixZaYb05a2eQ8GLs5aK4eBqUc9F3x7y8z9A0B1C2D3E4F5G6H7I8J', 'school_admin'),
-- Teacher 1: username=bintang_akbar, password=teacher123
('bintang_akbar', 'bintang@ujungraya.sch.id', '$2b$12$B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y', 'teacher'),
-- Teacher 2: username=maya_sari, password=teacher123
('maya_sari', 'maya@ujungraya.sch.id', '$2b$12$B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y', 'teacher'),
-- Students 1-5: password=student123
('student1', 'student1@ujungraya.sch.id', '$2b$12$C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z', 'student'),
('student2', 'student2@ujungraya.sch.id', '$2b$12$C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z', 'student'),
('student3', 'student3@ujungraya.sch.id', '$2b$12$C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z', 'student'),
('student4', 'student4@ujungraya.sch.id', '$2b$12$C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z', 'student'),
('student5', 'student5@ujungraya.sch.id', '$2b$12$C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z', 'student'),
-- Community Chair: username=besoeki_rachmat, password=chair123
('besoeki_rachmat', 'besoeki@saveouranimals.org', '$2b$12$D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z6A', 'community_chair'),
-- Community Members 1-3: password=member123
('community_member1', 'member1@saveouranimals.org', '$2b$12$E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z6A7B', 'community_member'),
('community_member2', 'member2@saveouranimals.org', '$2b$12$E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z6A7B', 'community_member'),
('community_member3', 'member3@saveouranimals.org', '$2b$12$E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z6A7B', 'community_member'),
-- Management Team: password=director123 / security123
('tegar_prayudi', 'tegar@komodo.org', '$2b$12$F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z6A7B8C', 'admin'),
('bhaskara', 'bhaskara@komodo.org', '$2b$12$G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z6A7B8C9D', 'admin');
-- Info: 16 users inserted


-- 2. Insert organization data (schools + community)
INSERT INTO organizations (org_type, org_name, org_profile, is_public, subscription_status, subscription_date)
VALUES 
-- School 1: Ujung Raya Primary School
('school', 'Ujung Raya Primary School', 
 'Located in Ujung Kulon, conservation area for Javan Rhinoceros', 
 TRUE, 'active', '2024-01-15'),
-- Community 1: #SaveOurAnimals Community
('community', '#SaveOurAnimals Community', 
 'Established in 2011, one of the biggest animal conservation communities in Indonesia', 
 TRUE, 'active', '2024-02-01'),
-- School 2: Jakarta Green School
('school', 'Jakarta Green School',
 'Urban school focused on environmental education',
 TRUE, 'active', '2024-03-01');
-- Info: 3 organizations inserted


-- 3. Insert organization member relationships (user-organization associations)
INSERT INTO organization_members (org_id, user_id, role, access_code, joined_date)
VALUES 
-- Ujung Raya Primary School (org_id=1)
(1, 2, 'principal', NULL, '2024-01-15'),  -- Principal: khairunnisa (user_id=2)
(1, 3, 'admin', NULL, '2024-01-15'),      -- School Admin: ayu_lestari (user_id=3)
(1, 4, 'teacher', NULL, '2024-01-20'),    -- Teacher: bintang_akbar (user_id=4)
(1, 5, 'teacher', NULL, '2024-01-20'),    -- Teacher: maya_sari (user_id=5)
(1, 6, 'student', 'STU-2024-001', '2024-02-01'),  -- Student 1 (user_id=6)
(1, 7, 'student', 'STU-2024-002', '2024-02-01'),  -- Student 2 (user_id=7)
(1, 8, 'student', 'STU-2024-003', '2024-02-01'),  -- Student 3 (user_id=8)
(1, 9, 'student', 'STU-2024-004', '2024-02-01'),  -- Student 4 (user_id=9)
(1, 10, 'student', 'STU-2024-005', '2024-02-01'), -- Student 5 (user_id=10)
-- #SaveOurAnimals Community (org_id=2)
(2, 11, 'chairman', NULL, '2024-02-01'),   -- Chair: besoeki_rachmat (user_id=11)
(2, 12, 'member', NULL, '2024-02-05'),     -- Member 1 (user_id=12)
(2, 13, 'member', NULL, '2024-02-10'),     -- Member 2 (user_id=13)
(2, 14, 'member', NULL, '2024-02-15');     -- Member 3 (user_id=14)
-- Info: 13 organization members inserted


-- 4. Insert conservation program data
INSERT INTO programs (program_name, description, program_type)
VALUES 
-- Javan Rhinoceros Protection Program
('Javan Rhinoceros Protection', 
 'Conservation program for critically endangered Javan Rhinoceros in Ujung Kulon National Park',
 'regional'),
-- Sumatran Tiger Conservation Program
('Sumatran Tiger Conservation',
 'Protection and habitat preservation for Sumatran Tigers',
 'national'),
-- Bali Myna Recovery Program
('Bali Myna Recovery',
 'Breeding and release program for Bali Myna (Jalak Bali)',
 'regional'),
-- Indonesian Wildlife Education Program
('Indonesian Wildlife Education',
 'Educational program about Indonesian endangered species for schools',
 'national'),
-- Community Conservation Program
('Community-Based Conservation',
 'Engaging local communities in conservation efforts',
 'local');
-- Info: 5 conservation programs inserted


-- 5. Insert class data (linking school and teacher)
INSERT INTO classes (org_id, teacher_id, class_name, syllabus)
VALUES 
-- School 1 (org_id=1) + Teacher 4 (bintang_akbar): Conservation Biology Class A
(1, 4, 'Conservation Biology Class A', 
 'Introduction to conservation principles and endangered species'),
-- School 1 + Teacher 4: Javan Rhino Project
(1, 4, 'Javan Rhino Project',
 'Hands-on project focused on local Javan Rhinoceros conservation'),
-- School 1 + Teacher 5 (maya_sari): Wildlife Photography
(1, 5, 'Wildlife Photography',
 'Learning to document wildlife through photography');
-- Info: 3 classes inserted


-- 6. Insert class enrollment data (student enrollments)
INSERT INTO class_enrollments (class_id, student_id, enrollment_date, status)
VALUES 
-- Conservation Biology Class A (class_id=1)
(1, 6, '2024-02-01', 'active'),  -- Student 1 (user_id=6)
(1, 7, '2024-02-01', 'active'),  -- Student 2 (user_id=7)
(1, 8, '2024-02-01', 'active'),  -- Student 3 (user_id=8)
-- Javan Rhino Project (class_id=2)
(2, 6, '2024-02-05', 'active'),  -- Student 1
(2, 7, '2024-02-05', 'active'),  -- Student 2
(2, 9, '2024-02-05', 'active'),  -- Student 4 (user_id=9)
(2, 10, '2024-02-05', 'active'), -- Student 5 (user_id=10)
-- Wildlife Photography (class_id=3)
(3, 8, '2024-02-10', 'active'),  -- Student 3
(3, 9, '2024-02-10', 'active'),  -- Student 4
(3, 10, '2024-02-10', 'active'); -- Student 5
-- Info: 10 class enrollments inserted


-- 7. Insert program enrollment data (organization/individual program registration)
INSERT INTO program_enrollments (program_id, user_id, org_id, enrollment_date, status)
VALUES 
-- School 1 (org_id=1) enrolls in programs 1, 4
(1, NULL, 1, '2024-02-01', 'active'),  -- Javan Rhino Protection (program_id=1)
(4, NULL, 1, '2024-02-01', 'active'),  -- Wildlife Education (program_id=4)
-- Community 2 (org_id=2) enrolls in programs 5, 2
(5, NULL, 2, '2024-02-01', 'active'),  -- Community Conservation (program_id=5)
(2, NULL, 2, '2024-02-01', 'active'),  -- Sumatran Tiger Protection (program_id=2)
-- Individual: Member 1 (user_id=12) enrolls in program 1, Member 2 (user_id=13) in program 2
(1, 12, NULL, '2024-02-05', 'active'),
(2, 13, NULL, '2024-02-10', 'active');
-- Info: 6 program enrollments inserted


-- 8. Insert activity data (linking program/class)
INSERT INTO activities (program_id, class_id, activity_name, activity_type, description, created_by)
VALUES 
-- Program 1 (Javan Rhino) + Class 1: Rhino Habitat Study (created by Teacher 4)
(1, 1, 'Rhino Habitat Study', 'in-class', 
 'Study the habitat requirements of Javan Rhinoceros', 4),
-- Program 1 + Class 2: Field Trip to Ujung Kulon (created by Teacher 4)
(1, 2, 'Field Trip to Ujung Kulon', 'outdoor',
 'Visit Ujung Kulon National Park to observe rhino habitat', 4),
-- Program 4 (Wildlife Education) + No Class: Species Identification Challenge (created by Admin 1)
(4, NULL, 'Species Identification Challenge', 'challenge',
 'Learn to identify Indonesian endangered species', 1),
-- Program 4 + Class 3: Wildlife Photography Assignment (created by Teacher 5)
(4, 3, 'Wildlife Photography Assignment', 'assessment',
 'Take photos of local wildlife and create a portfolio', 5);
-- Info: 4 activities inserted


-- 9. Insert user profile data (extended user info)
INSERT INTO user_profiles (user_id, avatar_path, color_scheme, bio, is_public)
VALUES 
-- Students 1-5 (user_id=6-10): profiles not public
(6, '/avatars/student1.png', 'blue', 'I love rhinos!', FALSE),
(7, '/avatars/student2.png', 'green', 'Future conservationist', FALSE),
(8, '/avatars/student3.png', 'orange', 'Wildlife photographer', FALSE),
(9, '/avatars/student4.png', 'purple', 'Nature lover', FALSE),
(10, '/avatars/student5.png', 'red', 'Animal friend', FALSE),
-- Community Members 11-14 (user_id=11-14): profiles public
(11, '/avatars/besoeki.png', 'brown', 
 'Chairman of #SaveOurAnimals, passionate about wildlife conservation', TRUE),
(12, '/avatars/member1.png', 'teal',
 'Wildlife photographer and conservationist', TRUE),
(13, '/avatars/member2.png', 'olive',
 'Environmental educator', TRUE),
(14, '/avatars/member3.png', 'navy',
 'Field researcher', TRUE),
-- Teachers 4-5 (user_id=4-5): profiles public
(4, '/avatars/bintang.png', 'gray',
 'Teacher at Ujung Raya Primary School', TRUE),
(5, '/avatars/maya.png', 'pink',
 'Wildlife photography instructor', TRUE);
-- Info: 11 user profiles inserted


-- 10. Insert content library data (articles/reports/educational materials)
INSERT INTO content_library (title, content_type, content_data, created_by, org_id, is_public)
VALUES 
-- Student 1 (user_id=6): Rhino essay (school 1, public)
('My First Rhino Sighting', 'essay', 
 'Today I saw a Javan Rhinoceros for the first time...', 
 6, 1, TRUE),
-- Student 2 (user_id=7): Conservation report (school 1, public)
('Conservation Report', 'report',
 'Research on Javan Rhino population trends', 
 7, 1, TRUE),
-- Community Member 12 (user_id=12): Sumatran Tiger article (community 2, public)
('Protecting Sumatran Tigers', 'article',
 'Comprehensive guide to Sumatran Tiger conservation...', 
 12, 2, TRUE),
-- Community Member 13 (user_id=13): Photography tips (community 2, public)
('Wildlife Photography Tips', 'article',
 'Best practices for photographing endangered species...', 
 13, 2, TRUE),
-- Admin 1 (user_id=1): Indonesian Endangered Species Guide (no org, public)
('Indonesian Endangered Species Guide', 'educational_material',
 'Complete guide to all endangered endemic species in Indonesia...',
 1, NULL, TRUE);
-- Info: 5 content library items inserted


-- 11. Insert species sighting records
INSERT INTO species_sightings (species_name, location, date_time, description, photo_path, reported_by, verified)
VALUES 
-- Student 1 (user_id=6): Javan Rhino (verified)
('Javan Rhinoceros', 'Ujung Kulon National Park, Sector A',
 '2024-03-15 08:30:00', 
 'Observed adult rhino near water source, appeared healthy',
 '/photos/rhino_sighting_001.jpg', 6, TRUE),
-- Community Member 12 (user_id=12): Bali Myna (verified)
('Bali Myna', 'Bali Barat National Park',
 '2024-03-10 14:15:00',
 'Pair of Bali Mynas spotted in nesting area',
 '/photos/myna_sighting_001.jpg', 12, TRUE),
-- Community Member 13 (user_id=13): Sumatran Tiger (not verified)
('Sumatran Tiger', 'Leuser Ecosystem',
 '2024-02-28 06:45:00',
 'Tiger tracks and signs observed during patrol',
 NULL, 13, FALSE);
-- Info: 3 species sighting records inserted


-- 12. Insert submission data
INSERT INTO submissions (activity_id, student_id, submission_data, submission_file_path, status)
VALUES 
-- Activity 1 (Rhino Habitat Study) + Student 1: report submitted (submitted)
(1, 6, 'Rhinos need large territories with water sources...', 
 '/submissions/student1_habitat.pdf', 'submitted'),
-- Activity 1 + Student 2: report submitted (graded)
(1, 7, 'The ideal habitat for Javan Rhino includes...', 
 '/submissions/student2_habitat.pdf', 'graded'),
-- Activity 4 (Photography Assignment) + Student 3: portfolio submitted (submitted)
(4, 8, 'My wildlife photography portfolio...',
 '/submissions/student3_photos.zip', 'submitted');
-- Info: 3 submissions inserted


-- 13. Insert assessment data (teacher grades)
INSERT INTO assessments (submission_id, teacher_id, grade, feedback)
VALUES 
-- Submission 2 (Student 2's report) + Teacher 4: grade A
(2, 4, 'A', 'Excellent work! Your analysis of rhino habitat is thorough.');
-- Info: 1 assessment inserted


-- 14. Insert messages (user private messages)
INSERT INTO messages (sender_id, recipient_id, message_text)
VALUES 
-- Teacher 4 → Student 6: praise + reminder
(4, 6, 'Great job on your habitat study! Please prepare for our field trip.'),
-- Student 6 → Teacher 4: thanks
(6, 4, 'Thank you teacher! I am very excited about the field trip.'),
-- Teacher 5 → Student 8: encouragement
(5, 8, 'Your photography skills are improving. Keep practicing!');
-- Info: 3 messages inserted


-- 15. Insert note data (teacher notes)
INSERT INTO notes (teacher_id, target_type, target_id, note_text)
VALUES 
-- Teacher 4: note on submission 1 (submission_id=1)
(4, 'submission', 1, 'Consider adding more details about water requirements.'),
-- Teacher 4: note on sighting 1 (sighting_id=1)
(4, 'sighting', 1, 'Excellent observation! Well documented.');
-- Info: 2 notes inserted


-- 16. Insert creative canvas data (JSON assets)
INSERT INTO creative_canvas (user_id, program_id, assets)
VALUES 
-- Student 6 (user_id=6) + Program 1: achievements + photos + essays
(6, 1, '{"achievements": ["First Rhino Sighting", "Habitat Study Completed"], "photos": ["/canvas/student1_photo1.jpg", "/canvas/student1_photo2.jpg"], "essays": ["My First Rhino Sighting"]}'),
-- Student 8 (user_id=8) + Program 4: achievements + photos + portfolio
(8, 4, '{"achievements": ["Wildlife Photographer Badge"], "photos": ["/canvas/student3_photo1.jpg"], "portfolio": "Wildlife Photography Portfolio"}');
-- Info: 2 creative canvas records inserted


-- 17. Insert business analytics data (statistics)
INSERT INTO business_analytics (metric_type, metric_value, metric_data)
VALUES 
-- Total subscriptions: 3 (2 schools + 1 community)
('total_subscriptions', 3, '{"schools": 2, "communities": 1}'),
-- Active users: 16 (all users)
('active_users', 16, '{"breakdown": "by_type"}'),
-- Popular program: program 1 (Javan Rhinoceros Protection)
('popular_program', 1, '{"name": "Javan Rhinoceros Protection"}');
-- Info: 3 business analytics records inserted


-- Commit all insert operations
COMMIT;
SELECT 'All initial data (92 records) inserted successfully!' AS result;
