import sys
import json
from escpos.printer import Usb
print ("Got arguments: ", sys.argv)
print ("Got arguments: ", sys.argv[1])
dic=json.loads(sys.argv[1])
name = dic["name"]
pnr = dic["pnr"]
flight = dic["flight"]
p = Usb(0x0456, 0x0808, in_ep=0x81, out_ep=0x03)
p.text("Baggage Tag\n")
p.text("Name "+name+"\n")
p.barcode(pnr, 'code39', 64, 2, '', '')
p.cut()
