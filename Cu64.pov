#include "colors.inc"
#include "finish.inc"

global_settings {assumed_gamma 1 max_trace_level 6}
background {color White}
camera {orthographic
  right -19.73*x up 20.38*y
  direction 1.00*z
  location <0,0,50.00> look_at <0,0,0>}
light_source {<  2.00,   3.00,  40.00> color White
  area_light <0.70, 0, 0>, <0, 0.70, 0>, 3, 3
  adaptive 1 jitter}

#declare simple = finish {phong 0.7}
#declare pale = finish {ambient .5 diffuse .85 roughness .001 specular 0.200 }
#declare intermediate = finish {ambient 0.3 diffuse 0.6 specular 0.10 roughness 0.04 }
#declare vmd = finish {ambient .0 diffuse .65 phong 0.1 phong_size 40. specular 0.500 }
#declare jmol = finish {ambient .2 diffuse .6 specular 1 roughness .001 metallic}
#declare ase2 = finish {ambient 0.05 brilliance 3 diffuse 0.6 metallic specular 0.70 roughness 0.04 reflection 0.15}
#declare ase3 = finish {ambient .15 brilliance 2 diffuse .6 metallic specular 1. roughness .001 reflection .0}
#declare glass = finish {ambient .05 diffuse .3 specular 1. roughness .001}
#declare glass2 = finish {ambient .0 diffuse .3 specular 1. reflection .25 roughness .001}
#declare Rcell = 0.070;
#declare Rbond = 0.100;

#macro atom(LOC, R, COL, TRANS, FIN)
  sphere{LOC, R texture{pigment{color COL transmit TRANS} finish{FIN}}}
#end
#macro constrain(LOC, R, COL, TRANS FIN)
union{torus{R, Rcell rotate 45*z texture{pigment{color COL transmit TRANS} finish{FIN}}}
      torus{R, Rcell rotate -45*z texture{pigment{color COL transmit TRANS} finish{FIN}}}
      translate LOC}
#end

cylinder {< -6.41,  -6.41, -14.00>, < -6.41,   0.59,  -7.00>, Rcell pigment {Black}}
cylinder {<  0.59,  -6.41,  -7.00>, <  0.59,   0.59,   0.00>, Rcell pigment {Black}}
cylinder {<  7.59,   0.59,  -7.00>, <  7.59,   7.59,   0.00>, Rcell pigment {Black}}
cylinder {<  0.59,   0.59, -14.00>, <  0.59,   7.59,  -7.00>, Rcell pigment {Black}}
cylinder {< -6.41,  -6.41, -14.00>, <  0.59,  -6.41,  -7.00>, Rcell pigment {Black}}
cylinder {< -6.41,   0.59,  -7.00>, <  0.59,   0.59,   0.00>, Rcell pigment {Black}}
cylinder {<  0.59,   7.59,  -7.00>, <  7.59,   7.59,   0.00>, Rcell pigment {Black}}
cylinder {<  0.59,   0.59, -14.00>, <  7.59,   0.59,  -7.00>, Rcell pigment {Black}}
cylinder {< -6.41,  -6.41, -14.00>, <  0.59,   0.59, -14.00>, Rcell pigment {Black}}
cylinder {< -6.41,   0.59,  -7.00>, <  0.59,   7.59,  -7.00>, Rcell pigment {Black}}
cylinder {<  0.59,   0.59,   0.00>, <  7.59,   7.59,   0.00>, Rcell pigment {Black}}
cylinder {<  0.59,  -6.41,  -7.00>, <  7.59,   0.59,  -7.00>, Rcell pigment {Black}}
atom(< -6.41,  -6.41, -14.00>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #0 
atom(< -4.66,  -4.66, -14.00>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #1 
atom(< -2.91,  -2.91, -14.00>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #2 
atom(< -1.16,  -1.16, -14.00>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #3 
atom(< -4.66,  -6.41, -12.25>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #4 
atom(< -2.91,  -4.66, -12.25>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #5 
atom(< -1.16,  -2.91, -12.25>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #6 
atom(<  0.59,  -1.16, -12.25>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #7 
atom(< -2.91,  -6.41, -10.50>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #8 
atom(< -1.16,  -4.66, -10.50>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #9 
atom(<  0.59,  -2.91, -10.50>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #10 
atom(<  2.34,  -1.16, -10.50>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #11 
atom(< -1.16,  -6.41,  -8.75>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #12 
atom(<  0.59,  -4.66,  -8.75>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #13 
atom(<  2.34,  -2.91,  -8.75>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #14 
atom(<  4.09,  -1.16,  -8.75>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #15 
atom(< -6.41,  -4.66, -12.25>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #16 
atom(< -4.66,  -2.91, -12.25>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #17 
atom(< -2.91,  -1.16, -12.25>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #18 
atom(< -1.16,   0.59, -12.25>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #19 
atom(< -4.66,  -4.66, -10.50>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #20 
atom(< -2.91,  -2.91, -10.50>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #21 
atom(< -1.16,  -1.16, -10.50>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #22 
atom(<  0.59,   0.59, -10.50>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #23 
atom(< -2.91,  -4.66,  -8.75>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #24 
atom(< -1.16,  -2.91,  -8.75>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #25 
atom(<  0.59,  -1.16,  -8.75>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #26 
atom(<  2.34,   0.59,  -8.75>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #27 
atom(< -1.16,  -4.66,  -7.00>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #28 
atom(<  0.59,  -2.91,  -7.00>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #29 
atom(<  2.34,  -1.16,  -7.00>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #30 
atom(<  4.09,   0.59,  -7.00>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #31 
atom(< -6.41,  -2.91, -10.50>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #32 
atom(< -4.66,  -1.16, -10.50>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #33 
atom(< -2.91,   0.59, -10.50>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #34 
atom(< -1.16,   2.34, -10.50>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #35 
atom(< -4.66,  -2.91,  -8.75>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #36 
atom(< -2.91,  -1.16,  -8.75>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #37 
atom(< -1.16,   0.59,  -8.75>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #38 
atom(<  0.59,   2.34,  -8.75>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #39 
atom(< -2.91,  -2.91,  -7.00>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #40 
atom(< -1.16,  -1.16,  -7.00>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #41 
atom(<  0.59,   0.59,  -7.00>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #42 
atom(<  2.34,   2.34,  -7.00>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #43 
atom(< -1.16,  -2.91,  -5.25>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #44 
atom(<  0.59,  -1.16,  -5.25>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #45 
atom(<  2.34,   0.59,  -5.25>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #46 
atom(<  4.09,   2.34,  -5.25>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #47 
atom(< -6.41,  -1.16,  -8.75>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #48 
atom(< -4.66,   0.59,  -8.75>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #49 
atom(< -2.91,   2.34,  -8.75>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #50 
atom(< -1.16,   4.09,  -8.75>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #51 
atom(< -4.66,  -1.16,  -7.00>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #52 
atom(< -2.91,   0.59,  -7.00>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #53 
atom(< -1.16,   2.34,  -7.00>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #54 
atom(<  0.59,   4.09,  -7.00>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #55 
atom(< -2.91,  -1.16,  -5.25>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #56 
atom(< -1.16,   0.59,  -5.25>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #57 
atom(<  0.59,   2.34,  -5.25>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #58 
atom(<  2.34,   4.09,  -5.25>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #59 
atom(< -1.16,  -1.16,  -3.50>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #60 
atom(<  0.59,   0.59,  -3.50>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #61 
atom(<  2.34,   2.34,  -3.50>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #62 
atom(<  4.09,   4.09,  -3.50>, 1.17, rgb <0.78, 0.50, 0.20>, 0.0, glass) // #63 
