----- chicago crime

SELECT
  DATE(date) AS date,
  COUNT( unique_key) AS crime_count,
FROM `bigquery-public-data.chicago_crime.crime`
GROUP BY date
ORDER BY date desc


----SANFRAN crime
select
  date(timestamp) as date,
--   category,
  count(unique_key) as incident
from `bigquery-public-data.san_francisco_sfpd_incidents.sfpd_incidents`
GROUP BY  1--,2
ORDER BY 1 DESC--, 2

--- london fire brigade data
select
    date_of_call,
    count(incident_number) as incidents
from `bigquery-public-data.london_fire_brigade.fire_brigade_service_calls` 
group by 1
order by 1

--consumer complain

select
  date_received,
--   issue,
  count( complaint_id) as complaints
from `bigquery-public-data.cfpb_complaints.complaint_database`
group by 1--,2
order by 1--,2