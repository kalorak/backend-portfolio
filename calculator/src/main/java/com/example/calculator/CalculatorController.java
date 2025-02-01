package com.example.calculator;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/calculator")
public class CalculatorController {

    @GetMapping("/add")
    public double add(@RequestParam double a, @RequestParam double b) {
        return a + b;
    }

    @GetMapping("/subtract")
    public double subtract(@RequestParam double a, @RequestParam double b) {
        return a - b;
    }

    @GetMapping("/multiply")
    public double multiply(@RequestParam double a, @RequestParam double b) {
        return a * b;
    }

    @GetMapping("/divide")
    public ResponseEntity<?> divide(@RequestParam double a, @RequestParam double b) {
        if (b == 0) {
            return ResponseEntity.badRequest().body("Hiba: 0-val nem lehet osztani!");
        }
        return ResponseEntity.ok(a / b);
    }
}