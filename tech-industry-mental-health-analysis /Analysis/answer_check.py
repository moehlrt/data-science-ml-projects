import sqlite3
from consts import MENTAL_HEALTH_DATASET_PATH
import shutil

shutil.copy(MENTAL_HEALTH_DATASET_PATH, '../Dataset/mental_health_copy.sqlite')
conn = sqlite3.connect('../Dataset/mental_health_copy.sqlite')
cursor = conn.cursor()

# Query used to check all answers for various questions

cursor.execute("SELECT a.AnswerText, COUNT(*) FROM Answer a WHERE QuestionID = X GROUP BY a.AnswerText ORDER BY COUNT(*) DESC")
print(cursor.fetchall())

# To check when the questions where asked, for example to check whether: 
# Q: 93 Do you work remotely (outside of an office) at least 50% of the time? - only asked 2014 - and the 33, 34 were asked from 2016 +

cursor.execute("""
SELECT QuestionID, SurveyID, COUNT(*) as Answers
FROM Answer 
WHERE QuestionID IN (X, Y)
GROUP BY QuestionID, SurveyID
ORDER BY QuestionID, SurveyID
""")
print(cursor.fetchall())

