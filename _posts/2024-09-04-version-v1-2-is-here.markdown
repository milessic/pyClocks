---
layout: post
title: "Version 1.2 is here!"
date:   2024-09-04 10:00:00 +0200
categories: release
---
Version v1.2 is here!

The goal of `v1.2` was to improve app appearance and responsiveness.

It was achived by implementing ``App Themes`` which are accessible from ``Settings`` and named ``App look``.
Additionally, app now auto-adjust it's size to fit all the clocks that can fit the screen :) In case the clocks won't fit screen, scroller will go with the help. Of course user can still adjust size of the app manually.

Aparat of that ``always-on-top`` option was added, also available from ``Settings``

<img src="/pyClocks/assets/v1_2_demo.png" alt="v1.2"></img>

### Release notes
#### General features
- Added always-on-top option (available from options)

#### App is more responsive
- Added minimum width for each timer
- Made main area scrollable
- Add app resize when using custom topnav

#### Appearance
- Made app as wide to fit all user's clocks by default
- Removed this little borders that were visible in light mode 
- Made edit mode not flicker due to button hiding
- Corrected separator placement in system tray 

#### Fixes
- [Grip points don't work on Windwos #7][issue4]
- [App doesn't load when clock file is corrupted #8][issue8]

[Go to downloads][downloads]

[downloads]: /pyClocks/downloads
[issue7]: https://github.com/milessic/pyClocks/issues/7
[issue8]: https://github.com/milessic/pyClocks/issues/8

