# EDNA - European Dosimetry Network aboard Aircraft

Software basement for the network of radiation measurements using various types of dosemeters, ready for inter-comparison especially for the case of extreme solar event or atmospheric discharge event.

Current database CR10 available online at http://bobr.ujf.cas.cz/~aircraft/CR10/ was prepared by a PhD student by means of SOCIS project. The database is limited to one device (Liulin). Our aim is to extend the database also for other types of dosemeters, including passive TLDs.

## Features 

- Web based form for upload the measured and flight-track data to the system
- Tools for merging dosimetry and flight-track data from all types of used devices
- Tools for visualisation of data measured aboard aircraft and at Lomnicky stit Neutron monitor
- Tool for measured data corrections and filtering
- Web access for public to measured data

There are CGI Python 2.7 scripts programmed in Django API for maintainance of SQL database for measurement metadata. The scripts provide possibility to upload and download measurement data, as well as metadata about sensors, calibration and measured quantities.

The system is expandable with ability to upload new plug-ins for evaluation of data from various new detectors in future. Current version is capable to merge data from Liulin detector together with XML GPS report from Czech airlines.

EDNA accepts plug-ins containing visualization scripts written in Python 2.7. There are sample scripts for creation of simple graphics from the Liulin-GPS data.

All the data are organized with respect to date and time. The measurement data can be connected to sets called "Expedition" in order to group measurements from different aircrafts, ground stations etc.

The database is accessible for download and visualization to non-registred users. Registred users are further allowed to upload data or sensors and visualization plug-ins.

The current version is deployed to www.edna.ujf.cas.cz

Technologies involved: Python, Django, Bootstrap, Pandas, NumPy
