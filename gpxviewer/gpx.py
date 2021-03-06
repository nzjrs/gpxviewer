#
#  gpx.py - Used to hold gpx files for access by other scripts
#
#  Copyright (C) 2009 Andrew Gee
#
#  GPX Viewer is free software: you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the
#  Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  GPX Viewer is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License along
#  with this program.  If not, see <http://www.gnu.org/licenses/>.

#
#  If you're having any problems, don't hesitate to contact: andrew@andrewgee.org
#

from datetime import *
from gpximport import *
from math import sqrt, radians, sin, cos, atan2, fabs
from os.path import basename, abspath

def calculate_distance(lat1, lat2, lon1, lon2):
  R = 6371000 #Earth's radius =~ 6371km
  #Haversine formula to work out distance between two lats and lons, using the radius of the world 
  dlat = radians(lat1 - lat2)
  dlon = radians(lon1 - lon2)
  a = fabs((sin(dlat/2) * sin(dlat/2)) + cos(radians(lat1)) * cos(radians(lon2)) * sin(dlon/2) * sin(dlon/2))
  c = 2 * atan2(sqrt(a), sqrt(1-a))
  d = R * c
  
  return d

class GPXTrace:
  def __init__(self,filename):
    self.trace = import_gpx_trace(filename)
        
  def get_points(self):
    tracks = []
    
    for track in self.trace['tracks']:
      segments = []
    
      for segment in track['segments']:
        points = []
        for point in segment['points']:
          points.append((radians(point['lat']),radians(point['lon'])))
        
        segments.append(points)
        
      tracks.append(segments)
    
    return tracks

  def get_display_name(self):
    try:
      return self.trace["metadata"]["name"]
    except KeyError:
      return self.get_filename()
  
  def get_filename(self):
    return basename(self.trace['filename'])

  def get_full_path(self):
    return abspath(self.trace['filename'])
  
  def get_max_lat(self):
    maxlat = self.trace['tracks'][0]['segments'][0]['points'][0]['lat']
    for track in self.trace['tracks']:
      for segment in track['segments']:
        for point in segment['points']:
          if maxlat < point['lat']:
            maxlat = point['lat']
    return maxlat
  
  def get_min_lat(self):
    minlat = self.trace['tracks'][0]['segments'][0]['points'][0]['lat']
    for track in self.trace['tracks']:
      for segment in track['segments']:
        for point in segment['points']:
          if minlat > point['lat']:
            minlat = point['lat']
    return minlat
  
  def get_max_lon(self):
    maxlon = self.trace['tracks'][0]['segments'][0]['points'][0]['lon']
    for track in self.trace['tracks']:
      for segment in track['segments']:
        for point in segment['points']:
          if maxlon < point['lon']:
            maxlon = point['lon']
    return maxlon
  
  def get_min_lon(self):
    minlon = self.trace['tracks'][0]['segments'][0]['points'][0]['lon']
    for track in self.trace['tracks']:
      for segment in track['segments']:
        for point in segment['points']:
          if minlon > point['lon']:
            minlon = point['lon']
    return minlon
    
  def get_centre(self):
    maxlat = self.get_max_lat()
    minlat = self.get_min_lat()
    maxlon = self.get_max_lon()
    minlon = self.get_min_lon()
    
    return (maxlat+minlat)/2,(maxlon+minlon)/2
    
  def get_average_speed(self):
    dt = 0
    seconds = 0

    for track in self.trace['tracks']:
      for segment in track['segments']:
        pointp = None
        for point in segment['points']:
          if pointp != None:
            d = calculate_distance(point['lat'], pointp['lat'], point['lon'], pointp['lon'])
    
            #Add distance to total
            dt = dt + d
    
          pointp = point
        seconds = seconds + (pointp['time'] - segment['points'][0]['time']).seconds
      
  
    return round(dt/seconds,2)
  
  def get_distance(self):
    dt = 0

    for track in self.trace['tracks']:
      for segment in track['segments']:
        pointp = None
        for point in segment['points']:
          if pointp != None:
            d = calculate_distance(point['lat'], pointp['lat'], point['lon'], pointp['lon'])
            #Add distance to total
            dt = dt + d
        
          pointp = point
  
    return dt
    
  def get_duration(self):
    seconds = 0

    for track in self.trace['tracks']:
      for segment in track['segments']:
        seconds = seconds + (segment['points'][len(segment['points'])-1]['time'] - segment['points'][0]['time']).seconds
    
    return seconds
    
  def get_gpxfrom(self):
    fromtime = datetime.now()
    
    fromtime = self.trace['tracks'][0]['segments'][0]['points'][0]['time']

    return fromtime

  def get_gpxto(self):
    totime = datetime.now()
      
    totime = self.trace['tracks'][-1]['segments'][-1]['points'][-1]['time']

    return totime
  
  def get_maximum_speed(self):
    mspeed = 0

    for track in self.trace['tracks']:
      for segment in track['segments']:
        pointp = None
        for point in segment['points']:
          if pointp != None:
            d = calculate_distance(point['lat'], pointp['lat'], point['lon'], pointp['lon'])
            t = (point['time'] - pointp['time']).microseconds + ((point['time'] - pointp['time']).seconds * 1000000)
            if t > 0:
              s = (d/t)*1000000  
              if s > mspeed:
                mspeed = s
    
          pointp = point

    return round(mspeed,2)

