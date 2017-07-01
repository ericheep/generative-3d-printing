; single extruder ending GCODE for a dual extruder Taz 6

M400                           ; wait for moves to finish
M104 S0                        ; hotend off
M107                           ; fans off
G91                            ; relative positioning
G1 E-1 F300                    ; retract the filament a bit before lifting the nozzle, to release some of the pressure
G1 Z+20 E-5 X-20 Y-20 F3000    ; move Z up a bit and retract filament even more
M117 Cooling please wait       ; progress indicator message
G90                            ; absolute positioning
G1 Y0 F3000                    ; move to cooling position
M104 S0                        ; Set Hot-end to 0C (off)
M140 S0                        ; Set bed to 0C (off)
G1 Y280 F3000                  ; present finished print
M84                            ; steppers off
G90                            ; absolute positioning
M117 TMDI Print complete       ; progress indicator message
