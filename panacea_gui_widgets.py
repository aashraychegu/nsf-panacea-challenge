
from panacea_other_imports import *


class info(QWidget):
    def __init__(self, title, moretext, url, uid) -> None:
        super(info, self).__init__()
        self.url = url
        self.container = QVBoxLayout()
        self.titlelabel = QLabel(title)
        self.titlelabel.setWordWrap(True)
        self.moretextlabel = QLabel(moretext)
        self.moretextlabel.setWordWrap(True)
        self.linkbutton = QPushButton("More information")
        self.uid = QLabel("Tip unique identifier: "+uid)

        self.container.addWidget(self.titlelabel)
        self.container.addWidget(self.moretextlabel)
        self.container.addWidget(self.uid)
        self.container.addWidget(self.linkbutton)
        self.linkbutton.clicked.connect(self.open_link)
        self.setLayout(self.container)

    def open_link(self):
        open_new_web_page(self.url)


class preferences(QWidget):
    def __init__(self, uid, v=35, h=120):
        super(preferences, self).__init__()
        self.uid = uid
        self.clearbtn = QPushButton("Clear my data for this tip")
        self.clearbtn.setMinimumSize(h, v)
        self.delbtn = QPushButton(
            "Delete this tip. Use this if there is a Bug or error")
        self.delbtn.setMinimumSize(h, v)
        self.allbtn = QPushButton("Select all for this tip")
        self.allbtn.setMinimumSize(h, v)
        self.unallbtn = QPushButton("Select all for this tip")
        self.unallbtn.setMinimumSize(h, v)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.clearbtn)
        self.layout.addWidget(self.delbtn)
        self.layout.addWidget(self.allbtn)
        self.layout.addWidget(self.unallbtn)
        self.setLayout(self.layout)
        self.clearbtn.clicked.connect(self.clearbtnclicked)
        self.delbtn.clicked.connect(self.delbtnclicked)
        self.allbtn.clicked.connect(self.allbtnclicked)
        self.unallbtn.clicked.connect(self.unallbtnclicked)

    def unallbtnclicked(self):
        setpref(self.uid, [False, False])

    def clearbtnclicked(self):
        setpref(self.uid, [False, False])

    def delbtnclicked(self):
        delpref(self.uid)
        setpref(self.uid, [False, False])

    def allbtnclicked(self):
        setpref(self.uid, [True, True])


class tip(QWidget):

    def __init__(self, text, tags, extratext, url, uid, v=35, h=120):
        super(tip, self).__init__()
        self.uid = uid
        self.prettyuid = "TUID-"+str(uid)
        self.url = url
        self.tags = tags
        self.text = text  # Name of widget used for searching.
        self.extratext = extratext
        ##
        self.is_on = False
        self.nots = False
        if loadpref(self.uid) != None:
            self.is_on, self.nots = loadpref(self.uid)
        elif loadpref(self.uid) == [None, None]:
            setpref(self.uid, [False, False])
        else:
            setpref(self.uid, [False, False])
        self.is_on, self.nots = loadpref(self.uid)
        self.tags = []
        self.label = QLabel(text)
        self.label.setMinimumSize(h, v)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.resize(300, 25)
        self.onbtn = QPushButton("I want to do this")
        self.onbtn.setMinimumSize(h, v)
        self.onbtn.resize(300, 25)
        self.notbtn = QCheckBox("I want notifications for this")
        self.notbtn.setStyleSheet("padding-left: 10;")
        self.notbtn.setChecked(loadpref(self.uid)[1])
        self.notbtn.setStyleSheet(
            "QCheckBox::indicator { width:25px; height: 20px;}")
        self.notbtn.setMinimumSize(h, v)
        self.moreinfo = QPushButton("Click for more information")
        self.moreinfo.setMinimumSize(h, v)
        self.prefbox = QPushButton("Preferences")
        self.prefbox.resize(300, 25)
        self.prefbox.setMinimumSize(h, v)
        self.box = QHBoxLayout()
        self.box.addWidget(self.label)
        self.box.addWidget(self.onbtn)
        self.box.addWidget(self.notbtn)
        self.box.addWidget(self.prefbox)
        self.box.addWidget(self.moreinfo)
        self.setLayout(self.box)
        self.setMinimumSize(self.sizeHint())
        self.onbtn.clicked.connect(self.btnclicked)
        self.notbtn.clicked.connect(self.notboxclicked)
        self.moreinfo.clicked.connect(self.infobtnclicked)
        self.prefbox.clicked.connect(self.prefboxclicked)
        self.colortext()
        setpref(self.uid, [self.is_on, self.nots])

    def notboxclicked(self):
        self.nots = self.notbtn.isChecked()
        setpref(self.uid, [self.is_on, self.nots])

    def btnclicked(self):
        self.is_on = not self.is_on
        setpref(self.uid, [self.is_on, self.nots])
        self.colortext()

    def colortext(self):
        if self.is_on:
            self.onbtn.setText("I am doing this")
            self.label.setStyleSheet("color: #4CAF50;")
        else:
            self.onbtn.setText("I am not doing this")
            self.label.setStyleSheet("color: #000000;")

    def infobtnclicked(self):
        self.infobox = info(self.text, self.extratext,
                            self.url, self.prettyuid)
        self.infobox.resize(300, 100)
        self.infobox.show()

    def prefboxclicked(self):
        self.aprefbox = preferences(self.uid)
        self.aprefbox.resize(300, 300)
        self.aprefbox.show()


class settings(QWidget):
    def __init__(self):
        super(settings, self).__init__()
        self.notsbox = QCheckBox("I don't want Notifications")
        self.delprefs = QPushButton("Delete Preferences")
        self.source = QLineEdit("Your source for tips.")
        self.source.textChanged.connect(self.changeprefs)
        self.container = QVBoxLayout()
        self.container.addWidget(self.notsbox)
        self.container.addWidget(self.delprefs)
        self.container.addWidget(self.source)
        self.notsbox.clicked.connect(self.changenots)
        self.delprefs.clicked.connect(self.delprefsclicked)
        self.setLayout(self.container)

    def changenots(self):
        BACKEND.nots = not BACKEND.nots

    def changeprefs(self, text):
        BACKEND.source = text

    def delprefsclicked(self):
        for i in db:
            del db[i]
