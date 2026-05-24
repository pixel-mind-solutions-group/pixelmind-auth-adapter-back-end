package com.pixelmind.auth_adapter.dto.client;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class ClientResponseDTO {
    private String clientUUID;
    private String clientId;
    private String clientSecret;
}
