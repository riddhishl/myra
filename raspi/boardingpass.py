import sys
import json
from escpos.printer import Usb
print ("Got arguments: ", sys.argv)
print ("Got arguments: ", sys.argv[1])
dic=json.loads(sys.argv[1])
name = dic["name"]
destination = dic["destination"]
flight = dic["flight"]
carrier = dic["carrier"]
gate = dic["gate"]
pnr = dic["pnr"]
seat = dic["seat"]
p = Usb(0x0456, 0x0808, in_ep=0x81, out_ep=0x03)
p.text("Boarding Pass\n")
p.text("Name "+name+"\n")
p.text("Carrier "+carrier+"\n")
p.text("To "+destination+"\n")
p.text("Gate "+gate+"\n")
p.text("Seat "+seat+"\n")
p.barcode(flight, 'code39', 64, 2, '', '')
p.cut()
