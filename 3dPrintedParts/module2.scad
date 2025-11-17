$fn = 600;

difference(){
    cube([110,115,45], center=true);

    cube([102.5,110,40], center=true);
    translate([23.25,-25,16])
        cylinder(h=15,r=20,center=true);
    translate([-23.25,-25,16])
        cylinder(h=15,r=20,center=true);
    translate([21.5,2,17])
        cylinder(h=15,r=2.45,center=true);
    translate([-21.5,2,17])
        cylinder(h=15,r=2.45,center=true);
    translate([21.5,20,17])
        cylinder(h=15,r=9.5,center=true);
    translate([-21.5,20,17])
        cylinder(h=15,r=9.5,center=true);
    translate([0,0,-16])
        cube([112,120,45], center=true);


}

difference(){
    //23.25
    //1.75
    translate([23.25,-25,14.5])
        cylinder(h=16,r=21,center=true);
    translate([23.25,-25,16])
        cylinder(h=15,r=20,center=true);

    translate([32.7,-25,-20])
        cylinder(r=2.8,h=1600,center=true);
    translate([13.8,-25,-20])
        cylinder(r=2.8,h=1600,center=true);

    translate([23.25,-14.5,-20])
        cylinder(r=2.5,h=1600,center=true);

}
difference(){
    translate([-23.25,-25,14.5])
        cylinder(h=16,r=21,center=true);
    translate([-23.25,-25,16])
        cylinder(h=15,r=20,center=true);

    translate([-32.7,-25,-20])
        cylinder(r=2.8,h=1600,center=true);
    translate([-13.8,-25,-20])
        cylinder(r=2.8,h=1600,center=true);

    translate([-23.25,-14.5,-20])
        cylinder(r=2.5,h=1600,center=true);
}
difference(){
    translate([-32.7,-12,4])
        cube([4,7,7],center=true);

}
difference(){
    translate([-13.8,-12,4])
        cube([4,7,7],center=true);

}
translate([49,40,7.6])
    cube([5,5,2],center=true);
translate([49,-40,7.6])
    cube([5,5,2],center=true);

translate([-49,40,7.6])
    cube([5,5,2],center=true);
translate([-49,-40,7.6])
    cube([5,5,2],center=true);