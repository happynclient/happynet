
from PySide2 import QtCore, QtWidgets, QtGui

class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.clientModel = QtCore.QSortFilterProxyModel()
        self.clientModel.setDynamicSortFilter(True)
        # default set filter all key columns
        self.clientModel.setFilterKeyColumn(-1)

        self.serverGroupBox = QtWidgets.QGroupBox("Server Stat")
        self.clientGroupBox = QtWidgets.QGroupBox("Sorted/Filtered Client Stat")

        self.serverView = QtWidgets.QTreeView()
        self.serverView.setRootIsDecorated(False)
        self.serverView.setAlternatingRowColors(True)

        self.clientView = QtWidgets.QTreeView()
        self.clientView.setRootIsDecorated(False)
        self.clientView.setAlternatingRowColors(True)
        self.clientView.setModel(self.clientModel)
        self.clientView.setSortingEnabled(True)

        self.sortCaseSensitivityCheckBox = QtWidgets.QCheckBox("Case sensitive sorting")
        self.filterCaseSensitivityCheckBox = QtWidgets.QCheckBox("Case sensitive filter")

        self.filterPatternLineEdit = QtWidgets.QLineEdit()
        self.filterPatternLabel = QtWidgets.QLabel("&Search:")
        self.filterPatternLabel.setBuddy(self.filterPatternLineEdit)

        self.filterSyntaxComboBox = QtWidgets.QComboBox()
        self.filterSyntaxComboBox.addItem("Regular expression",
                QtCore.QRegExp.RegExp)
        self.filterSyntaxComboBox.addItem("Wildcard",
                QtCore.QRegExp.Wildcard)
        self.filterSyntaxComboBox.addItem("Fixed string",
                QtCore.QRegExp.FixedString)
        self.filterSyntaxLabel = QtWidgets.QLabel("Filter &syntax:")
        self.filterSyntaxLabel.setBuddy(self.filterSyntaxComboBox)

        self.filterColumnComboBox = QtWidgets.QComboBox()
        self.filterColumnComboBox.addItem("Subject")
        self.filterColumnComboBox.addItem("Sender")
        self.filterColumnComboBox.addItem("Date")
        self.filterColumnLabel = QtWidgets.QLabel("Filter &column:")
        self.filterColumnLabel.setBuddy(self.filterColumnComboBox)

        self.filterPatternLineEdit.textChanged.connect(self.filterRegExpChanged)
        self.filterSyntaxComboBox.currentIndexChanged.connect(self.filterRegExpChanged)
        self.filterColumnComboBox.currentIndexChanged.connect(self.filterColumnChanged)
        self.filterCaseSensitivityCheckBox.toggled.connect(self.filterRegExpChanged)
        self.sortCaseSensitivityCheckBox.toggled.connect(self.sortChanged)

        sourceLayout = QtWidgets.QHBoxLayout()
        sourceLayout.addWidget(self.serverView)
        self.serverGroupBox.setLayout(sourceLayout)

        proxyLayout = QtWidgets.QGridLayout()
        proxyLayout.addWidget(self.clientView, 0, 0, 1, 3)
        proxyLayout.addWidget(self.filterPatternLabel, 1, 0)
        proxyLayout.addWidget(self.filterPatternLineEdit, 1, 1, 1, 2)
        # proxyLayout.addWidget(self.filterColumnLabel, 3, 0)
        # proxyLayout.addWidget(self.filterColumnComboBox, 3, 1, 1, 2)
        self.clientGroupBox.setLayout(proxyLayout)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.serverGroupBox)
        mainLayout.addWidget(self.clientGroupBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Happynet Device Stat")
        self.resize(900, 650)

        self.clientView.sortByColumn(1, QtCore.Qt.AscendingOrder)
        self.filterColumnComboBox.setCurrentIndex(0)

        self.filterPatternLineEdit.setText("")
        self.filterCaseSensitivityCheckBox.setChecked(False)
        self.sortCaseSensitivityCheckBox.setChecked(False)

    def setClientModel(self, model):
        self.clientModel.setSourceModel(model)

    def setServerModel(self, model):
        self.serverView.setModel(model)

    def filterRegExpChanged(self):
        syntax_nr = self.filterSyntaxComboBox.itemData(self.filterSyntaxComboBox.currentIndex())
        syntax = QtCore.QRegExp.PatternSyntax(syntax_nr)

        if self.filterCaseSensitivityCheckBox.isChecked():
            caseSensitivity = QtCore.Qt.CaseSensitive
        else:
            caseSensitivity = QtCore.Qt.CaseInsensitive

        regExp = QtCore.QRegExp(self.filterPatternLineEdit.text(),
                caseSensitivity, syntax)
        self.clientModel.setFilterRegExp(regExp)

    def filterColumnChanged(self):
        self.clientModel.setFilterKeyColumn(self.filterColumnComboBox.currentIndex())

    def sortChanged(self):
        if self.sortCaseSensitivityCheckBox.isChecked():
            caseSensitivity = QtCore.Qt.CaseSensitive
        else:
            caseSensitivity = QtCore.Qt.CaseInsensitive

        self.clientModel.setSortCaseSensitivity(caseSensitivity)


