from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from itertools import count, islice


class Threaded(QObject):
    result = pyqtSignal(int)

    def __init__(self):
        super(Threaded, self).__init__()

    @pyqtSlot(int)
    def calculate_prime(self, n):
        primes = (n for n in count(2) if all(n % d for d in range(2, n)))
        self.result.emit(list(islice(primes, 0, n))[-1])


class GUI(QWidget):
    requestPrime = pyqtSignal(int)

    def __init__(self):
        super(GUI, self).__init__()

        self._thread = QThread()
        self._threaded = Threaded()
        self._threaded.result.connect(self.display_prime)
        self.requestPrime.connect(self._threaded.calculate_prime)
        self._threaded.moveToThread(self._thread)
        qApp.aboutToQuit.connect(self._thread.quit)
        self._thread.start()

        fon = QVBoxLayout(self)
        self._iterationLE = QLineEdit()
        self._iterationLE.setPlaceholderText('Iteration (n)')
        fon.addWidget(self._iterationLE)
        self._requestBtn = QPushButton('Calculate Prime')
        self._requestBtn.clicked.connect(self.prime_requested)
        fon.addWidget(self._requestBtn)
        self._busy = QProgressBar(self)
        fon.addWidget(self._busy)
        self._resultLbl = QLabel("Result:", self)
        fon.addWidget(self._resultLbl)

    @pyqtSlot()
    def prime_requested(self):
        try:
            n = int(self._iterationLE.text())
        except:
            return
        self.requestPrime.emit(n)
        self._busy.setRange(0, 0)
        self._iterationLE.setEnabled(False)
        self._requestBtn.setEnabled(False)

    @pyqtSlot(int)
    def display_prime(self, prime):
        self._resultLbl.setText("Result: {}".format(prime))
        self._busy.setRange(0, 100)
        self._iterationLE.setEnabled(True)
        self._requestBtn.setEnabled(True)


if __name__ == "__main__":
    from sys import exit, argv

    a = QApplication(argv)
    g = GUI()
    g.show()
    exit(a.exec_())
