SET FOREIGN_KEY_CHECKS = 0;

SELECT CONCAT('TRUNCATE TABLE `', table_name, '`;')
FROM information_schema.tables
WHERE table_schema = 'komodo';

SET FOREIGN_KEY_CHECKS = 1;
