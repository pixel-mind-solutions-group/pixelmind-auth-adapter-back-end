package com.pixelmind.auth_adapter.controller.application;

import com.pixelmind.auth_adapter.dto.CommonResponseDTO;
import com.pixelmind.auth_adapter.dto.application.ApplicationRequestDTO;
import com.pixelmind.auth_adapter.service.ApplicationService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RequiredArgsConstructor
@RestController
@RequestMapping(value = "/api/pixel-auth-adapter/application")
public class ApplicationController {

    private final ApplicationService applicationService;

    @PostMapping(value = "/create-or-modify")
    public ResponseEntity<CommonResponseDTO> createOrModify(@RequestParam(value = "realmName") String realmName,
                                                            @RequestBody ApplicationRequestDTO applicationRequest) {
        return ResponseEntity.ok(applicationService.createOrModify(realmName, applicationRequest));
    }

    @GetMapping(value = "/get-all")
    public ResponseEntity<CommonResponseDTO> getAll(@RequestParam(value = "realmName") String realmName,
                                                    @RequestParam(value = "page", required = false, defaultValue = "0") Integer page,
                                                    @RequestParam(value = "size", required = false, defaultValue = "5") Integer size) {
        return ResponseEntity.ok(applicationService.getAll(realmName, page, size));
    }
}
