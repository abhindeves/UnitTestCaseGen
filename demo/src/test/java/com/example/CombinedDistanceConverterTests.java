package com.example;

import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;

class CombinedDistanceConverterTests {
    DistanceConverterController controller = new DistanceConverterController();

    @Test
    void testMetersToKilometersZero() {
        double result = controller.metersToKilometers(0);
        assertEquals(0, result);
    }

    @Test
    void testMetersToKilometersPositive() {
        double result = controller.metersToKilometers(1500);
        assertEquals(1.5, result);
    }

    @Test
    void testMetersToKilometersNegative() {
        double result = controller.metersToKilometers(-1000);
        assertEquals(-1, result);
    }

    @Test
    void testKilometersToMeters() {
        double result = controller.kilometersToMeters(2);
        assertEquals(2000, result);
    }

    @Test
    void testMilesToKilometers() {
        double result = controller.milesToKilometers(1);
        assertEquals(1.60934, result);
    }

    @Test
    void testKilometersToMiles() {
        double result = controller.kilometersToMiles(1.60934);
        assertEquals(1, result);
    }

    @Test
    void testMetersToKilometersLargeValue() {
        double result = controller.metersToKilometers(1000000);
        assertEquals(1000, result);
    }

    @Test
    void testKilometersToMetersLargeValue() {
        double result = controller.kilometersToMeters(1000);
        assertEquals(1000000, result);
    }
}
