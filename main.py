import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTreeWidgetItem
from PyQt5 import QtCore
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle, Spacer, Paragraph, SimpleDocTemplate

from core.api import APIClient
from ui.main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Подключаем сигнал для кнопок
        self.ui.btnLoadData.clicked.connect(self.load_data)
        self.ui.btnSearch.clicked.connect(self.filter_tree)
        self.ui.btnGenerateReport.clicked.connect(self.generate_report)

        # Хранилище данных для быстрого доступа
        self.records = []

    def load_data(self):
        try:
            response = APIClient.fetch_full_info()
            data = response.get("data", [])

            if not data:
                QMessageBox.information(self, "Информация", "Данные отсутствуют.")
                return

            # Очищаем дерево и сохраняем записи
            self.ui.treeWidgetEO.clear()
            self.records = data

            # Группируем записи по 'EO' и 'Cargo_UNIT_ID'
            grouped_data = {}
            for record in data:
                eo = record.get("eo", "Не указано")
                cargo_unit_id = record.get("Cargo_UNIT_ID", "Не указано")

                if (eo, cargo_unit_id) not in grouped_data:
                    grouped_data[(eo, cargo_unit_id)] = []
                grouped_data[(eo, cargo_unit_id)].append(record)

            # Заполняем дерево
            for (eo, cargo_unit_id), records in grouped_data.items():
                top_item = QTreeWidgetItem([
                    cargo_unit_id,
                    f"{eo}",
                    f"Всего записей: {len(records)}"
                ])
                self.ui.treeWidgetEO.addTopLevelItem(top_item)

                for record in records:
                    details = (
                        f"Серийный номер: {record.get('sn', 'Не указано')} | "
                        f"Адрес: {record.get('address', 'Не указано')} | "
                        f"Клиент: {record.get('client', 'Не указано')} | "
                        f"Место: {record.get('mesto', 'Не указано')} | "
                        f"Дата создания: {record.get('created_at', 'Не указано')}"
                    )
                    child_item = QTreeWidgetItem([details])
                    top_item.addChild(child_item)

            # Раскрываем все записи
            self.ui.treeWidgetEO.expandAll()

            # Автоматическая подгонка ширины столбцов
            for i in range(self.ui.treeWidgetEO.columnCount()):
                self.ui.treeWidgetEO.resizeColumnToContents(i)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные:\n{e}")

    def filter_tree(self):
        search_text = self.ui.lineEditSearch.text().strip().lower()

        if not search_text:
            QMessageBox.information(self, "Информация", "Введите текст для поиска.")
            return

        # Очищаем дерево перед добавлением результатов фильтрации
        self.ui.treeWidgetEO.clear()

        if not self.records:
            QMessageBox.warning(self, "Ошибка", "Нет данных для фильтрации. Загрузите данные сначала.")
            return

        # Фильтрация данных
        filtered_data = [record for record in self.records if search_text in str(record).lower()]

        if not filtered_data:
            QMessageBox.information(self, "Результаты поиска", "Ничего не найдено.")
            return

        # Группируем отфильтрованные записи
        grouped_data = {}
        for record in filtered_data:
            eo = record.get("eo", "Не указано")
            cargo_unit_id = record.get("Cargo_UNIT_ID", "Не указано")
            if (eo, cargo_unit_id) not in grouped_data:
                grouped_data[(eo, cargo_unit_id)] = []
            grouped_data[(eo, cargo_unit_id)].append(record)

        # Добавляем данные в дерево
        for (eo, cargo_unit_id), records in grouped_data.items():
            top_item = QTreeWidgetItem([
                cargo_unit_id,
                f"{eo}",
                f"Всего записей: {len(records)}"
            ])
            self.ui.treeWidgetEO.addTopLevelItem(top_item)

            for record in records:
                details = (
                    f"Серийный номер: {record.get('sn', 'Не указано')} | "
                    f"Адрес: {record.get('address', 'Не указано')} | "
                    f"Клиент: {record.get('client', 'Не указано')} | "
                    f"Место: {record.get('mesto', 'Не указано')} | "
                    f"Дата создания: {record.get('created_at', 'Не указано')}"
                )
                child_item = QTreeWidgetItem([details])
                top_item.addChild(child_item)

        self.ui.treeWidgetEO.expandAll()

    def generate_report(self):
        try:
            if not self.records:
                QMessageBox.warning(self, "Ошибка", "Нет данных для отчета.")
                return

            output_file = "report.pdf"
            doc = SimpleDocTemplate(output_file, pagesize=A4)
            elements = []

            # Заголовок отчета
            elements.append(Paragraph("Грузовая спецификация", getSampleStyleSheet()["Heading1"]))
            elements.append(Spacer(1, 12))

            # Таблица с данными
            table_data = [["№", "Cargo Unit ID", "EO", "Серийный номер", "Адрес", "Клиент", "Место", "Дата"]]
            for idx, record in enumerate(self.records):
                table_data.append([
                    idx + 1,
                    record.get("Cargo_UNIT_ID", ""),
                    record.get("eo", ""),
                    record.get("sn", ""),
                    record.get("address", ""),
                    record.get("client", ""),
                    record.get("mesto", ""),
                    record.get("created_at", "")
                ])

            table = Table(table_data, colWidths=[40, 80, 80, 80, 120, 120, 60, 80])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))

            elements.append(table)
            doc.build(elements)

            QMessageBox.information(self, "Отчет", f"Отчет успешно создан: {output_file}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать отчет:\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Загрузка стилей
    try:
        with open("assets/style.qss", "r") as style:
            app.setStyleSheet(style.read())
    except FileNotFoundError:
        print("Warning: Style file not found. Proceeding without styles.")

    # Запуск главного окна
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())