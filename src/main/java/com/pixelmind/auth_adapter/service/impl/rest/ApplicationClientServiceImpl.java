package com.pixelmind.auth_adapter.service.impl.rest;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.pixelmind.auth_adapter.dto.CommonResponseDTO;
import com.pixelmind.auth_adapter.dto.application.ApplicationRequestDTO;
import com.pixelmind.auth_adapter.dto.client.ClientResponseDTO;
import com.pixelmind.auth_adapter.exception.BaseException;
import com.pixelmind.auth_adapter.service.rest.ApplicationClientService;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
@RequiredArgsConstructor
public class ApplicationClientServiceImpl implements ApplicationClientService {

    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper;

    @Value("${keycloak.adapter-url}")
    private String keycloakAdapterUrl;

    @Override
    public ClientResponseDTO createApplication(String realmName, ApplicationRequestDTO applicationRequest) {

        String url = keycloakAdapterUrl + "/api/keycloak-adapter/client/" + realmName + "/create";

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        try {

            HttpEntity<ApplicationRequestDTO> entity = new HttpEntity<>(applicationRequest, headers);
            ResponseEntity<CommonResponseDTO> response = restTemplate.exchange(
                    url,
                    HttpMethod.POST,
                    entity,
                    CommonResponseDTO.class
            );

            if (response.getStatusCode().is2xxSuccessful() &&
                    response.getBody().getStatus().equals(HttpStatus.CREATED.value()) &&
                    response.getBody().getData() != null) {
                return objectMapper.convertValue(response.getBody().getData(), ClientResponseDTO.class);
            } else {
                throw new BaseException(response.getBody().getStatus(),
                        response.getBody().getMessage()
                );
            }

        } catch (BaseException e) {
            throw new BaseException(e.getErrorCode(), e.getErrorDescription());

        } catch (Exception e) {
            throw new BaseException(HttpStatus.INTERNAL_SERVER_ERROR.value(), "Unexpected error occurred while creating a client by calling keycloak adapter. Error: " + e.getMessage());
        }
    }
}
