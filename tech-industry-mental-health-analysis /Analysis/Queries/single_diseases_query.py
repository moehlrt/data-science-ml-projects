# Calculating the prevalence rate of the most common disorders diagnosed.

QUERY_DISORDER = """ 

WITH disease_counts AS (
    SELECT 
        'Mood Disorder (Depression, Bipolar Disorder, etc)' AS disease,
        COUNT(*) AS count
    FROM Answer
    WHERE QuestionID = 115
      AND AnswerText LIKE '%Mood Disorder (Depression, Bipolar Disorder, etc)%'

    UNION ALL

    SELECT 
        'Anxiety Disorder (Generalized, Social, Phobia, etc)' AS disease,
        COUNT(*) AS count
    FROM Answer
    WHERE QuestionID = 115
      AND AnswerText LIKE '%Anxiety Disorder (Generalized, Social, Phobia, etc)%'

    UNION ALL

    SELECT 
        'Attention Deficit Hyperactivity Disorder' AS disease,
        COUNT(*) AS count
    FROM Answer
    WHERE QuestionID = 115
      AND AnswerText LIKE '%Attention Deficit Hyperactivity Disorder%'
),
total AS (
    SELECT COUNT(DISTINCT UserID) AS n_total
    FROM Answer
    WHERE QuestionID = 115
)
SELECT 
    d.disease,
    d.count,
    t.n_total,
    ROUND(100.0 * d.count / t.n_total, 2) AS prevalence_percent,
    ROUND(100.0 * (d.count*1.0 / t.n_total - 1.96 * SQRT((d.count*1.0/t.n_total)*(1 - d.count*1.0/t.n_total)/t.n_total)), 2) AS ci_lower_percent,
    ROUND(100.0 * (d.count*1.0 / t.n_total + 1.96 * SQRT((d.count*1.0/t.n_total)*(1 - d.count*1.0/t.n_total)/t.n_total)), 2) AS ci_upper_percent
FROM disease_counts d
CROSS JOIN total t
ORDER BY prevalence_percent DESC;
"""