# Social Influence on self reported and diagnosed mental diseases.

QUERY_SOCIAL_SELF = """

WITH base AS (
    SELECT o.SurveyID AS survey_year,
           CASE UPPER(TRIM(o.AnswerText))
                WHEN 'VERY OPEN' THEN 'Very open'
                WHEN 'SOMEWHAT OPEN' THEN 'Somewhat open'
                WHEN 'NEUTRAL' THEN 'Neutral'
                WHEN 'SOMEWHAT NOT OPEN' THEN 'Somewhat not open'
                WHEN 'NOT OPEN AT ALL' THEN 'Not open at all'
                WHEN 'NOT APPLICABLE TO ME (I DO NOT HAVE A MENTAL ILLNESS)' THEN 'Not applicable'
                ELSE 'Other'
           END AS openness,
           CASE WHEN UPPER(TRIM(s.AnswerText)) = 'YES' THEN 'Yes' ELSE 'No' END AS self_report
    FROM Answer o
    JOIN Answer s ON o.SurveyID = s.SurveyID AND o.UserID = s.UserID
    WHERE o.QuestionID = 30 AND s.QuestionID = 33
),
filtered AS (
    SELECT * FROM base WHERE openness NOT IN ('Not applicable', 'Other')
),
totals AS (
    SELECT survey_year,
           COUNT(*) AS n,
           SUM(self_report = 'Yes') AS col_yes,
           SUM(self_report = 'No')  AS col_no
    FROM filtered
    GROUP BY survey_year
),
row_totals AS (
    SELECT survey_year, openness,
           COUNT(*) AS row_n,
           SUM(self_report = 'Yes') AS obs_yes,
           SUM(self_report = 'No')  AS obs_no
    FROM filtered
    GROUP BY survey_year, openness
),
expected AS (
    SELECT r.survey_year, r.openness,
           r.obs_yes, r.obs_no, r.row_n,
           t.n, t.col_yes, t.col_no,
           (1.0 * r.row_n * t.col_yes) / t.n AS exp_yes,
           (1.0 * r.row_n * t.col_no) / t.n AS exp_no
    FROM row_totals r
    JOIN totals t ON r.survey_year = t.survey_year
),
chi_terms AS (
    SELECT survey_year, openness,
           CASE WHEN exp_yes > 0 THEN ((obs_yes - exp_yes)*(obs_yes - exp_yes))/exp_yes ELSE 0 END AS term_yes,
           CASE WHEN exp_no  > 0 THEN ((obs_no  - exp_no )*(obs_no  - exp_no ))/exp_no  ELSE 0 END AS term_no
    FROM expected
)
SELECT survey_year,
       SUM(term_yes + term_no) AS chi2_statistic,
       COUNT(*) AS rows_k,
       (COUNT(*) - 1) AS degrees_of_freedom
FROM chi_terms
GROUP BY survey_year
ORDER BY survey_year;
"""

QUERY_CONT = """

WITH openness AS (
    SELECT SurveyID, UserID,
           CASE UPPER(TRIM(AnswerText))
                WHEN 'VERY OPEN' THEN 'Very open'
                WHEN 'SOMEWHAT OPEN' THEN 'Somewhat open'
                WHEN 'NEUTRAL' THEN 'Neutral'
                WHEN 'SOMEWHAT NOT OPEN' THEN 'Somewhat not open'
                WHEN 'NOT OPEN AT ALL' THEN 'Not open at all'
                WHEN 'NOT APPLICABLE TO ME (I DO NOT HAVE A MENTAL ILLNESS)' THEN 'Not applicable'
                ELSE 'Other'
           END AS openness
    FROM Answer
    WHERE QuestionID = 30
),
self_report AS (
    SELECT SurveyID, UserID,
           CASE WHEN UPPER(TRIM(AnswerText)) = 'YES' THEN 1 ELSE 0 END AS self_yes
    FROM Answer
    WHERE QuestionID = 33
)
,
agg AS (
    SELECT o.SurveyID AS survey_year,
           o.openness,
           SUM(s.self_yes) AS yes_count,
           COUNT(*) - SUM(s.self_yes) AS no_count,
           COUNT(*) AS total
    FROM openness o
    JOIN self_report s
      ON o.SurveyID = s.SurveyID AND o.UserID = s.UserID
    WHERE o.openness NOT IN ('Not applicable', 'Other')
    GROUP BY o.SurveyID, o.openness
)
SELECT survey_year,
       openness,
       'yes_count' AS response,
       yes_count AS count,
       total,
       ROUND(100.0 * yes_count / NULLIF(total, 0), 2) AS percentage,
       CASE openness
            WHEN 'Very open' THEN 1
            WHEN 'Somewhat open' THEN 2
            WHEN 'Neutral' THEN 3
            WHEN 'Somewhat not open' THEN 4
            WHEN 'Not open at all' THEN 5
            ELSE 6
       END AS openness_order
FROM agg
UNION ALL
SELECT survey_year,
       openness,
       'no_count' AS response,
       no_count AS count,
       total,
       ROUND(100.0 * no_count / NULLIF(total, 0), 2) AS percentage,
       CASE openness
            WHEN 'Very open' THEN 1
            WHEN 'Somewhat open' THEN 2
            WHEN 'Neutral' THEN 3
            WHEN 'Somewhat not open' THEN 4
            WHEN 'Not open at all' THEN 5
            ELSE 6
       END AS openness_order
FROM agg
ORDER BY survey_year, openness_order, response;
"""
    