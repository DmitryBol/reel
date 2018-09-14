import ntpath


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def isint(value):
    try:
        int(value)
        return int(value)
    except ValueError:
        return -1


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def float_validate(self, bot, top):
    sender = self.sender()
    if str(sender.text()) != '':
        try:
            if not bot <= float(sender.text()) <= top:
                raise ValueError
            sender.setStyleSheet('')
        except ValueError:
            sender.setStyleSheet('QLineEdit {background-color: #f6989d;}')
    else:
        sender.setStyleSheet('')


def int_validate(self, bot, top):
    sender = self.sender()
    if str(sender.text()) != '':
        try:
            if not bot <= int(sender.text()) <= top:
                raise ValueError
            sender.setStyleSheet('')
        except ValueError:
            sender.setStyleSheet('QLineEdit {background-color: #f6989d;}')
    else:
        sender.setStyleSheet('')


def string_validate(self):
    sender = self.sender()
    if str(sender.text()) == '' or ';' in str(sender.text()):
        sender.setStyleSheet('QLineEdit {background-color: #f6989d;}')
    else:
        sender.setStyleSheet('')
