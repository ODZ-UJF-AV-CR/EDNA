# EDNA - European Dosimetry Network aboard Aircraft

Software basement for the network of radiation measurements using various types of dosemeters, ready for inter-comparison, especially in the case of extreme solar events or atmospheric discharge events.

Current [database CR10](https://academic.oup.com/rpd/article/186/2-3/224/5618735?login=true) is available online at http://bobr.ujf.cas.cz/~aircraft/CR10/ was prepared by a Ph.D. student by means of SOCIS project. The database is limited to one device (Liulin). Our aim is to extend the database also for other types of dosemeters, including passive TLDs.

## Features 

- Web-based form for uploading the measured and flight-track data to the system
- Tools for merging dosimetry and flight-track data from all types of used devices
- Tools for visualization of data measured aboard aircraft and at Lomnicky stit Neutron monitor
- Tool for measured data corrections and filtering
- Web access for the public to measure data

There are CGI Python 2.7 scripts programmed in Django API for maintenance of SQL database for measurement metadata. The scripts provide the possibility to upload and download measurement data, as well as metadata about sensors, calibration, and measured quantities.

The system is expandable with the ability to upload new plug-ins for the evaluation of data from various new detectors in the future. The current version is capable to merge data from the Liulin detector together with XML GPS reports from Czech airlines.

EDNA accepts plug-ins containing visualization scripts written in Python 2.7. There are sample scripts for the creation of simple graphics from the Liulin-GPS data.

All the data are organized with respect to date and time. The measurement data can be connected to sets called "Expedition" in order to group measurements from different aircraft, ground stations, etc.

The database is accessible for download and visualization to non-registered users. Registered users are further allowed to upload data or sensors and visualization plug-ins.

The current version is deployed to www.edna.ujf.cas.cz

Technologies involved: Python, Django, Bootstrap, Pandas, NumPy


## Related documents

  * [European Dosimetry Network aboard Aircraft (EDNA) slides](https://docs.google.com/presentation/d/1MtXrfd3f4mMmrlZ84HuAUgjUKm84PMN8U536UpBLaLY/edit?usp=sharing)

