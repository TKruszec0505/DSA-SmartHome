$fn = 100;



difference() {
    // Płaska płyta z zaokrąglonymi krawędziami
    minkowski() {
        cube([105,95,2.5], center=true);
        sphere(1);
    }

    // Napis grawerowany w płycie

    translate([0,35,1.3])
        linear_extrude(height = 1.5)
            text("TK Electronics™",
            size = 4,
            halign="center",
            valign="center");
    translate([0, 29, 1.3])
        linear_extrude(height = 1.5)
            text("DSA - Domowy System Automatyzacji",
            size = 4,
            halign="center",
            valign="center");
    translate([0, 23, 1.3])
        linear_extrude(height = 1.5)
            text("Moduł 1",
            size = 4,
            halign="center",
            valign="center");
    translate([0,0,1.5])
        cylinder(r=9.5,h=8,center=true);
}
