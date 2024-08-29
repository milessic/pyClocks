---
layout: post
title: "Version 1.1 is here!"
date:   2024-08-29 15:00:00 +0200
categories: release
---
Version v1.1 is here!

The goal of `v1.1` was to make app better looking, easier to use and to consume less resources.

App writes much less data into disk right now. Version ``v1.0`` was writing ``around 80kb/second``, while version ``v1.1`` is writing ``around 2kbs/second`` with default settings. Additionally, it consumes ``70% RAM`` less with more features (tested on Ubuntu with KDE Plasma).

### Release notes
#### General features
- added option to not run app as Tool
- added version information to the application

#### App is more responsive
- added minimum widht for each timer
- made main area scrollable
- add app resize when using custom topnav

#### Appearance
- redesigned edit screen
- add + button to no-timers-panel

#### Save improvements
- app doesn't save while edit mode is enabled
- app force saves on close
- saving interval is cusomizable

#### Fixes
- nerdfonts may not be displayed correctly #4

[Go to downloads][downloads]

[downloads]: /pyClocks/downloads
