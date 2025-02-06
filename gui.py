from mido import (MetaMessage, MidiFile, MidiTrack)
from os import path
from utils import LogicHandler
from PySide6.QtWidgets import (QSizePolicy, QWidget, QMainWindow, QVBoxLayout, QMessageBox, QTabWidget, QSpacerItem,
    QLabel, QHBoxLayout, QSpinBox, QDoubleSpinBox, QLineEdit, QPushButton, QFileDialog)

class TrackSettingsWidget(QWidget):
    def __init__(self, trackIndex, parent=None):
        super().__init__(parent)
        self.trackIndex = trackIndex
        self.layout = QVBoxLayout(self)

        # self.labelTrack = QLabel(f"Track {trackIndex + 1}")
        # self.layout.addWidget(self.labelTrack)

        self.layoutTime = QHBoxLayout()
        self.labelTime = QLabel("Time Offset:")
        self.timeOffsetSpinbox = QSpinBox()
        self.timeOffsetSpinbox.setRange(0, 127)
        self.timeOffsetSpinbox.setValue(5)
        self.layoutTime.addWidget(self.labelTime)
        self.layoutTime.addWidget(self.timeOffsetSpinbox)
        self.layout.addLayout(self.layoutTime)

        self.layoutDuration = QHBoxLayout()
        self.labelDuration = QLabel("Duration Offset:")
        self.durationSpinbox = QSpinBox()
        self.durationSpinbox.setRange(0, 127)
        self.durationSpinbox.setValue(5)
        self.layoutDuration.addWidget(self.labelDuration)
        self.layoutDuration.addWidget(self.durationSpinbox)
        self.layout.addLayout(self.layoutDuration)

        self.layoutVelocity = QHBoxLayout()
        self.labelVelocity = QLabel("Velocity Offset:")
        self.velocitySpinbox = QSpinBox()
        self.velocitySpinbox.setRange(0, 127)
        self.velocitySpinbox.setValue(10)
        self.layoutVelocity.addWidget(self.labelVelocity)
        self.layoutVelocity.addWidget(self.velocitySpinbox)
        self.layout.addLayout(self.layoutVelocity)

        self.layoutDurationPrecentage = QHBoxLayout()
        self.labelDurationPercentage = QLabel("Duration Percentage:")
        self.durationPrecentageSpinbox = QDoubleSpinBox()
        self.durationPrecentageSpinbox.setRange(0.0, 100.0)
        self.durationPrecentageSpinbox.setValue(15.0)
        self.layoutDurationPrecentage.addWidget(self.labelDurationPercentage)
        self.layoutDurationPrecentage.addWidget(self.durationPrecentageSpinbox)
        self.layout.addLayout(self.layoutDurationPrecentage)
        self.layout.addItem(QSpacerItem(0,0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def getParams(self) -> dict:
        return {
            "timeRange" : self.timeOffsetSpinbox.value(),
            "durationRange": self.durationSpinbox.value(),
            "velocityRange": self.velocitySpinbox.value(),
            "durationPrecent": self.durationPrecentageSpinbox.value()
        }

class Ui_MainWindow(object):
    def setupUi(self, MainWindow: QMainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(350, 210)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelFilePath = QLabel(self.centralwidget)
        self.labelFilePath.setObjectName(u"labelFilePath")
        self.horizontalLayout.addWidget(self.labelFilePath)

        self.lineEditFilePath = QLineEdit(self.centralwidget)
        self.lineEditFilePath.setObjectName(u"lineEditFilePath")

        self.pushButtonSelectFile = QPushButton(self.centralwidget)
        self.pushButtonSelectFile.setObjectName(u"pushButtonSelectFile")

        self.horizontalLayout.addWidget(self.lineEditFilePath)
        self.horizontalLayout.addWidget(self.pushButtonSelectFile)
        self.verticalLayout.addLayout(self.horizontalLayout)
        
        self.tabWidgetTracks = QTabWidget(self.centralwidget)
        self.tabWidgetTracks.setObjectName(u"tabWidgetTracks")

        self.pushButtonHumanize = QPushButton(self.centralwidget)
        self.pushButtonHumanize.setDisabled(True)
        self.pushButtonHumanize.setObjectName(u"pushButtonHumanize")

        self.verticalLayout.addWidget(self.tabWidgetTracks)
        self.verticalLayout.addWidget(self.pushButtonHumanize)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
    
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("MIDI Humanizer")
        self.labelFilePath.setText("File")
        self.pushButtonSelectFile.setText("Select file")
        self.pushButtonHumanize.setText("Process MIDI")

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.pushButtonSelectFile.clicked.connect(self.selectFile)
        self.lineEditFilePath.textChanged.connect(self.loadTracks)
        self.pushButtonHumanize.clicked.connect(self.startProcessing)

        self.trackWidgets = []
    
    def loadTracks(self, filepath):
        try:
            self.tabWidgetTracks.clear()
            self.trackWidgets.clear()
            self.pushButtonHumanize.setEnabled(False)
            if not (path.exists(filepath) and path.isfile(filepath)):
                return
            mid: MidiFile = MidiFile(filepath)
            for index, track in enumerate(mid.tracks):
                valid_track = False
                for msg in track:

                    # Checks if the track has midi notes
                    if (str(msg).find("note_on") != -1) or (str(msg).find("note_off") != -1):
                        valid_track = True
                        break
                if valid_track:
                    trackWidget = TrackSettingsWidget(index)
                    self.trackWidgets.append(trackWidget)
                    self.tabWidgetTracks.addTab(trackWidget, track.name if track.name != "" else f"Track {index + 1}")
            self.pushButtonHumanize.setEnabled(True)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Unable to load MIDI: {e}")
    
    def selectFile(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Select MIDI file", "", "MIDI files (*.mid *.midi);;All files (*)")
        if filepath:
            self.lineEditFilePath.setText(filepath)

    def startProcessing(self):
        inputPath = self.lineEditFilePath.text()
        if not inputPath:
            QMessageBox.warning(self, "Error", "No file selected!")
            return
        
        try:
            mid = MidiFile(inputPath)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Unable to load MIDI: {e}")
            return
        
        trackParams = {}
        for widget in self.trackWidgets:
            trackParams[widget.trackIndex] = widget.getParams()
        
        try:
            midi = LogicHandler.humanizeMidi(mid, trackParams)
            outputPath = f"{path.splitext(inputPath)[0]}_humanized.mid"
            midi.save(outputPath)
            QMessageBox.information(self, "Success", f"Humanizing MIDI successfuly completed!\nNew MIDI saved by path: {outputPath}")
            self.tabWidgetTracks.clear()
            self.lineEditFilePath.clear()
            self.pushButtonHumanize.setDisabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error while processing MIDI: {e}")