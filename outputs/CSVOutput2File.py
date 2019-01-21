import PluginLoader
import os
from datetime import datetime


class CSVOutput(PluginLoader.Plugin):
    """Outputs the data from the inverter logger to stdout in csv format"""

    def process_message(self, msg):
        """Output the information from the inverter to stdout in csv format.

        Args:
            msg (InverterMsg.InverterMsg): Message to process
        """
        if (self.config.getboolean('csv', 'daily_file')):
            csvfilename = datetime.now().strftime("%Y-%m-%d") + "_" + self.config.get('csv', 'csv_file_name')
        else:
            csvfilename = self.config.get('csv', 'csv_file_name')

        if (not os.path.exists(csvfilename)) & (not self.config.getboolean('csv', 'disable_header')):
            file = open(csvfilename, 'w')
            file.write ("DateTime,ID,Temp,VPV1,VPV2,VPV3,IPV1,IPV2,IPV3,IAC1,IAC2,IAC3," \
                  "VAC1,VAC2,VAC3,FAC1,PAC1,FAC2,PAC2,FAC3,PAC3," \
                  "ETODAY,ETOTAL,HTOTAL\n")
        else:
            file = open(csvfilename, 'a')

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M');
        file.write (("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}," +
               "{10},{11},{12},{13},{14},{15},{16},{17},{18},{19}," +
               "{20},{21},{22},{23}\n")\
            .format(timestamp, msg.id, msg.temperature,
                    msg.v_pv(1), msg.v_pv(2), msg.v_pv(3),
                    msg.i_pv(1), msg.i_pv(2), msg.i_pv(3),
                    msg.i_ac(1), msg.i_ac(2), msg.i_ac(3),
                    msg.v_ac(1), msg.v_ac(2), msg.v_ac(3),
                    msg.f_ac(1), msg.p_ac(1),
                    msg.f_ac(2), msg.p_ac(2),
                    msg.f_ac(3), msg.p_ac(3),
                    msg.e_today, ((((msg.e_today*10)-(int(msg.e_today*10)))/10)+msg.e_total), msg.h_total))
