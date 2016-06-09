import sys, math, random
from PyQt4 import QtGui
import numpy as np
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from plotter_GUI import Ui_MainWindow
import mysql.connector

class Main(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)
        self.PlotButton.clicked.connect(self.plot)
        self.ClearButton.clicked.connect(self.clear)
        self.SaveButton.clicked.connect(self.save)
        self.QuitButton.clicked.connect(self.quit)
        self.subjectNo = 0;
        self.filter = 0;
        self.param =0;
        self.fig = plt.figure();
        self.a1 = self.fig.add_subplot(121)
        self.a2 = self.fig.add_subplot(122)
        self.cnx = mysql.connector.connect(user='root',password='neuro',database='mohand');
        self.cursor = self.cnx.cursor();

    def addplot(self):
        self.canvas = FigureCanvas(self.fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()
        self.toolbar = NavigationToolbar(self.canvas, self, coordinates=True)
        self.addToolBar(self.toolbar)

    def rmplot(self):
        self.mplvl.removeWidget(self.canvas)
        self.canvas.close()
        self.mplvl.removeWidget(self.toolbar)
        self.toolbar.close()

    def filterstr(self,x):
        return{
            0: '_fil_',
            1: '_raw_'
            }.get(x)

    def paramstr(self,x):
        return{
            0: 'indexVal',
            1: 'meanReactionTime',
            2: 'meanMovementTime',
            3: 'meanResponseTime',
            4: 'meanMaxVel',
            5: 'meanMaxAcc',
            6: 'meanEPD',
            7: 'meanRealDist',
            8: 'meanTraversedDist',
            9: 'meanPerDev',
            10: 'ovMaxReactionTime',
            11: 'ovMaxMovementTime',
            12: 'ovMaxEPD',
            13: 'ovMaxSpeed',
            14: 'ovMaxAcc'
        }.get(x)

    def daystr(self,x):
        return{
            0: 'baseline',
            1: 'day1',
            2: 'day2',
            3: 'day3',
            4: 'day4',
            5: 'day5'
            }.get(x,'performance')
    
    def plot(self):
        print "plotting graph";
        self.subjectNo = int(self.text_subNo.text());
        self.filter = self.combo_filter.currentIndex();
        self.param = self.combo_param.currentIndex();
        fstr = self.filterstr(self.filter);
        pstr = self.paramstr(self.param);
        rep_data = np.zeros(7);
        ran_data = np.zeros(7);
        for i in range(7):
            s = "select count("+pstr+fstr+"rep) from "+self.daystr(i)+" where subNo="+str(self.subjectNo);
            res=self.cursor.execute(s);
            if(int(self.cursor.fetchone()[0])==1):
                s = "select "+pstr+fstr+"rep from "+self.daystr(i)+" where subNo="+str(self.subjectNo);
                res2 = self.cursor.execute(s);
                rep_data[i] = float(self.cursor.fetchone()[0]);
            s = "select count("+pstr+fstr+"ran) from "+self.daystr(i)+" where subNo="+str(self.subjectNo);
            res=self.cursor.execute(s);
            if(int(self.cursor.fetchone()[0])==1):
                s = "select "+pstr+fstr+"ran from "+self.daystr(i)+" where subNo="+str(self.subjectNo);
                res2 = self.cursor.execute(s);
                ran_data[i] = float(self.cursor.fetchone()[0]);
        self.rmplot();
        
        labels = ['Baseline', 'Day 1', 'Day 2','Day 3','Day 4','Day 5','Performance'];
        self.a1.set_xticklabels(labels);
        self.a2.set_xticklabels(labels);
        self.a1.set_title('Repeated Sequence');
        self.a2.set_title('Random Sequence');
        label_ax = 'Subject '+str(self.subjectNo)+' '+pstr;
        self.a1.plot(rep_data, label=label_ax);
        self.a2.plot(ran_data, label =label_ax);
        leg1 = self.a1.legend(loc='best');
        leg2 = self.a2.legend(loc='best');
        leg1.draggable(state=True);
        leg2.draggable(state=True);
        self.addplot();
        self.sub_info.setText("(Subject Number "+str(self.subjectNo)+")");
        rep_d1_val = int((rep_data[1]-rep_data[0])*100/rep_data[0]);
        self.rep_d1.setText(str(rep_d1_val));
        ran_d1_val = int((ran_data[1]-ran_data[0])*100/ran_data[0]);
        self.ran_d1.setText(str(ran_d1_val));
        rep_d2_val = int((rep_data[2]-rep_data[0])*100/rep_data[0]);
        self.rep_d2.setText(str(rep_d2_val));
        ran_d2_val = int((ran_data[2]-ran_data[0])*100/ran_data[0]);
        self.ran_d2.setText(str(ran_d2_val));
        rep_d3_val = int((rep_data[3]-rep_data[0])*100/rep_data[0]);
        self.rep_d3.setText(str(rep_d3_val));
        ran_d3_val = int((ran_data[3]-ran_data[0])*100/ran_data[0]);
        self.ran_d3.setText(str(ran_d3_val));
        rep_d4_val = int((rep_data[4]-rep_data[0])*100/rep_data[0]);
        self.rep_d4.setText(str(rep_d4_val));
        ran_d4_val = int((ran_data[4]-ran_data[0])*100/ran_data[0]);
        self.ran_d4.setText(str(ran_d4_val));
        rep_d5_val = int((rep_data[5]-rep_data[0])*100/rep_data[0]);
        self.rep_d5.setText(str(rep_d5_val));
        ran_d5_val = int((ran_data[5]-ran_data[0])*100/ran_data[0]);
        self.ran_d5.setText(str(ran_d5_val));
        rep_p_val = int((rep_data[6]-rep_data[0])*100/rep_data[0]);
        self.rep_p.setText(str(rep_p_val));
        ran_p_val = int((ran_data[6]-ran_data[0])*100/ran_data[0]);
        self.ran_p.setText(str(ran_p_val));


    def clear(self):
        self.a1.cla();
        self.a2.cla();
        self.rmplot();
        self.addplot();
        self.text_subNo.setText("");
        self.combo_filter.setCurrentIndex(0);
        self.combo_param.setCurrentIndex(0);
        print "clear";

    def save(self):
        print "save"
        #open a dialog box and input name of figure and then save.
        #plt.savefig('common_labels_text.png', dpi=300)
    
    def quit(self):
        #self.cnx.commit();
        #self.cnx.close();
        exit()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.a1.plot(np.random.rand(5));
    main.a2.plot(np.random.rand(10));
    main.addplot()
    main.show()
    main.clear()
    sys.exit(app.exec_())
