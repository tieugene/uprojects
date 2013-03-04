SET NAMES koi8r;
SET collation_connection = 'koi8r_general_ci';
SELECT DISTINCT Employer, Email, Contact FROM main WHERE (EmployerType = 1) ORDER BY Employer, Contact;