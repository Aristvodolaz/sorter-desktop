from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Главный контейнер для вкладок
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 1180, 750))
        self.tabWidget.setObjectName("tabWidget")

        # Вкладка EO
        self.tabEO = QtWidgets.QWidget()
        self.tabEO.setObjectName("tabEO")

        # Главный вертикальный layout для вкладки EO
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tabEO)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(10)

        # Поле ввода для поиска
        self.lineEditSearch = QtWidgets.QLineEdit(self.tabEO)
        self.lineEditSearch.setObjectName("lineEditSearch")
        self.lineEditSearch.setPlaceholderText("Введите текст для поиска...")
        self.verticalLayout.addWidget(self.lineEditSearch)

        # Горизонтальный layout для кнопок
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(10)

        # Кнопка загрузки данных
        self.btnLoadData = QtWidgets.QPushButton(self.tabEO)
        self.btnLoadData.setObjectName("btnLoadData")
        self.btnLoadData.setText("Загрузить данные")
        self.horizontalLayout.addWidget(self.btnLoadData)

        # Кнопка поиска
        self.btnSearch = QtWidgets.QPushButton(self.tabEO)
        self.btnSearch.setObjectName("btnSearch")
        self.btnSearch.setText("Поиск")
        self.horizontalLayout.addWidget(self.btnSearch)

        # Добавляем горизонтальный layout в основной вертикальный layout
        self.verticalLayout.addLayout(self.horizontalLayout)

        # Дерево для отображения списка EO
        self.treeWidgetEO = QtWidgets.QTreeWidget(self.tabEO)
        self.treeWidgetEO.setHeaderLabels(['Cargo Unit ID', 'EO'])
        self.treeWidgetEO.setObjectName("treeWidgetEO")
        self.verticalLayout.addWidget(self.treeWidgetEO)

        # Добавляем вкладку EO в главное окно
        self.tabWidget.addTab(self.tabEO, "Список реестров")


        # Вкладка отчётов
        self.tabReports = QtWidgets.QWidget()
        self.tabReports.setObjectName("tabReports")

        self.btnGenerateReport = QtWidgets.QPushButton(self.tabReports)
        self.btnGenerateReport.setGeometry(QtCore.QRect(10, 10, 200, 40))
        self.btnGenerateReport.setObjectName("btnGenerateReport")
        self.btnGenerateReport.setText("Сформировать")

        self.textEditReportPreview = QtWidgets.QTextEdit(self.tabReports)
        self.textEditReportPreview.setGeometry(QtCore.QRect(10, 60, 1160, 650))
        self.textEditReportPreview.setObjectName("textEditReportPreview")

        # Добавляем вкладку отчётов в главное окно
        self.tabWidget.addTab(self.tabReports, "Отчёты")

        # Настройка главного окна
        MainWindow.setCentralWidget(self.centralwidget)

        # Установка текста для элементов интерфейса
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Управление паллетами и EO"))
