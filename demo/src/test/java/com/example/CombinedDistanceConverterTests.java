package com.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

class CombinedDistanceConverterTests {
    private final DistanceConverterController controller = new DistanceConverterController();

    @Test
    void test_meters_to_kilometers_zero() {
        double result = controller.metersToKilometers(0);
        assertEquals(0, result);
    }

    @Test
    void test_kilometers_to_meters_zero() {
        double result = controller.kilometersToMeters(0);
        assertEquals(0, result);
    }

    @Test
    void test_miles_to_kilometers_zero() {
        double result = controller.milesToKilometers(0);
        assertEquals(0, result);
    }

    @Test
    void test_kilometers_to_miles_zero() {
        double result = controller.kilometersToMiles(0);
        assertEquals(0, result);
    }
}
