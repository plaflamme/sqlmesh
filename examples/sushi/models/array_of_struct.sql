model(
  name sushi.array_of_struct,
  kind FULL,
  dialect 'bigquery'
);
SELECT '2024-01-01'::DATE AS event_date, ARRAY(STRUCT('a' AS a)) AS my_structs
