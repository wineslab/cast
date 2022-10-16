#! /bin/bash
source /opt/fpga/usrp3/top/x300/setupenv.sh
viv_jtag_program /usr/share/uhd/images/usrp_x310_fpga_HG.bit
