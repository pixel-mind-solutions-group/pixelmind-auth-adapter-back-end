package com.pixelmind.auth_adapter.service.rest;

import com.pixelmind.auth_adapter.dto.application.ApplicationRequestDTO;
import com.pixelmind.auth_adapter.dto.client.ClientResponseDTO;

public interface ApplicationClientService {

    ClientResponseDTO createApplication(String realmName, ApplicationRequestDTO applicationRequest);

    ClientResponseDTO updateApplication(String realmName, String clientId, ApplicationRequestDTO applicationRequest);
}
