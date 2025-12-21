# Workplace Influence on self reported and diagnosed mental diseases.

# Access to mental health resources at current company

QUERY_RES_SELF = """

WITH total AS (
    SELECT 
        SurveyID,
        SUM(UPPER(TRIM(AnswerText)) = 'YES') AS total_yes,
        SUM(UPPER(TRIM(AnswerText)) = 'NO') AS total_no,
        SUM(UPPER(TRIM(AnswerText)) = 'I DON''T KNOW') AS total_dont_know
    FROM Answer
    WHERE QuestionID = 16
    GROUP BY SurveyID
),
yes_counts AS (
    SELECT 
        g.SurveyID,
        SUM(UPPER(TRIM(g.AnswerText)) = 'YES') AS yes_count,
        SUM(UPPER(TRIM(g.AnswerText)) = 'NO') AS no_count,
        SUM(UPPER(TRIM(g.AnswerText)) = 'I DON''T KNOW') AS dont_know_count
    FROM Answer AS g
    JOIN Answer AS d
      ON g.UserID = d.UserID
     AND g.SurveyID = d.SurveyID
    WHERE g.QuestionID = 16
      AND d.QuestionID = 33
      AND TRIM(d.AnswerText) = 'Yes'
    GROUP BY g.SurveyID
),
base AS (
    SELECT 
        y.SurveyID AS survey_year,
        y.yes_count,
        y.no_count,
        y.dont_know_count,
        t.total_yes,
        t.total_no,
        t.total_dont_know
    FROM yes_counts y
    JOIN total t ON y.SurveyID = t.SurveyID
)
SELECT 
    survey_year,
    'YES' AS access,
    yes_count   AS count,
    total_yes  AS total,
    ROUND(100.0 * yes_count / NULLIF(total_yes, 0), 2)   AS percent
FROM base
UNION ALL
SELECT 
    survey_year,
    'NO' AS access,
    no_count AS count,
    total_no AS total,
    ROUND(100.0 * no_count / NULLIF(total_no, 0), 2) AS percent
FROM base
UNION ALL 
SELECT
    survey_year,
    'DONT KNOW' AS access,
    dont_know_count AS count,
    total_dont_know AS total,
    ROUND(100.0 * dont_know_count / NULLIF(total_dont_know, 0), 2) AS percent
FROM base
ORDER BY survey_year, access;
"""

QUERY_RES_DIAG = """

WITH total AS (
    SELECT 
        SurveyID,
        SUM(UPPER(TRIM(AnswerText)) = 'YES') AS total_yes,
        SUM(UPPER(TRIM(AnswerText)) = 'NO') AS total_no,
        SUM(UPPER(TRIM(AnswerText)) = 'I DON''T KNOW') AS total_dont_know
    FROM Answer
    WHERE QuestionID = 16
    GROUP BY SurveyID
),
yes_counts AS (
    SELECT 
        g.SurveyID,
        SUM(UPPER(TRIM(g.AnswerText)) = 'YES') AS yes_count,
        SUM(UPPER(TRIM(g.AnswerText)) = 'NO') AS no_count,
        SUM(UPPER(TRIM(g.AnswerText)) = 'I DON''T KNOW') AS dont_know_count
    FROM Answer AS g
    JOIN Answer AS d
      ON g.UserID = d.UserID
     AND g.SurveyID = d.SurveyID
    WHERE g.QuestionID = 16
      AND d.QuestionID = 34
      AND TRIM(d.AnswerText) = 'Yes'
    GROUP BY g.SurveyID
),
base AS (
    SELECT 
        y.SurveyID AS survey_year,
        y.yes_count,
        y.no_count,
        y.dont_know_count,
        t.total_yes,
        t.total_no,
        t.total_dont_know
    FROM yes_counts y
    JOIN total t ON y.SurveyID = t.SurveyID
)
SELECT 
    survey_year,
    'YES' AS access,
    yes_count   AS count,
    total_yes  AS total,
    ROUND(100.0 * yes_count / NULLIF(total_yes, 0), 2)   AS percent
FROM base
UNION ALL
SELECT 
    survey_year,
    'NO' AS access,
    no_count AS count,
    total_no AS total,
    ROUND(100.0 * no_count / NULLIF(total_no, 0), 2) AS percent
FROM base
UNION ALL 
SELECT
    survey_year,
    'DONT KNOW' AS access,
    dont_know_count AS count,
    total_dont_know AS total,
    ROUND(100.0 * dont_know_count / NULLIF(total_dont_know, 0), 2) AS percent
FROM base
ORDER BY survey_year, access;
"""

# Remote vs. Office

QUERY_PLC_SELF = """

WITH total_100 AS (
    SELECT 
        SurveyID,
        SUM(UPPER(TRIM(AnswerText)) = 'ALWAYS') AS total_100_always,
        SUM(UPPER(TRIM(AnswerText)) = 'NEVER') AS total_100_never,
        SUM(UPPER(TRIM(AnswerText)) = 'SOMETIMES') AS total_100_sometimes
    FROM Answer
    WHERE QuestionID = 118
    GROUP BY SurveyID
),
counts_100 AS (
    SELECT 
        g.SurveyID,
        SUM(UPPER(TRIM(g.AnswerText)) = 'ALWAYS') AS always_100_count,
        SUM(UPPER(TRIM(g.AnswerText)) = 'NEVER') AS never_100_count,
        SUM(UPPER(TRIM(g.AnswerText)) = 'SOMETIMES') AS sometimes_100_count
    FROM Answer AS g
    JOIN Answer AS d
      ON g.UserID = d.UserID
     AND g.SurveyID = d.SurveyID
    WHERE g.QuestionID = 118
      AND d.QuestionID = 33
      AND TRIM(d.AnswerText) = 'Yes'
    GROUP BY g.SurveyID
),
base_100 AS (
    SELECT 
        c.SurveyID AS survey_year,
        c.always_100_count,
        c.never_100_count,
        c.sometimes_100_count,
        t.total_100_always,
        t.total_100_never,
        t.total_100_sometimes
    FROM counts_100 AS c
    JOIN total_100 AS t ON c.SurveyID = t.SurveyID
)
SELECT 
    survey_year,
    'ALWAYS' AS remote_100,
    always_100_count AS count_100,
    total_100_always AS total_100,
    ROUND(100.0 * always_100_count / NULLIF(total_100_always, 0), 2) AS percent_100,
    ROUND(100.0 * ((always_100_count*1.0/NULLIF(total_100_always, 0)) - 1.96 * SQRT((always_100_count*1.0/NULLIF(total_100_always, 0))*(1 - (always_100_count*1.0/NULLIF(total_100_always, 0)))/NULLIF(total_100_always, 0))), 2) AS ci_lower_percent_100,
    ROUND(100.0 * ((always_100_count*1.0/NULLIF(total_100_always, 0)) + 1.96 * SQRT((always_100_count*1.0/NULLIF(total_100_always, 0))*(1 - (always_100_count*1.0/NULLIF(total_100_always, 0)))/NULLIF(total_100_always, 0))), 2) AS ci_upper_percent_100
FROM base_100
UNION ALL
SELECT 
    survey_year,
    'NEVER' AS remote_100,
    never_100_count AS count_100,
    total_100_never AS total_100,
    ROUND(100.0 * never_100_count / NULLIF(total_100_never, 0), 2) AS percent_100,
    ROUND(100.0 * ((never_100_count*1.0/NULLIF(total_100_never, 0)) - 1.96 * SQRT((never_100_count*1.0/NULLIF(total_100_never, 0))*(1 - (never_100_count*1.0/NULLIF(total_100_never, 0)))/NULLIF(total_100_never, 0))), 2) AS ci_lower_percent_100,
    ROUND(100.0 * ((never_100_count*1.0/NULLIF(total_100_never, 0)) + 1.96 * SQRT((never_100_count*1.0/NULLIF(total_100_never, 0))*(1 - (never_100_count*1.0/NULLIF(total_100_never, 0)))/NULLIF(total_100_never, 0))), 2) AS ci_upper_percent_100
FROM base_100
UNION ALL
SELECT 
    survey_year,
    'SOMETIMES' AS remote_100,
    sometimes_100_count AS count_100,
    total_100_sometimes AS total_100,
    ROUND(100.0 * sometimes_100_count / NULLIF(total_100_sometimes, 0), 2) AS percent_100,
    ROUND(100.0 * ((sometimes_100_count*1.0/NULLIF(total_100_sometimes, 0)) - 1.96 * SQRT((sometimes_100_count*1.0/NULLIF(total_100_sometimes, 0))*(1 - (sometimes_100_count*1.0/NULLIF(total_100_sometimes, 0)))/NULLIF(total_100_sometimes, 0))), 2) AS ci_lower_percent_100,
    ROUND(100.0 * ((sometimes_100_count*1.0/NULLIF(total_100_sometimes, 0)) + 1.96 * SQRT((sometimes_100_count*1.0/NULLIF(total_100_sometimes, 0))*(1 - (sometimes_100_count*1.0/NULLIF(total_100_sometimes, 0)))/NULLIF(total_100_sometimes, 0))), 2) AS ci_upper_percent_100
FROM base_100
ORDER BY survey_year, count_100;
"""

QUERY_PLC_DIAG = """

WITH total_100 AS (
    SELECT 
        SurveyID,
        SUM(UPPER(TRIM(AnswerText)) = 'ALWAYS') AS total_100_always,
        SUM(UPPER(TRIM(AnswerText)) = 'NEVER') AS total_100_never,
        SUM(UPPER(TRIM(AnswerText)) = 'SOMETIMES') AS total_100_sometimes
    FROM Answer
    WHERE QuestionID = 118
    GROUP BY SurveyID
),
counts_100 AS (
    SELECT 
        g.SurveyID,
        SUM(UPPER(TRIM(g.AnswerText)) = 'ALWAYS') AS always_100_count,
        SUM(UPPER(TRIM(g.AnswerText)) = 'NEVER') AS never_100_count,
        SUM(UPPER(TRIM(g.AnswerText)) = 'SOMETIMES') AS sometimes_100_count
    FROM Answer AS g
    JOIN Answer AS d
      ON g.UserID = d.UserID
     AND g.SurveyID = d.SurveyID
    WHERE g.QuestionID = 118
      AND d.QuestionID = 34
      AND TRIM(d.AnswerText) = 'Yes'
    GROUP BY g.SurveyID
),
base_100 AS (
    SELECT 
        c.SurveyID AS survey_year,
        c.always_100_count,
        c.never_100_count,
        c.sometimes_100_count,
        t.total_100_always,
        t.total_100_never,
        t.total_100_sometimes
    FROM counts_100 AS c
    JOIN total_100 AS t ON c.SurveyID = t.SurveyID
)
SELECT 
    survey_year,
    'ALWAYS' AS remote_100,
    always_100_count AS count_100,
    total_100_always AS total_100,
    ROUND(100.0 * always_100_count / NULLIF(total_100_always, 0), 2) AS percent_100,
    ROUND(100.0 * ((always_100_count*1.0/NULLIF(total_100_always, 0)) - 1.96 * SQRT((always_100_count*1.0/NULLIF(total_100_always, 0))*(1 - (always_100_count*1.0/NULLIF(total_100_always, 0)))/NULLIF(total_100_always, 0))), 2) AS ci_lower_percent_100,
    ROUND(100.0 * ((always_100_count*1.0/NULLIF(total_100_always, 0)) + 1.96 * SQRT((always_100_count*1.0/NULLIF(total_100_always, 0))*(1 - (always_100_count*1.0/NULLIF(total_100_always, 0)))/NULLIF(total_100_always, 0))), 2) AS ci_upper_percent_100
FROM base_100
UNION ALL
SELECT 
    survey_year,
    'NEVER' AS remote_100,
    never_100_count AS count_100,
    total_100_never AS total_100,
    ROUND(100.0 * never_100_count / NULLIF(total_100_never, 0), 2) AS percent_100,
    ROUND(100.0 * ((never_100_count*1.0/NULLIF(total_100_never, 0)) - 1.96 * SQRT((never_100_count*1.0/NULLIF(total_100_never, 0))*(1 - (never_100_count*1.0/NULLIF(total_100_never, 0)))/NULLIF(total_100_never, 0))), 2) AS ci_lower_percent_100,
    ROUND(100.0 * ((never_100_count*1.0/NULLIF(total_100_never, 0)) + 1.96 * SQRT((never_100_count*1.0/NULLIF(total_100_never, 0))*(1 - (never_100_count*1.0/NULLIF(total_100_never, 0)))/NULLIF(total_100_never, 0))), 2) AS ci_upper_percent_100
FROM base_100
UNION ALL
SELECT 
    survey_year,
    'SOMETIMES' AS remote_100,
    sometimes_100_count AS count_100,
    total_100_sometimes AS total_100,
    ROUND(100.0 * sometimes_100_count / NULLIF(total_100_sometimes, 0), 2) AS percent_100,
    ROUND(100.0 * ((sometimes_100_count*1.0/NULLIF(total_100_sometimes, 0)) - 1.96 * SQRT((sometimes_100_count*1.0/NULLIF(total_100_sometimes, 0))*(1 - (sometimes_100_count*1.0/NULLIF(total_100_sometimes, 0)))/NULLIF(total_100_sometimes, 0))), 2) AS ci_lower_percent_100,
    ROUND(100.0 * ((sometimes_100_count*1.0/NULLIF(total_100_sometimes, 0)) + 1.96 * SQRT((sometimes_100_count*1.0/NULLIF(total_100_sometimes, 0))*(1 - (sometimes_100_count*1.0/NULLIF(total_100_sometimes, 0)))/NULLIF(total_100_sometimes, 0))), 2) AS ci_upper_percent_100
FROM base_100
ORDER BY survey_year, count_100;
"""


