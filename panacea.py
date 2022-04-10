# panacea imports
from panacea_web_grab_from_dump import *
from panacea_gui_widgets import *


# main program starts here:

class app_window(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(app_window, self).__init__(*args, **kwargs)
        self.items = gettext(PREFS)
        self.widgets = {}
        # stuff goes here
        self.controls = QWidget()
        self.controlsLayout = QVBoxLayout()
        for i in self.items:
            # print(i)
            aw = tip(str(i[0]).strip(), i[1], i[2].strip(), i[3].strip(), i[4])
            aw.tags = i[1]
            self.controlsLayout.addWidget(aw)
            self.widgets[i[0]] = aw

        spacer = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.controlsLayout.addItem(spacer)
        self.controls.setLayout(self.controlsLayout)

        # Scroll Area Properties.
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.controls)

        # Search bar.
        self.searchbar = QLineEdit()
        self.searchbar.textChanged.connect(self.update_display)
        self.completionlist = []
        for i in self.widgets:
            self.completionlist.append(self.widgets[i].text)
            self.completionlist.extend(self.widgets[i].tags)
        self.completionlist = list(set(self.completionlist))
        self.completer = QCompleter(self.completionlist)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.searchbar.setCompleter(self.completer)

        settings_menu_item = QAction(QIcon("bug.png"), "&Settings", self)
        settings_menu_item.setStatusTip("Settings")
        settings_menu_item.triggered.connect(self.settings_button_clicked)
        settings_menu_item.setCheckable(True)

        about_menu_item = QAction(QIcon("bug.png"), "&About", self)
        about_menu_item.setStatusTip("About")
        about_menu_item.triggered.connect(self.about_button_clicked)
        about_menu_item.setCheckable(True)

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        file_menu.addAction(settings_menu_item)
        file_menu.addAction(about_menu_item)

        container = QWidget()
        containerLayout = QVBoxLayout()
        containerLayout.addWidget(self.searchbar)
        containerLayout.addWidget(self.scroll)

        container.setLayout(containerLayout)
        self.setCentralWidget(container)

        self.timer = QTimer()
        self.timer.setInterval(1000*60*60)
        self.timer.timeout.connect(self.notify)
        self.timer.start()

        self.setGeometry(600, 100, 800, 600)
        self.setWindowTitle('Eco Friend')
        self.setCentralWidget(container)

        self.notify()
        self.exit = QAction("Exit Application", shortcut=QKeySequence(
            "Ctrl+q"), triggered=lambda: self.close())
        self.addAction(self.exit)

    def update_display(self, text):

        for i in self.widgets:
            if text.lower() in self.widgets[i].text.lower() or contains(self.widgets[i].tags, text.lower()):
                self.widgets[i].show()
            else:
                self.widgets[i].hide()

    def notify(self):
        if not BACKEND.nots:
            return None
        notslist = []
        for i in self.widgets:
            if self.widgets[i].nots:
                notslist.append(self.widgets[i].text)
        if notslist:
            nstring = ("Remember to do " + str(notslist)
                       [1:len(str(notslist))-1])[:256]
        else:
            nstring = "Remember to keep up on your Eco Goals "
        notification.notify(title="Keep working on your Eco Friendly Lifestyle",
                            message=nstring, app_name="Eco Friend", timeout=9999, toast=True, ticker="EcoFriend Remainder", app_icon="resources/icon.ico")

    def settings_button_clicked(self, s):
        self.msg = settings()
        self.msg.show()

    def about_button_clicked(self, s):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText("About")
        self.msg.setInformativeText("About")
        self.msg.setWindowTitle("MessageBox demo")
        self.msg.setDetailedText("About")
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.msg.exec()


app = QApplication([])
app.setStyle('WindowsVista')
app.setQuitOnLastWindowClosed(True)
app.setApplicationName("Eco Friend")
app.setOrganizationName("Eco Friend")
app.setOrganizationDomain("Eco Friend")
w = app_window()
w.show()
sys.exit(app.exec())
app.exec_()
db.sync()
db.close()
sys.exit(0)
