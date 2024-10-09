package com.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class CombinedDistanceConverterTests {
    DistanceConverterController controller = new DistanceConverterController();

    @Test
    void test_meters_to_kilometers() {
        double result = controller.metersToKilometers(1000);
        assertEquals(1.0, result);
    }

    @Test
    void test_kilometers_to_meters() {
        double result = controller.kilometersToMeters(1);
        assertEquals(1000.0, result);
    }

    @Test
    void test_miles_to_kilometers() {
        double result = controller.milesToKilometers(1);
        assertEquals(1.60934, result, 0.00001);
    }

    @Test
    void test_kilometers_to_miles() {
        double result = controller.kilometersToMiles(1);
        assertEquals(0.621371, result, 0.00001);
    }

    @Test
    void test_meters_to_kilometers_zero() {
        double result = controller.metersToKilometers(0);
        assertEquals(0.0, result);
    }

    @Test
    void test_kilometers_to_meters_zero() {
        double result = controller.kilometersToMeters(0);
        assertEquals(0.0, result);
    }

    @Test
    void test_miles_to_kilometers_zero() {
        double result = controller.milesToKilometers(0);
        assertEquals(0.0, result);
    }

    @Test
    void test_kilometers_to_miles_zero() {
        double result = controller.kilometersToMiles(0);
        assertEquals(0.0, result);
    }

    @Test
    void test_meters_to_kilometers_negative() {
        double result = controller.metersToKilometers(-1000);
        assertEquals(-1.0, result);
    }

    @Test
    void test_kilometers_to_meters_negative() {
        double result = controller.kilometersToMeters(-1);
        assertEquals(-1000.0, result);
    }

    @Test
    void test_kilometers_to_miles_negative() {
        double result = controller.kilometersToMiles(-1);
        assertEquals(-0.621371, result, 0.00001);
    }

    @Test
    void test_kilometers_to_miles_non_numeric() {
        assertThrows(NumberFormatException.class, () -> {
            controller.kilometersToMiles(Double.parseDouble("notANumber"));
        });
    }
}
