package com.example.brake.controller;

import com.example.brake.dto.SensorDTO;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.*;

@RestController
@RequestMapping("/api/brake")
@CrossOrigin(origins = "*")
public class BrakeController {

    private final RestTemplate restTemplate = new RestTemplate();
    private final String AI_SERVICE_URL = "http://localhost:8000/analyze";

    @PostMapping("/diagnose")
    public ResponseEntity<Object> diagnose(@RequestBody SensorDTO dto) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        
        HttpEntity<SensorDTO> entity = new HttpEntity<>(dto, headers);
        
        try {
            Object result = restTemplate.postForObject(AI_SERVICE_URL, entity, Object.class);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            return ResponseEntity.status(500).body("AI Service Error: " + e.getMessage());
        }
    }
}
