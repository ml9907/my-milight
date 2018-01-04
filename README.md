# my-milight

A simple easy-to-integrate with ha-bridge - and therefore Google home / Amazon
eco - milight v6 bridge controller python script

<h2>Usage</h2>

python my-milight.py [-h] -c CMD [-b BRIGHTNESS] [-s SATURATION] [-o COLOR] -z ZONE

required arguments:

-c CMD, --cmd CMD     ON,OFF,BRI,SAT,COLOR,WHITE

-z ZONE, --zone ZONE Value of ZONE (1,2,3,4, 0 means all, 5 means bridge)

optional arguments:

  -h, --help            show this help message and exit
  
  -b BRIGHTNESS, --brightness BRIGHTNESS Value of brightess percent
  
  -s SATURATION, --saturation SATURATION Value of saturation percent
  
  -o COLOR, --color COLOR Value of color
  
Based on: https://stackoverflow.com/questions/42535502/problems-with-sending-udp-packets-milight-limitlessled/  

          http://www.limitlessled.com/dev/
