//


$fn = 100;

module hexagon(r) {
    polygon(points = [
        [cos(0)   * r, sin(0)   * r],
        [cos(60)  * r, sin(60)  * r],
        [cos(120) * r, sin(120) * r],
        [cos(180) * r, sin(180) * r],
        [cos(240) * r, sin(240) * r],
        [cos(300) * r, sin(300) * r]
    ]);
}

difference() {

    minkowski() {
        cube([105,95,65], center=true);
        sphere(1);
    }


    translate([0,0,-2.5])
        cube([100,90,65], center=true);


    translate([-60,-27,10])
        rotate([0,90,0])
            cylinder(r=3.5,h=200);

    // Prawa ściana
    for (z = [-25 : 7 : 25])
        for (y = [-35 : 8 : 35])
            translate([53, y + (z % 2) * 4, z])
                rotate([0,-90,0])
                    linear_extrude(height = 2.5, center = true)
                        hexagon(3.5);

    // Lewa ściana
    for (z = [-25 : 7 : 25])
        for (y = [-35 : 8 : 35])
            if (!(y > -33 && y < -27 && z > -5 && z < 5))
                translate([-53, y + (z % 2) * 4, z])
                    rotate([0,90,0])
                        linear_extrude(height = 2.5, center = true)
                            hexagon(3.5);

    // Przednia ściana
    for (x = [-45 : 8 : 45])
        for (z = [-25 : 7 : 25])
            translate([x + (z % 2) * 4, 48, z])
                rotate([90,0,0])
                    linear_extrude(height = 7, center = true)
                        hexagon(3.5);

    // Tylna ściana
    for (x = [-45 : 8 : 45])
        for (z = [-25 : 7 : 25])
            translate([x + (z % 2) * 4, -48, z])
                rotate([90,0,0])
                    linear_extrude(height = 7, center = true)
                        hexagon(3.5);
}
