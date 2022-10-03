from PySide2 import QtCore, QtWidgets, QtGui
from netcat import get_edges

class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.clientModel = QtCore.QSortFilterProxyModel()
        self.clientModel.setDynamicSortFilter(True)
        # default set filter all key columns
        self.clientModel.setFilterKeyColumn(-1)

        self.serverGroupBox = QtWidgets.QGroupBox("happyn服务端列表")
        self.clientGroupBox = QtWidgets.QGroupBox("happyn网络客户端列表(不包括本机)")

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
        self.filterPatternLabel = QtWidgets.QLabel("&搜索:")
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
        #mainLayout.addWidget(self.serverGroupBox)
        mainLayout.addWidget(self.clientGroupBox)
        self.setLayout(mainLayout)

        icon = QtGui.QIcon()
        icon.addFile(u"happynet.ico", QtCore.QSize(),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        self.setWindowTitle("Happynet Device Monitor")
        self.resize(900, 450)

        self.clientView.sortByColumn(1, QtCore.Qt.AscendingOrder)
        self.filterColumnComboBox.setCurrentIndex(0)

        self.filterPatternLineEdit.setText("")
        self.filterCaseSensitivityCheckBox.setChecked(False)
        self.sortCaseSensitivityCheckBox.setChecked(False)

    def updateClientModel(self):
        model = self.updateDeviceStatModel()
        self.clientModel.setSourceModel(model)
        self.clientView.header().resizeSection(0, 100)
        self.clientView.header().resizeSection(1, 80)
        self.clientView.header().resizeSection(2, 150)
        self.clientView.header().resizeSection(3, 150)
        self.clientView.header().resizeSection(4, 180)
        #self.clientView.setColumnWidth(0, 200)
        #self.clientView.resizeColumnToContents(0)

    def updateServerModel(self):
        model = self.updateDeviceStatModel()
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

    def addDevice(self, model, name, mode, mac, ip, sockaddr, uptime):
        model.insertRow(0)
        model.setData(model.index(0, 0), name)
        model.setData(model.index(0, 1), mode)
        model.setData(model.index(0, 2), mac)
        model.setData(model.index(0, 3), ip)
        model.setData(model.index(0, 4), sockaddr)
        model.setData(model.index(0, 5), uptime)


    def updateDeviceStatModel(self):
        model = QtGui.QStandardItemModel(0, 6, self)

        model.setHeaderData(0, QtCore.Qt.Horizontal, "设备名称")
        model.setHeaderData(1, QtCore.Qt.Horizontal, "通讯模式")
        model.setHeaderData(2, QtCore.Qt.Horizontal, "happyn mac地址")
        model.setHeaderData(3, QtCore.Qt.Horizontal, "happyn 内网ip")
        model.setHeaderData(4, QtCore.Qt.Horizontal, "本机对外通信ip:port")
        model.setHeaderData(5, QtCore.Qt.Horizontal, "最近活动时间")

        for device in get_edges():
            self.addDevice(model, device['desc'], device['mode'], device['macaddr'],
                             device['ip4addr'], device['sockaddr'],
                             QtCore.QDateTime.fromMSecsSinceEpoch(device['last_seen']*1000).toString('yyyy-MM-dd hh:mm:ss'))
                      #QtCore.QDateTime(QtCore.QDate(2006, 12, 22), QtCore.QTime(9, 44)))

        return model