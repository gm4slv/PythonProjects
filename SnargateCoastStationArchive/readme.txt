Wire2waves DSC Coast Station : GMDSS DSC Coast Station server and client

    Copyright (C) 2015  John Pumford-Green

Wire2waves Ltd : 7 June 2015

                          Wire2waves DSC Coast Station Server

  What is it?
  -----------

  The Coast Station Server provides automated GMDSS DSC Test responses on the
  MF and HF Marine DSC frequencies using a single HF transceever and one or
  more receivers which may be remotely located. The software is written in 
  Python 2.7 and will run under Windows or Linux. Remote receivers send their
  decoded DSC messages via UPD/IP to the Server which inspects each message
  and replies automatically, changing transmit frequency accordingly.
  
  Automatic conversion of MMSI into Ship Name and Callsign is performed, where 
  possible, for logging.
  
  All messages handled by the Server are logged using SQLite and also plain
  text files. 
  
  A TCP/IP inerface is built into the Server for remote administration, and a 
  Python TKinter graphical client is provided for this purpose. The Remote Admin
  client includes server failure detection and Sysop email alerting.
  
  An example Coast Station installation consists of a single Icom HF transceiver, 
  model IC-7200 is preferred, along with the necessary antenna and antenna
  tuning unit and a Windows or Linux PC. A remote-receiver message feed can
  be provided from an existing network of volunteer receiving stations, and 
  can be extended with the user's own receiver installations.
  
  Each receiver requires a recent (> 1.7) version of YaDD which can be provided
  by the author or obtained from its author (see Credits for details).

  The Latest Version
  ------------------

  The latest Client version is v0.9 pre 5
  The latest server version is v0.9 pre 7

  File Manifest
  -------------
  
  README.TXT
  LICENSE.TXT
  GPL.TXT
  w2w_coast_server.py
  coast_sql.py
  dsc_functions.py
  new_coast_dict.py
  radio_functions.py
  resolve.py
  w2w_client.py
  
  
  w2w_client.exe
  
  Documentation
  -------------

  Under construction

  Installation
  ------------

  Contact the developer for assistance.
  
  Credits and Thanks
  ------------------
  
  Dirk Claessens for YaDD / Yet Another DSC Decoder
  Bill Lionheart for the Continuous-Phase Frequency Modulator function
  Richard Ware for testing and provision of receive DSC data
  YaDDNet contributors http://gm4slv.plus.com:8000 for DSC data
  Roger Taylor of GMDSS Training for the initial motive

  Licensing
  ---------

  Please see the file called LICENSE.TXT
  
  Contact
  -------
  
  John Pumford-Green
  Wire2waves Ltd
  john@wire2waves.co.uk
  +44(0)7717 433441
  