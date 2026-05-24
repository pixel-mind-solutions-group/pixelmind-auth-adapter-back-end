package com.pixelmind.auth_adapter.controller.user;

import com.pixelmind.auth_adapter.dto.CommonResponseDTO;
import com.pixelmind.auth_adapter.dto.user.UserRequestDTO;
import com.pixelmind.auth_adapter.service.UserService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@Slf4j
@RequiredArgsConstructor
@RestController
@RequestMapping(value = "/api/pixel-auth-adapter/user")
public class UserController {

    private final UserService userService;

    @PostMapping(value = "/create-or-modify")
    public ResponseEntity<CommonResponseDTO> createOrModify(@RequestBody UserRequestDTO userRequest) {

        return ResponseEntity.ok(userService.createOrModify(userRequest));
    }

    @GetMapping(value = "/search")
    public ResponseEntity<CommonResponseDTO> search(@RequestParam(value = "searchParam") String searchParam,
                                                    @RequestParam(value = "page", required = false, defaultValue = "0") Integer page,
                                                    @RequestParam(value = "size", required = false, defaultValue = "5") Integer size) {
        return ResponseEntity.ok(userService.search(searchParam, page, size));
    }
}
