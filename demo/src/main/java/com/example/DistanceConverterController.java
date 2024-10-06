package com.example;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/distanceConverter")
public class DistanceConverterController {

    @GetMapping("/metersToKilometers")
    public double metersToKilometers(@RequestParam double meters) {
        return meters / 1000;
    }

    @GetMapping("/kilometersToMeters")
    public double kilometersToMeters(@RequestParam double kilometers) {
        return kilometers * 1000;
    }

    @GetMapping("/milesToKilometers")
    public double milesToKilometers(@RequestParam double miles) {
        return miles * 1.60934;
    }

    @GetMapping("/kilometersToMiles")
    public double kilometersToMiles(@RequestParam double kilometers) {
        return kilometers / 1.60934;
    }
}
