; single extruder beginning GCODE for a dual extruder Taz 6

G26                          ; clear potential ‘probe fail’ condition
G21                          ; set units to Millimetres
M107                         ; disable fans
G90                          ; absolute positioning
T0                           ; select this extruder first
M82                          ; set extruder to absolute mode
G92 E0                       ; set extruder position to 0
M140 S[first_layer_bed_temperature]; get bed heating up
M104 S170 T0                 ; soften filament
M104 S150 T1                 ; soften filament
G28 X Y                      ; home X and Y
G1 X-19 Y258                 ; move over the Z_MIN switch
M109 R170 T0                 ; wait for T0 to reach temp
M109 R150 T1                 ; wait for T1 to reach temp
G28 Z                        ; home Z
G1 E-30 F100                 ; suck up XXmm of filament
G1 X-17 Y100 F3000           ; move above wiper pad
G1 Z1                        ; push nozzle into wiper
G1 X-19 Y95 F1000            ; slow wipe
G1 X-17 Y90 F1000            ; slow wipe
G1 X-19 Y85 F1000            ; slow wipe
G1 X-17 Y90 F1000            ; slow wipe
G1 X-19 Y80 F1000            ; slow wipe
G1 X-17 Y95 F1000            ; slow wipe
G1 X-19 Y75 F2000            ; fast wipe
G1 X-17 Y85 F2000            ; fast wipe
G1 X-19 Y80 F2000            ; fast wipe
G1 X-17 Y70 F2000            ; fast wipe
G1 X-19 Y75 F2000            ; fast wipe
G1 X-17 Y95 F1000            ; slow wipe
G1 X-19 Y90 F1000            ; slow wipe
G1 X-17 Y85 F1000            ; slow wipe
G1 X-19 Y90 F1000            ; slow wipe
G1 X-17 Y80 F1000            ; slow wipe
G1 X-19 Y95 F1000            ; slow wipe
G1 X-17 Y75 F2000            ; fast wipe
G1 X-19 Y85 F2000            ; fast wipe
G1 X-17 Y80 F2000            ; fast wipe
G1 X-19 Y90 F2000            ; fast wipe
G1 X-17 Y85 F2000            ; fast wipe
G1 Z10                       ; raise extruder
M109 R170                    ; heat to probe temp
G1 X-9 Y-9                   ; move above first probe point
M204 S100                    ; set accel for probing
G29                          ; probe sequence (for auto-leveling)
M204 S500                    ; set accel back to normal
G1 X0 Y0 Z15 F5000           ; get out the way
M400                         ; clear buffer
M140 S[first_layer_bed_temperature]; get bed heating up
M104 S[first_layer_temperature_0] T0 ; set extruder temp
M104 S0 T1                   ; set extruder temp to zero
M109 R[first_layer_temperature_0] T0 ; set extruder temp and wait
M190 R[first_layer_bed_temperature]; get bed temping up during first layer
G92 E-30                     ; adjust E value
G1 Z2 E0 F75                 ; extrude filament back into nozzle
M117 TMDI Printing…         ; LCD status message
