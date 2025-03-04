SELECT * 
FROM steps
WHERE run_id = (SELECT MAX(run_id) FROM steps)