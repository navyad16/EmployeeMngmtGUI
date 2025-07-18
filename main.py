# main.py

import sys
from PyQt5 import QtWidgets, uic
import database

class EmployeeApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the Qt Designer .ui file
        uic.loadUi("ui_main.ui", self)

        # Initialize database table
        database.create_table()

        # Load data into table
        self.load_data()

        # Connect buttons to functions
        self.addBtn.clicked.connect(self.add_employee)
        self.updateBtn.clicked.connect(self.update_employee)
        self.deleteBtn.clicked.connect(self.delete_employee)
        self.searchBtn.clicked.connect(self.search_employee)
        self.tableWidget.itemSelectionChanged.connect(self.load_selected_row)

    def load_data(self):
        """Fetch all employees and display in the table."""
        self.tableWidget.setRowCount(0)
        for row_idx, record in enumerate(database.get_all_employees()):
            self.tableWidget.insertRow(row_idx)
            for col_idx, value in enumerate(record):
                self.tableWidget.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(value)))

    def add_employee(self):
        """Insert a new employee record."""
        name = self.nameLine.text().strip()
        dept = self.departmentLine.text().strip()
        salary_text = self.salaryLine.text().strip()

        if not name or not salary_text:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Name and Salary are required.")
            return

        try:
            salary = float(salary_text)
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Salary must be a number.")
            return

        database.insert_employee(name, dept, salary)
        self.load_data()
        self.clear_fields()

    def update_employee(self):
        """Update the selected employee record."""
        selected = self.tableWidget.currentRow()
        if selected < 0:
            return

        emp_id = int(self.tableWidget.item(selected, 0).text())
        name = self.nameLine.text().strip()
        dept = self.departmentLine.text().strip()
        salary_text = self.salaryLine.text().strip()

        if not name or not salary_text:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Name and Salary are required.")
            return

        try:
            salary = float(salary_text)
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Salary must be a number.")
            return

        database.update_employee(emp_id, name, dept, salary)
        self.load_data()
        self.clear_fields()

    def delete_employee(self):
        """Delete the selected employee record."""
        selected = self.tableWidget.currentRow()
        if selected < 0:
            return

        emp_id = int(self.tableWidget.item(selected, 0).text())
        confirm = QtWidgets.QMessageBox.question(
            self, "Confirm Delete",
            f"Delete employee ID {emp_id}?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if confirm == QtWidgets.QMessageBox.Yes:
            database.delete_employee(emp_id)
            self.load_data()
            self.clear_fields()

    def search_employee(self):
        """Search employees by keyword and display results."""
        keyword = self.searchLine.text().strip()
        self.tableWidget.setRowCount(0)
        for row_idx, record in enumerate(database.search_employees(keyword)):
            self.tableWidget.insertRow(row_idx)
            for col_idx, value in enumerate(record):
                self.tableWidget.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(value)))

    def load_selected_row(self):
        """Load data from the selected table row into input fields."""
        selected = self.tableWidget.currentRow()
        if selected < 0:
            return

        self.nameLine.setText(self.tableWidget.item(selected, 1).text())
        self.departmentLine.setText(self.tableWidget.item(selected, 2).text())
        self.salaryLine.setText(self.tableWidget.item(selected, 3).text())

    def clear_fields(self):
        """Clear all input fields."""
        self.nameLine.clear()
        self.departmentLine.clear()
        self.salaryLine.clear()
        self.searchLine.clear()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = EmployeeApp()
    window.setWindowTitle("Employee Management System")
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())

