### My project question

# Question: 71
.Attendance Report Generator
Description: Generate attendance reports from dynamic arrays of records; two report types
share a base interface.
Tasks:

• Define struct AttRecord { char studentID[10]; Date* date;
bool present; }; and allocate AttRecord* recs dynamically.

• Create an abstract class ReportBase with virtual void generate(const
AttRecord*, int) = 0;, then derive DailyReport : ReportBase
(counts present) and TrendReport : ReportBase (detects downward trend)
to demonstrate inheritance and polymorphism.

• Store ReportBase* in a dynamic ReportBase** reports; calling
reports[i]->generate(recs, n) dispatches correctly.

• Use pointer arithmetic on recs to count presence and detect trends.

• Implement addAttendance(AttRecord) and removeAttendance(int
index) by resizing AttRecord*

## detail: this project deals with attendence report but in C++ programming languege 
## screen shot of result on project
![screen shot on project examination](https://github.com/user-attachments/assets/4a219195-44d6-44fe-9f5d-2fb9d7fbcc1a)

