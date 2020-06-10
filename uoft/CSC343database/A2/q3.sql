SET search_path TO artistdb;

SELECT DISTINCT rl.label_name AS record_label, a.year AS year, a.sales AS total_sales
FROM Album a, RecordLabel rl, ProducedBy pb
WHERE a.album_id = pb.album_id
      AND rl.label_id = pb.label_id
ORDER BY rl.label_name ASC, a.year ASC; 