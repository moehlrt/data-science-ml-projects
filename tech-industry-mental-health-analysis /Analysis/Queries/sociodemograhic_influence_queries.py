# Sociodemographic influence on self reported and diagnosed mental diseases.

# Gender

QUERY_GENDER_SELF = """

WITH total AS (
    SELECT 
        SurveyID,
        SUM(UPPER(TRIM(AnswerText)) = 'MALE') AS total_male,
        SUM(UPPER(TRIM(AnswerText)) = 'FEMALE') AS total_female
    FROM Answer
    WHERE QuestionID = 2
    GROUP BY SurveyID
),
yes_counts AS (
    SELECT 
        g.SurveyID,
        SUM(UPPER(TRIM(g.AnswerText)) = 'MALE') AS male_count,
        SUM(UPPER(TRIM(g.AnswerText)) = 'FEMALE') AS female_count
    FROM Answer AS g
    JOIN Answer AS d
      ON g.UserID = d.UserID
     AND g.SurveyID = d.SurveyID
    WHERE g.QuestionID = 2
      AND d.QuestionID = 33
      AND TRIM(d.AnswerText) = 'Yes'
    GROUP BY g.SurveyID
),
base AS (
    SELECT 
        y.SurveyID AS survey_year,
        y.male_count,
        y.female_count,
        t.total_male,
        t.total_female
    FROM yes_counts y
    JOIN total t ON y.SurveyID = t.SurveyID
)
SELECT 
    survey_year,
    'Male'   AS gender,
    male_count   AS count,
    total_male   AS total,
    ROUND(100.0 * male_count / NULLIF(total_male, 0), 2)   AS percent
FROM base
UNION ALL
SELECT 
    survey_year,
    'Female' AS gender,
    female_count AS count,
    total_female AS total,
    ROUND(100.0 * female_count / NULLIF(total_female, 0), 2) AS percent
FROM base
ORDER BY survey_year, gender;
"""

QUERY_GENDER_DIAG = """

WITH total AS (
    SELECT 
        SurveyID,
        SUM(UPPER(TRIM(AnswerText)) = 'MALE') AS total_male,
        SUM(UPPER(TRIM(AnswerText)) = 'FEMALE') AS total_female
    FROM Answer
    WHERE QuestionID = 2
    GROUP BY SurveyID
),
yes_counts AS (
    SELECT 
        g.SurveyID,
        SUM(UPPER(TRIM(g.AnswerText)) = 'MALE') AS male_count,
        SUM(UPPER(TRIM(g.AnswerText)) = 'FEMALE') AS female_count
    FROM Answer AS g
    JOIN Answer AS d
      ON g.UserID = d.UserID
     AND g.SurveyID = d.SurveyID
    WHERE g.QuestionID = 2
      AND d.QuestionID = 34
      AND TRIM(d.AnswerText) = 'Yes'
    GROUP BY g.SurveyID
),
base AS (
    SELECT 
        y.SurveyID AS survey_year,
        y.male_count,
        y.female_count,
        t.total_male,
        t.total_female
    FROM yes_counts y
    JOIN total t ON y.SurveyID = t.SurveyID
)
SELECT 
    survey_year,
    'Male'   AS gender,
    male_count   AS count,
    total_male   AS total,
    ROUND(100.0 * male_count / NULLIF(total_male, 0), 2)   AS percent
FROM base
UNION ALL
SELECT 
    survey_year,
    'Female' AS gender,
    female_count AS count,
    total_female AS total,
    ROUND(100.0 * female_count / NULLIF(total_female, 0), 2) AS percent
FROM base
ORDER BY survey_year, gender;
"""

# Age

QUERY_AGE_SELF = """

WITH ages AS (
    SELECT
        SurveyID,
        UserID,
        CASE
            WHEN CAST(TRIM(AnswerText) AS INTEGER) BETWEEN 18 AND 24 THEN '18-24'
            WHEN CAST(TRIM(AnswerText) AS INTEGER) BETWEEN 25 AND 34 THEN '25-34'
            WHEN CAST(TRIM(AnswerText) AS INTEGER) BETWEEN 35 AND 44 THEN '35-44'
            WHEN CAST(TRIM(AnswerText) AS INTEGER) BETWEEN 45 AND 54 THEN '45-54'
            WHEN CAST(TRIM(AnswerText) AS INTEGER) BETWEEN 55 AND 64 THEN '55-64'
            ELSE '65+'
        END AS age_group
    FROM Answer
    WHERE QuestionID = 1
      AND TRIM(AnswerText) GLOB '[0-9]*'
      AND CAST(TRIM(AnswerText) AS INTEGER) >= 18
      AND SurveyID IN (2016, 2017, 2018, 2019)
),
totals AS (
    SELECT SurveyID, age_group, COUNT(*) AS total
    FROM ages
    GROUP BY SurveyID, age_group
),
yes_counts AS (
    SELECT a.SurveyID, a.age_group, COUNT(*) AS diagnosed_count
    FROM ages a
    JOIN Answer d
      ON d.SurveyID = a.SurveyID AND d.UserID = a.UserID
    WHERE d.QuestionID = 33
      AND TRIM(d.AnswerText) = 'Yes'
    GROUP BY a.SurveyID, a.age_group
)
SELECT
    t.SurveyID AS survey_year,
    t.age_group,
    COALESCE(y.diagnosed_count, 0) AS count,
    t.total,
    ROUND(100.0 * COALESCE(y.diagnosed_count, 0) / NULLIF(t.total, 0), 2) AS percent
FROM totals t
LEFT JOIN yes_counts y
  ON y.SurveyID = t.SurveyID AND y.age_group = t.age_group
ORDER BY survey_year,
         CASE t.age_group
            WHEN '18-24' THEN 1
            WHEN '25-34' THEN 2
            WHEN '35-44' THEN 3
            WHEN '45-54' THEN 4
            WHEN '55-64' THEN 5
            ELSE 6
         END;
"""

QUERY_AGE_DIAG = """

WITH ages AS (
    SELECT
        SurveyID,
        UserID,
        CASE
            WHEN CAST(TRIM(AnswerText) AS INTEGER) BETWEEN 18 AND 24 THEN '18-24'
            WHEN CAST(TRIM(AnswerText) AS INTEGER) BETWEEN 25 AND 34 THEN '25-34'
            WHEN CAST(TRIM(AnswerText) AS INTEGER) BETWEEN 35 AND 44 THEN '35-44'
            WHEN CAST(TRIM(AnswerText) AS INTEGER) BETWEEN 45 AND 54 THEN '45-54'
            WHEN CAST(TRIM(AnswerText) AS INTEGER) BETWEEN 55 AND 64 THEN '55-64'
            ELSE '65+'
        END AS age_group
    FROM Answer
    WHERE QuestionID = 1
      AND TRIM(AnswerText) GLOB '[0-9]*'
      AND CAST(TRIM(AnswerText) AS INTEGER) >= 18
      AND SurveyID IN (2016, 2017, 2018, 2019)
),
totals AS (
    SELECT SurveyID, age_group, COUNT(*) AS total
    FROM ages
    GROUP BY SurveyID, age_group
),
yes_counts AS (
    SELECT a.SurveyID, a.age_group, COUNT(*) AS diagnosed_count
    FROM ages a
    JOIN Answer d
      ON d.SurveyID = a.SurveyID AND d.UserID = a.UserID
    WHERE d.QuestionID = 34
      AND TRIM(d.AnswerText) = 'Yes'
    GROUP BY a.SurveyID, a.age_group
)
SELECT
    t.SurveyID AS survey_year,
    t.age_group,
    COALESCE(y.diagnosed_count, 0) AS count,
    t.total,
    ROUND(100.0 * COALESCE(y.diagnosed_count, 0) / NULLIF(t.total, 0), 2) AS percent
FROM totals t
LEFT JOIN yes_counts y
  ON y.SurveyID = t.SurveyID AND y.age_group = t.age_group
ORDER BY survey_year,
         CASE t.age_group
            WHEN '18-24' THEN 1
            WHEN '25-34' THEN 2
            WHEN '35-44' THEN 3
            WHEN '45-54' THEN 4
            WHEN '55-64' THEN 5
            ELSE 6
         END;
"""

# Family Background - for reported ones

QUERY_FAM_SELF = """

SELECT family_history,
       100.0 * COUNT(family_history) / SUM(COUNT(family_history)) OVER () AS percentage
FROM (
    SELECT SurveyID AS survey_year,
            MAX(CASE WHEN (QuestionID == 33 AND AnswerText == 'Yes') THEN 1 END) AS mental_health,
            MAX(CASE WHEN (QuestionID == 6) THEN AnswerText END) AS family_history

    FROM Answer
    WHERE QuestionID IN (6, 33) AND survey_year != 2014
    GROUP BY survey_year, UserID
    HAVING mental_health IS NOT NULL
)
GROUP BY family_history

"""

QUERY_FAM_DIAG = """

SELECT family_history,
       100.0 * COUNT(family_history) / SUM(COUNT(family_history)) OVER () AS percentage
FROM (
    SELECT SurveyID AS survey_year,
            MAX(CASE WHEN (QuestionID == 34 AND AnswerText == 'Yes') THEN 1 END) AS mental_health,
            MAX(CASE WHEN (QuestionID == 6) THEN AnswerText END) AS family_history

    FROM Answer
    WHERE QuestionID IN (6, 34) AND survey_year != 2014
    GROUP BY survey_year, UserID
    HAVING mental_health IS NOT NULL
)
GROUP BY family_history

"""

# Family Background - for non reported ones

QUERY_FAM_NON_SELF = """

SELECT family_history,
       100.0 * COUNT(family_history) / SUM(COUNT(family_history)) OVER () AS percentage
FROM (
    SELECT SurveyID AS survey_year,
            MAX(CASE WHEN (QuestionID == 33 AND AnswerText == 'No') THEN 1 END) AS mental_health,
            MAX(CASE WHEN (QuestionID == 6) THEN AnswerText END) AS family_history

    FROM Answer
    WHERE QuestionID IN (6, 33) AND survey_year != 2014
    GROUP BY survey_year, UserID
    HAVING mental_health IS NOT NULL
)
GROUP BY family_history

"""

QUERY_FAM_NON_DIAG = """

SELECT family_history,
       100.0 * COUNT(family_history) / SUM(COUNT(family_history)) OVER () AS percentage
FROM (
    SELECT SurveyID AS survey_year,
            MAX(CASE WHEN (QuestionID == 34 AND AnswerText == 'No') THEN 1 END) AS mental_health,
            MAX(CASE WHEN (QuestionID == 6) THEN AnswerText END) AS family_history

    FROM Answer
    WHERE QuestionID IN (6, 34) AND survey_year != 2014
    GROUP BY survey_year, UserID
    HAVING mental_health IS NOT NULL
)
GROUP BY family_history

"""