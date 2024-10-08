package com.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

class CombinedDistanceConverterTests {
    private final DistanceConverterController controller = new DistanceConverterController();

    @Test
    void test_meters_to_kilometers() {
        assertEquals(1.0, controller.metersToKilometers(1000), 0.001);
        assertEquals(0.5, controller.metersToKilometers(500), 0.001);
        assertEquals(0.0, controller.metersToKilometers(0), 0.001);
    }

    @Test
    void test_kilometers_to_meters() {
        assertEquals(1000.0, controller.kilometersToMeters(1), 0.001);
        assertEquals(500.0, controller.kilometersToMeters(0.5), 0.001);
        assertEquals(0.0, controller.kilometersToMeters(0), 0.001);
    }

    @Test
    void test_miles_to_kilometers() {
        assertEquals(1.60934, controller.milesToKilometers(1), 0.00001);
        assertEquals(0.80467, controller.milesToKilometers(0.5), 0.00001);
        assertEquals(0.0, controller.milesToKilometers(0), 0.00001);
    }

    @Test
    void test_kilometers_to_miles() {
        assertEquals(0.621371, controller.kilometersToMiles(1), 0.00001);
        assertEquals(0.310685, controller.kilometersToMiles(0.5), 0.00001);
        assertEquals(0.0, controller.kilometersToMiles(0), 0.00001);
    }
}
