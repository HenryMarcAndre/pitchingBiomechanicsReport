SELECT 
  SUBSTRING_INDEX(metric_name, '_at', 1) as metric_name, 
  CASE 
    WHEN metric_name LIKE '%at_sit' THEN 'Sit AVG'
    WHEN metric_name LIKE '%at_footplant' THEN 'FP AVG'
    WHEN metric_name LIKE '%at_release' THEN 'BR AVG'
    WHEN metric_name LIKE 'stride_%' THEN 'AVG'
    WHEN metric_name LIKE 'release_time' THEN 'AVG'
  END as position, 
  AVG(value) as value
FROM (
  SELECT 
    metric_name, 
    value
  FROM pitches
  WHERE value IS NOT NULL
) t
GROUP BY metric_name, position

UNION

SELECT 
  SUBSTRING_INDEX(metric_name, '_at', 1) as metric_name, 
  CASE 
    WHEN metric_name LIKE '%at_sit' THEN 'Sit STD'
    WHEN metric_name LIKE '%at_footplant' THEN 'FP STD'
    WHEN metric_name LIKE '%at_release' THEN 'BR STD'
    WHEN metric_name LIKE 'stride_%' THEN 'STD'
    WHEN metric_name LIKE 'release_time' THEN 'STD'
  END as position_std, 
  STD(value) as stdev_value
FROM (
  SELECT 
    metric_name, 
    value
  FROM pitches
  WHERE value IS NOT NULL
) t
GROUP BY metric_name, position_std;
