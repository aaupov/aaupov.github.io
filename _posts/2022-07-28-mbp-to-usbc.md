---
layout: post
title: "Using MacBook Pro Early 2015 with LG Ultrafine 4k 22in"
date: 2022-07-28
comments: true
---
# Preface: how the COVID pandemic got me a new monitor
I think I don't need to explain how the switch to WFH got me thinking about investing in a good monitor and a reasonably ergonomic work space at home.
It affected my productivity big time when I had to switch from the full-sized keyboard and a 24" monitor holding two vim panes to a laptop keyboard 
and a 15" screen. But at the same time, I got used to a crisp hi-dpi Retina display of the work laptop.

The search for the perfect display got me here: [Pixel Density Display Listing](https://pixensity.com/list/desktop/).
From that chart, I decided that I need LG Ultrafine 4k with a 22-inch display, which is:
- the highest PPI 4K monitor available,
- is a reasonably-sized display and not a 27" monster like Ultrafine 5K,
- doesn't cost much nowadays as it was discontinued in favor of lower-ppi display.

So I ended up hunting for that display on Ebay and Facebook Marketplace and got my hands on it shortly after.

# LG Ultrafine 4K is a great USB-C monitor
That's all I want to say about the monitor itself – the resolution is great, it works well with USB-C laptops, and it has a Power Delivery feature which
reduces cable clutter. The biggest downside is that it suffers from burn-out on edges, but that's the trade-off I'm willing to accept.

# Using Thunderbolt 2/mini-DisplayPort MBP with USB-C monitor
However, I got my personal old MacBook Pro (Early 2015) that I wanted to connect to the monitor as I occasionally use it too.
This MBP'15 is equipped with Thunderbolt 2/mini-DisplayPort and HDMI outputs.
The issue with HDMI out on this laptop is that it can only 
[drive 4K at 30Hz](https://support.apple.com/kb/sp715?locale=en_US#:~:text=adapters%20(sold%20separately)-,HDMI%20video%20output,-Support%20for%201080p), 
which is insufficient.

The problem is that the monitor is USB-C only, and doesn't feature any other input ports. So I ended up looking for 
a TB2/mini-DP in, USB-C out cable or adapter, but couldn't find it on Amazon or elsewhere. I ordered several combinations of cables but nothing worked.

Months later I was on a lookout for the solution and stumbled upon this comprehensive post in Dan S. Charlton's Tech Blog: 
[Bi-directional DisplayPort->USB-C, HDMI->USB-C, and HDMI->DP cables](https://dancharblog.wordpress.com/2020/05/10/bi-directional-usbc-dp-cables/)

# The final combination that worked
1. Short AmazonBasics UTC-DP-B-L DP1.2 <–> USB-C cable
2. Cable Matters 8K Mini DP to DP 1.4 Adapter

# Making it easy to switch laptops without replugging the monitor cable
And since the monitor's input USB-C connector is so fragile, I didn't want to plug and unplug cables every time when switching between laptops.
The solution that I ended up with is to
1. keep USB-C to USB-C cable plugged in the monitor all the time,
2. when using USB-C mac, just use that cable,
3. when using TB2/mini-DP mac, attach Cellularize USB C Female to Female Adapter and then the final combo.

Hope this little note helps other users of this combination of monitor and laptops!
