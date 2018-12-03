# avis_courrier
paper mail delivery notification with USB Camera, running on the embeded Linux Board like Raspberry Pi.

## How to work
1. Put delivered paper mail into the box.
<img src="doc/ss.2018-03-03 13.29.39.png" width="75%">  

2. Push switch
<img src="doc/ss.2018-03-03 13.30.06.png" width="75%">

3. Then, USB Camera in the box take a photo of the mail.
<img src="doc/org.jpg" width="75%">  

4. The photo is transformed by perspective transformation.
<img src="doc/transformed.jpg" width="75%">  

5. Send notify mail with calling [biff](https://github.com/UedaTakeyuki/biff).

## configration

<img src="https://github.com/UedaTakeyuki/biff/blob/master/pic/configration.of.biff&avis_courrier.pages.png">

In above figure, the ***[biff](https://github.com/UedaTakeyuki/biff)*** is a webservice to send notification mail of paper mail delivery.
