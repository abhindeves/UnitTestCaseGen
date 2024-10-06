package com.example;

import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;

class TestDistanceConverter {
    @Test
    void test_meters_to_kilometers_basic() {
        DistanceConverterController controller = new DistanceConverterController();
        double result = controller.metersToKilometers(1000);
        assertEquals(1.0, result, 0.00001);
    }

    @Test
    void test_kilometers_to_meters_basic() {
        DistanceConverterController controller = new DistanceConverterController();
        double result = controller.kilometersToMeters(1);
        assertEquals(1000.0, result, 0.00001);
    }

    @Test
    void test_miles_to_kilometers_basic() {
        DistanceConverterController controller = new DistanceConverterController();
        double result = controller.milesToKilometers(1);
        assertEquals(1.60934, result, 0.00001);
    }

    @Test
    void test_kilometers_to_miles_basic() {
        DistanceConverterController controller = new DistanceConverterController();
        double result = controller.kilometersToMiles(1);
        assertEquals(0.621371, result, 0.00001);
    }
}
