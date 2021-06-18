import sys

from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.flowchart import Flowchart

from activity_model import ActivityModel
from node_constants import NodeType, NodeInputOutputType
from gesture_node import GestureNode
from custom_nodes import FeatureExtractionFilterNode, DisplayTextNode
from DIPPID_pyqtnode import BufferNode, DIPPIDNode

# TODO add if removed after automatic code refactoring
# from gesture_node import GestureNode
# from custom_nodes import FeatureExtractionFilterNode, DisplayTextNode
# from DIPPID_pyqtnode import BufferNode, DIPPIDNode

"""
The workload was distributed evenly and tasks were discussed together.

# start program example:
# python3 activity_recognizer.py 5700
"""


# Author: Claudia
# Reviewer: Martina
class MainWindow(QtWidgets.QWidget):

    def __init__(self, port_number=None):
        super(MainWindow, self).__init__()

        self.__model = ActivityModel(port_number)

        self.__setup_flowchart()
        self.__setup_main_window()

    def __setup_main_window(self):
        self.setWindowTitle("Activity Recognizer")
        self.move(QtWidgets.qApp.desktop().availableGeometry(
            self).center() - self.rect().center())
        # TODO

    def __setup_flowchart(self):
        self.__flow_chart = Flowchart(terminals={})
        self.__layout = QtGui.QGridLayout()
        self.__layout.addWidget(self.__flow_chart.widget(), 0, 0, 2, 1)

        self.__setup_dippid()
        self.__setup_buffers()
        self.__setup_feature_extraction_filter()
        self.__setup_gesture()
        self.__setup_display_text()

        self.setLayout(self.__layout)

    def __setup_dippid(self):
        self.__dippid_node = self.__flow_chart.createNode(NodeType.DIPPID.value, pos=(0, 0))
        self.__dippid_node.set_port(self.__model.get_port_number())

    def __setup_buffers(self):
        self.__setup_buffer_x()
        self.__setup_buffer_y()
        self.__setup_buffer_z()

    def __setup_buffer_x(self):
        self.__buffer_node_x = self.__flow_chart.createNode(NodeType.BUFFER.value, pos=(150, -100))
        self.__flow_chart.connectTerminals(self.__dippid_node[NodeInputOutputType.ACCEL_X.value],
                                           self.__buffer_node_x[NodeInputOutputType.DATA_IN.value])

    def __setup_buffer_y(self):
        self.__buffer_node_y = self.__flow_chart.createNode(NodeType.BUFFER.value, pos=(150, 0))
        self.__flow_chart.connectTerminals(self.__dippid_node[NodeInputOutputType.ACCEL_Y.value],
                                           self.__buffer_node_y[NodeInputOutputType.DATA_IN.value])

    def __setup_buffer_z(self):
        self.__buffer_node_z = self.__flow_chart.createNode(NodeType.BUFFER.value, pos=(150, 100))
        self.__flow_chart.connectTerminals(self.__dippid_node[NodeInputOutputType.ACCEL_Z.value],
                                           self.__buffer_node_z[NodeInputOutputType.DATA_IN.value])

    def __setup_feature_extraction_filter(self):
        self.__feature_extraction_filter_node = self.__flow_chart.createNode(NodeType.FEATURE_EXTRACTION_FILTER.value,
                                                                             pos=(300, -75))

        self.__flow_chart.connectTerminals(self.__buffer_node_x[NodeInputOutputType.DATA_OUT.value],
                                           self.__feature_extraction_filter_node[NodeInputOutputType.ACCEL_X.value])
        self.__flow_chart.connectTerminals(self.__buffer_node_y[NodeInputOutputType.DATA_OUT.value],
                                           self.__feature_extraction_filter_node[NodeInputOutputType.ACCEL_Y.value])
        self.__flow_chart.connectTerminals(self.__buffer_node_z[NodeInputOutputType.DATA_OUT.value],
                                           self.__feature_extraction_filter_node[NodeInputOutputType.ACCEL_Z.value])

    def __setup_gesture(self):
        self.__gesture_node = self.__flow_chart.createNode(NodeType.GESTURE.value,
                                                                        pos=(300, 50))

        # TODO output
        #  self.__flow_chart.connectTerminals(self.__feature_extraction_filter_node["FREQUENCY_SPECTROGRAM"],
        #                                   self.__activity_recognition_node[
        #                                       NodeInputOutputType.sample.value])

    def __setup_display_text(self):
        # TODO + pos
        self.__display_text_node = self.__flow_chart.createNode(NodeType.DISPLAY_TEXT.value,
                                                                        pos=(300, 100))
        pass


def start_program():
    port_number = read_port_number()

    app = QtWidgets.QApplication([])
    main_window = MainWindow(port_number)
    main_window.show()

    if (sys.flags.interactive != 1) or not hasattr(QtCore, "PYQT_VERSION"):
        sys.exit(QtWidgets.QApplication.instance().exec_())

    sys.exit(app.exec_())


def read_port_number():
    if len(sys.argv) < 2:
        sys.stderr.write("Please give a port number as argument (￢_￢)\n")
        # sys.exit(1) # TODO uncomment
        return 5700

    return sys.argv[1]


if __name__ == '__main__':
    start_program()
