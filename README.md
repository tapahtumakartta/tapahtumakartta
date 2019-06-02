# Tapahtumakartta
Backend and web interface for the event map

![front page](https://i.imgur.com/lDrKsYm.png)

## Requirements specification
The interface consits of two main parts
* editor panel
* user view  
  
The two parts have their own web pages which users use to interact with the backend server program.

### Different views

#### Editor panel
Editors (or admins) are users who have have created a map or have been given an access to edit an already created map.
Map creators are given a special link they can use to access the editor panel to make changes to even maps. The link
contains a hash string that is used for authenticating the user thus making the link itself private. Due to the nature
of the system and the data stored, this level of authentication is considered sufficient.

#### User view
Map creators are given another link on map creation. This link is used for accessing the map and interacting with it
but users who are given this link can not make changes.

### Map
Leaflet.py is used as the mapping platform. Both editors and users will interact with Leaflet either by adding points to it
or viewing the data applied into the map. OpenStreetMap will be embedded into the Leaflet mapper and used as the map grapher.

### Features
- Editable markers
- Search bar
- Link generator
- Live user location
- Info page for each map
- Clicking on a marker opens up a popup for user
- Clicking on a marker opens up an editing view for admin
- Automatically get the latest data from the backend

## API URLs
/new_map: saves the provided data into a file and returns hashes for accessing and editing the map  
 params: q - json string with marker data

## Dependencies

### Backend
* Flask: for setting up a REST API

### Frontend
* Leaflet.py
* Google Fonts  
