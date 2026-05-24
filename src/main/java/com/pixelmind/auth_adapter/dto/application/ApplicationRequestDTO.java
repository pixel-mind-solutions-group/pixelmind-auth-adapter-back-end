package com.pixelmind.auth_adapter.dto.application;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class ApplicationRequestDTO {
    private String id;
    private String clientId;
    private String description;
    private boolean enabled;
}
