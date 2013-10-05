templates.ini
==============
Fields
______
- **available.**
  ???


    max: 65535


- **compBody.**
  Key form :doc:`body`



- **compBrain.**
  Key form :doc:`brain`


    required: True


- **compConstruct.**
  Key form :doc:`construction`


    required: True


- **compPropulsion.**
  Key form :doc:`propulsion`


    required: True


- **compRepair.**
  Key form :doc:`repair`


    required: True


- **compSensor.**
  Key form :doc:`sensor`


    required: True


- **type.**
  ???


    required: True

    choices:
      - DROID
      - CYBORG_SUPER
      - CYBORG_REPAIR
      - CYBORG
      - PERSON
      - TRANSPORTER
      - CYBORG_CONSTRUCT
      - SUPERTRANSPORTER


- **weapons.**
  Coma separated keys rom :doc:`weapons`


