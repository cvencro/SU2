#!/usr/bin/env python 

## \file finite_differences.py
#  \brief Python script for doing the finite differences computation using the SU2 suite.
#  \author F. Palacios
#  \version 5.0.0 "Raven"
#
# SU2 Original Developers: Dr. Francisco D. Palacios.
#                          Dr. Thomas D. Economon.
#
# SU2 Developers: Prof. Juan J. Alonso's group at Stanford University.
#                 Prof. Piero Colonna's group at Delft University of Technology.
#                 Prof. Nicolas R. Gauger's group at Kaiserslautern University of Technology.
#                 Prof. Alberto Guardone's group at Polytechnic University of Milan.
#                 Prof. Rafael Palacios' group at Imperial College London.
#                 Prof. Edwin van der Weide's group at the University of Twente.
#                 Prof. Vincent Terrapon's group at the University of Liege.
#
# Copyright (C) 2012-2017 SU2, the open-source CFD code.
#
# SU2 is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# SU2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with SU2. If not, see <http://www.gnu.org/licenses/>.

import os, sys
from optparse import OptionParser
sys.path.append(os.environ['SU2_RUN'])
import SU2

# -------------------------------------------------------------------
#  Main 
# -------------------------------------------------------------------

def main():
        
    parser = OptionParser()
    parser.add_option("-f", "--file",       dest="filename",
                      help="read config from FILE", metavar="FILE")
    parser.add_option("-n", "--partitions", dest="partitions", default=1,
                      help="number of PARTITIONS", metavar="PARTITIONS")
    parser.add_option("-q", "--quiet",      dest="quiet",      default='False',
                      help="output QUIET to log files", metavar="QUIET")
    parser.add_option("-z", "--zones", dest="nzones", default="1",
                        help="Number of Zones", metavar="ZONES")

    (options, args)=parser.parse_args()
    options.partitions = int( options.partitions )
    options.quiet      = options.quiet.upper() == 'TRUE'
    options.nzones     = int( options.nzones )

    finite_differences( options.filename   ,
                        options.partitions ,
                        options.quiet      ,
                        options.nzones      )
#: def main()


# -------------------------------------------------------------------
#  Finite Differences Function 
# -------------------------------------------------------------------

def finite_differences( filename           , 
                        partitions = 0     , 
                        quiet      = False ,
                        nzones     = 1      ):
    # Config
    config = SU2.io.Config(filename)
    config.NUMBER_PART = partitions
    config.NZONES      = int( nzones )

    if quiet: 
        config.CONSOLE = 'CONCISE'
    
    # State
    state = SU2.io.State()
    physics = SU2.io.read_physics(config)
    state.find_files(physics)
    
    # Finite Difference Gradients
    SU2.eval.gradients.findiff(config,state)
    
    return state

#: finite_differences()


# -------------------------------------------------------------------
#  Run Main Program
# -------------------------------------------------------------------

# this is only accessed if running from command prompt
if __name__ == '__main__':
    main()
