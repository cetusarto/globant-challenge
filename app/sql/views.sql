
/*
Number of employees hired for each job and department in 2021 divided by quarter. The
table must be ordered alphabetically by department and job.
*/
CREATE OR REPLACE VIEW job_department_view AS (
WITH distinct_quarter as (
  SELECT
    extract(quarter from datetime::timestamp::date) as quarter, 
    e.job_id,
    e.department_id,
    j.job,
    d.department,
    count(*) as count
  FROM employees e LEFT JOIN jobs j ON e.job_id = j.id LEFT JOIN departments d ON e.department_id = d.id
  WHERE e.job_id IS NOT NULL AND e.department_id IS NOT NULL AND e.datetime IS NOT NULL
  AND extract(YEAR from datetime::timestamp::date) = 2021
  GROUP BY e.job_id, e.department_id, quarter, job, department
)
  
SELECT
    department,
    job,
    SUM(CASE WHEN quarter = 1 THEN count ELSE 0 END) AS Q1,
    SUM(CASE WHEN quarter = 2 THEN count ELSE 0 END) AS Q2,
    SUM(CASE WHEN quarter = 3 THEN count ELSE 0 END) AS Q3,
    SUM(CASE WHEN quarter = 4 THEN count ELSE 0 END) AS Q4
FROM distinct_quarter
GROUP BY department,job
ORDER BY department,job);


/*
List of ids, name and number of employees hired of each department that hired more
employees than the mean of employees hired in 2021 for all the departments, ordered
by the number of employees hired (descending).
*/
CREATE OR REPLACE VIEW department_view AS (
  WITH departments_hires as (
    SELECT 
      e.department_id as id,
      d.department,
      count(*) as hired
    FROM employees e LEFT JOIN departments d ON e.department_id = d.id
    WHERE e.department_id IS NOT NULL AND e.datetime IS NOT NULL
    AND extract(YEAR from datetime::timestamp::date) = 2021
    GROUP BY e.department_id, d.department
  )
  SELECT * FROM departments_hires WHERE hired > (SELECT AVG(hired) from departments_hires)
);