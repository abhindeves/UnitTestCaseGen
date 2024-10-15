package com.example;

import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;

class CombinedDistanceConverterTests {
    @Test
    void testMetersToKilometersPositive() {
        DistanceConverterController controller = new DistanceConverterController();
        double result = controller.metersToKilometers(1500);
        assertEquals(1.5, result);
    }

    @Test
    void testMetersToKilometersZero() {
        DistanceConverterController controller = new DistanceConverterController();
        double result = controller.metersToKilometers(0);
        assertEquals(0, result);
    }

    @Test
    void testKilometersToMetersPositive() {
        DistanceConverterController controller = new DistanceConverterController();
        double result = controller.kilometersToMeters(2);
        assertEquals(2000, result);
    }

    @Test
    void testMilesToKilometersPositive() {
        DistanceConverterController controller = new DistanceConverterController();
        double result = controller.milesToKilometers(1);
        assertEquals(1.60934, result);
    }

    @Test
    void testKilometersToMilesPositive() {
        DistanceConverterController controller = new DistanceConverterController();
        double result = controller.kilometersToMiles(1.60934);
        assertEquals(1, result);
    }
}
