# Queries for exploring the sociodemograhic features of the respondents

QUERY_AGE = """

SELECT SurveyID,
       CASE
            WHEN CAST(TRIM(AnswerText) AS INTEGER) BETWEEN 18 AND 24 THEN '18-24'
            WHEN CAST(TRIM(AnswerText) AS INTEGER) BETWEEN 25 AND 34 THEN '25-34'
            WHEN CAST(TRIM(AnswerText) AS INTEGER) BETWEEN 35 AND 44 THEN '35-44'
            WHEN CAST(TRIM(AnswerText) AS INTEGER) BETWEEN 45 AND 54 THEN '45-54'
            WHEN CAST(TRIM(AnswerText) AS INTEGER) BETWEEN 55 AND 64 THEN '55-64'
            WHEN CAST(TRIM(AnswerText) AS INTEGER) BETWEEN 65 AND 99 THEN 'Over 65'
        END AS age_group,
    COUNT(*) AS count
FROM Answer
WHERE SurveyID IN (2014, 2016, 2017, 2018, 2019)
      AND QuestionID=1
      AND AnswerText > 18
      AND age_group IS NOT NULL
GROUP BY SurveyID, age_group
ORDER BY SurveyID, age_group;
"""

QUERY_GENDER = """

SELECT CASE
            WHEN UPPER(TRIM(a.AnswerText)) LIKE '%MALE%' AND UPPER(TRIM(a.AnswerText)) NOT LIKE '%FEMALE%' THEN 'Male'
            WHEN UPPER(TRIM(a.AnswerText)) LIKE '%FEMALE%' THEN 'Female'
            WHEN UPPER(TRIM(a.AnswerText)) IN ('NONBINARY', 'NON-BINARY', 'GENDERQUEER', 'AGENDER') THEN 'Non-Binary'
            ELSE 'Other'
        END AS gender,
    COUNT(*) AS count
FROM Answer AS a
WHERE a.QuestionID=2
      AND a.AnswerText IS NOT NULL
      AND UPPER(TRIM(a.AnswerText)) NOT IN ('NONE')

GROUP BY gender
ORDER BY count DESC;
"""

QUERY_COUNTRY = """

WITH country_counts AS (
    SELECT CASE 
                WHEN UPPER(TRIM(a.AnswerText)) IN ('UNITED STATES OF AMERICA', 'UNITED STATES', 'USA') THEN 'USA'
                WHEN a.AnswerText = 'Bahamas, The' THEN 'Bahamas'
                ELSE a.AnswerText 
            END AS country,
           COUNT(*) AS count
    FROM Answer AS a
    WHERE a.QuestionID = 3
      AND a.AnswerText IS NOT NULL
    GROUP BY country
)
SELECT 
    CASE 
        WHEN count > 5 THEN country
        ELSE 'Other'
    END AS country,
    SUM(count) AS count
FROM country_counts
GROUP BY 
    CASE 
        WHEN count > 5 THEN country
        ELSE 'Other'
    END
ORDER BY count DESC;
"""

QUERY_RACE = """

SELECT
    CASE
    WHEN AnswerText IN ('White', 'European American', 'Caucasian') THEN 'White'
    WHEN AnswerText IN ('White Hispanic', 'Hispanic') THEN 'Hispanic'
    WHEN AnswerText IN ('More than one of the above') THEN 'Multiracial'
    WHEN AnswerText IN ('Black or African American') THEN 'Black or African American'
    WHEN AnswerText IN ('Asian') THEN 'Asian'
    ELSE 'Other'
  END AS race,
COUNT(*) as count
FROM Answer a 
WHERE QuestionID = 89 
GROUP BY race
ORDER BY COUNT(*) DESC;
"""