features.json
=============
allowLOS
--------

  ``Line Of Sight. Whether of not units and structures can see through them and shoot at objects behind them``


  default: 1

  choices:
    - 1
    - 0
armour
------

  ``Armour of the feature, similar to armour used on buildings.``


  required: True

  max: 65535
bodyPoints
----------

  ``Hit points.``


  required: True

  max: 65535
breadth
-------

  ``Breadth/length of the feature (z-axis)``


  required: True

  max: 65535
damageable
----------

  ``Whether or not the feature is damagable, if set to 0, the 'x' cursor will appear instead of the 'attack' cursor.``


  default: 1

  choices:
    - 1
    - 0
name
----

  ``Verbose model name.``

pieFile
-------

  ``Pie model of body.``

tileDraw
--------

  ``Breadth/length of the feature (z-axis)``


  required: True

  max: 65535
type
----

  ``Size of the body``


  required: True

  choices:
    - BOULDER
    - BUILDING
    - GENERIC ARTEFACT
    - OIL DRUM
    - OIL RESOURCE
    - SKYSCRAPER
    - TANK WRECK
    - TREE
    - VEHICLE
visible
-------

  ``Whether or not the feature is visible even if you haven't explored that area of terrain yet``


  default: 1

  choices:
    - 1
    - 0
width
-----

  `` Width of the feature (x-axis)``


  required: True

  max: 65535