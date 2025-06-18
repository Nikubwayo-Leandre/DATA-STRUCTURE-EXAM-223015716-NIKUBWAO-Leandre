#include <iostream>
#include <cstring>
#include <stdexcept>

// Date structure
struct Date {
    int day, month, year;

    Date(int d = 1, int m = 1, int y = 2000) : day(d), month(m), year(y) {}

    void print() const {
        std::cout << day << "/" << month << "/" << year;
    }

    bool isBefore(const Date& other) const {
        if (year != other.year) return year < other.year;
        if (month != other.month) return month < other.month;
        return day < other.day;
    }

    bool isEqual(const Date& other) const {
        return day == other.day && month == other.month && year == other.year;
    }
};

// Attendance Record structure
struct AttRecord {
    char studentID[10];
    Date* date;
    bool present;

    AttRecord() : date(NULL), present(false) { // Changed nullptr to NULL
        studentID[0] = '\0';
    }

    AttRecord(const char* id, Date* d, bool p) : date(new Date(*d)), present(p) {
        strncpy(studentID, id, 9);
        studentID[9] = '\0';
    }

    // Copy constructor
    AttRecord(const AttRecord& other) : date(new Date(*other.date)), present(other.present) {
        strncpy(studentID, other.studentID, 10);
    }

    // Assignment operator
    AttRecord& operator=(const AttRecord& other) {
        if (this != &other) {
            strncpy(studentID, other.studentID, 10);
            present = other.present;
            if (date) delete date;
            date = new Date(*other.date);
        }
        return *this;
    }

    ~AttRecord() {
        delete date;
    }
};

// Abstract Report Base
class ReportBase {
public:
    virtual void generate(const AttRecord* recs, int n) const = 0;
    virtual ~ReportBase() {}
};

// Daily Report
class DailyReport : public ReportBase {
public:
    void generate(const AttRecord* recs, int n) const override {
        if (n == 0) {
            std::cout << "No attendance records to generate daily report.\n";
            return;
        }

        Date reportDate = *(recs[0].date);
        int count = 0, total = 0;

        for (int i = 0; i < n; ++i) {
            if (recs[i].date->isEqual(reportDate)) {
                total++;
                if (recs[i].present) count++;
            }
        }

        std::cout << "Daily Attendance Report for ";
        reportDate.print();
        std::cout << "\nPresent: " << count << " / " << total << "\n";
    }
};

// Trend Report
class TrendReport : public ReportBase {
public:
    void generate(const AttRecord* recs, int n) const override {
        if (n < 3) {
            std::cout << "Not enough records to detect trends.\n";
            return;
        }

        // Copy and sort records by date
        AttRecord* sorted = new AttRecord[n];
        for (int i = 0; i < n; ++i) sorted[i] = recs[i];

        for (int i = 0; i < n - 1; ++i)
            for (int j = 0; j < n - i - 1; ++j)
                if (sorted[j + 1].date->isBefore(*sorted[j].date))
                    std::swap(sorted[j], sorted[j + 1]);

        // Detect trend
        bool downward = false;
        for (int i = 2; i < n; ++i) {
            if (sorted[i - 2].present && !sorted[i - 1].present && !sorted[i].present) {
                downward = true;
                break;
            }
        }

        std::cout << "Trend Report: Downward trend detected: " << (downward ? "Yes" : "No") << "\n";
        delete[] sorted;
    }
};

// Attendance Manager
class AttendanceManager {
private:
    AttRecord* records;
    int recordCount, recordCapacity;

    ReportBase** reports;
    int reportCount, reportCapacity;

    void resizeRecords(int newCap) {
        AttRecord* temp = new AttRecord[newCap];
        for (int i = 0; i < recordCount; ++i)
            temp[i] = records[i];
        delete[] records;
        records = temp;
        recordCapacity = newCap;
    }

    void resizeReports(int newCap) {
        ReportBase** temp = new ReportBase*[newCap];
        for (int i = 0; i < reportCount; ++i)
            temp[i] = reports[i];
        delete[] reports;
        reports = temp;
        reportCapacity = newCap;
    }

public:
    AttendanceManager() : records(NULL), recordCount(0), recordCapacity(0),
                          reports(NULL), reportCount(0), reportCapacity(0) {} // Changed nullptr to NULL

    ~AttendanceManager() {
        delete[] records;
        for (int i = 0; i < reportCount; ++i)
            delete reports[i];
        delete[] reports;
    }

    void addAttendance(const AttRecord& rec) {
        if (recordCount >= recordCapacity)
            resizeRecords(recordCapacity == 0 ? 2 : recordCapacity * 2);
        records[recordCount++] = rec;
    }

    void removeAttendance(int index) {
        if (index < 0 || index >= recordCount) {
            std::cout << "Invalid index.\n";
            return;
        }
        for (int i = index; i < recordCount - 1; ++i)
            records[i] = records[i + 1];
        --recordCount;
        if (recordCount <= recordCapacity / 4 && recordCapacity > 2)
            resizeRecords(recordCapacity / 2);

        std::cout << "Attendance record at index " << index << " removed successfully.\n";
    }

    void addReport(ReportBase* report) {
        if (reportCount >= reportCapacity)
            resizeReports(reportCapacity == 0 ? 2 : reportCapacity * 2);
        reports[reportCount++] = report;
    }

    void generateAllReports() const {
        for (int i = 0; i < reportCount; ++i) {
            reports[i]->generate(records, recordCount);
            std::cout << "----------------------\n";
        }
    }
};

// Main Program
int main() {
    AttendanceManager manager;

    manager.addAttendance(AttRecord("S001", new Date(10, 6, 2023), true));
    manager.addAttendance(AttRecord("S002", new Date(10, 6, 2023), false));
    manager.addAttendance(AttRecord("S003", new Date(10, 6, 2023), true));
    manager.addAttendance(AttRecord("S001", new Date(11, 6, 2023), true));
    manager.addAttendance(AttRecord("S002", new Date(11, 6, 2023), false));
    manager.addAttendance(AttRecord("S003", new Date(11, 6, 2023), false));
    manager.addAttendance(AttRecord("S001", new Date(12, 6, 2023), false));
    manager.addAttendance(AttRecord("S002", new Date(12, 6, 2023), false));
    manager.addAttendance(AttRecord("S003", new Date(12, 6, 2023), false));

    manager.addReport(new DailyReport());
    manager.addReport(new TrendReport());

    std::cout << "=== Initial Reports ===\n";
    manager.generateAllReports();

    std::cout << "\n=== After Removing First Record ===\n";
    manager.removeAttendance(0);
    manager.generateAllReports();

    return 0;
}

