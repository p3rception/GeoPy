import os
import sys
import dpkt
import socket
import pygeoip
import requests
from webbrowser import open_new_tab as browser

# The database used for IP address translation into GeoLocation
# Got it from https://github.com/mbcc2006/GeoLiteCity-data/tree/master
db = pygeoip.GeoIP('GeoLiteCity.dat')

def get_public_ip():
   try:
      response = requests.get('https://ipinfo.io/json')
      data = response.json()
      return data['ip']
   except Exception as e:
      print(f"Error getting public IP: {e}")
      return None

def retKML(dstip, srcip):
   dst = db.record_by_name(dstip)
   src = db.record_by_name(srcip)
   try:
      dstlongitude = dst['longitude']
      dstlatitude = dst['latitude']
      srclongitude = src['longitude']
      srclatitude = src['latitude']
      kml = (
         '<Placemark>\n'
         '<name>%s</name>\n'
         '<extrude>1</extrude>\n'
         '<tessellate>1</tessellate>\n'
         '<styleUrl>#anyName</styleUrl>\n'
         '<LineString>\n'
         '<coordinates>%6f,%6f\n%6f,%6f</coordinates>\n'
         '</LineString>\n'
         '</Placemark>\n'
      )%(dstip, dstlongitude, dstlatitude, srclongitude, srclatitude)
      return kml
   except:
      return ''

def plotIPs(pcap, src):
   kmlPts = ''
   for (ts, buf) in pcap:
      try:
         eth = dpkt.ethernet.Ethernet(buf)
         ip = eth.data
         # src = socket.inet_ntoa(ip.src)
         dst = socket.inet_ntoa(ip.dst)
         KML = retKML(dst, src)
         kmlPts = kmlPts + KML
      except:
         pass
   return kmlPts

def main():
   if len(sys.argv) != 2:
      print("Usage: python main.py <pcap_file>")
      return
   
   public_ip = get_public_ip()
   if not public_ip:
      print("Could not determine public IP. Exiting.")
      return
   
   # pcap_file = 'test.pcap'
   pcap_file = sys.argv[1]
   pcap_name, pcap_ext = os.path.splitext(pcap_file)

   f = open(pcap_file, 'rb') # Open in binary format
   pcap = dpkt.pcap.Reader(f)
   kmlheader = '<?xml version="1.0" encoding="UTF-8"?> \n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'\
   '<Style id="anyName">' \
               '<LineStyle>' \
               '<width>2</width>' \
               '<color>934bc7</color>' \
               '</LineStyle>' \
               '</Style>'
   kmlfooter = '</Document>\n</kml>\n'
   kmldoc = kmlheader + plotIPs(pcap, public_ip) + kmlfooter

   output_filename = f"map-{pcap_name}.kml"

   with open(output_filename, 'w') as kml_file:
      kml_file.write(kmldoc)
   print(f'The output has been saved to {output_filename}')
   print('Upload it to https://www.google.com/mymaps to see the results.')
   
   open_in_browser = input('Do you want to open mymaps in a new browser tab? (y/N): ').lower().strip()
   if open_in_browser == 'y':
      browser('https://www.google.com/mymaps')

if __name__ == '__main__':
   main()